from __future__ import annotations

from contextlib import asynccontextmanager
import logging
import os
import ctypes  # Add ctypes for work with libraries
from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from faster_whisper_server.dependencies import get_config, get_model_manager
from faster_whisper_server.logger import setup_logger
from faster_whisper_server.routers.list_models import router as list_models_router
from faster_whisper_server.routers.misc import router as misc_router
from faster_whisper_server.routers.stt import router as stt_router

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


# Loading libraries cuDNN and cuBLAS via ctypes
def load_cuda_libraries():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cublas_path = os.path.join(current_dir, "cudnn", "libcublas.so.12")
    cublasLt_path = os.path.join(current_dir, "cudnn", "libcublasLt.so.12")
    cudnn_cnn_infer_path = os.path.join(current_dir, "cudnn", "libcudnn_cnn_infer.so.8")
    cudnn_ops_infer_path = os.path.join(current_dir, "cudnn", "libcudnn_ops_infer.so.8")

    try:
        ctypes.CDLL(cublas_path)
        print("libcublas.so.12 success load!")

        ctypes.CDLL(cublasLt_path)
        print("libcublasLt.so.12 success load!!")

        ctypes.CDLL(cudnn_cnn_infer_path)
        print("libcudnn_cnn_infer.so.8 success load!!")

        ctypes.CDLL(cudnn_ops_infer_path)
        print("libcudnn_ops_infer.so.8 success load!!")

    except OSError as e:
        print(f"Error loading: {e}")


# Load Cuda Libraries
load_cuda_libraries()

# FastAPI
def create_app() -> FastAPI:
    logging.info("Creating app...")
    setup_logger()

    logger = logging.getLogger(__name__)

    config = get_config()  # HACK
    logger.debug(f"Config: {config}")

    model_manager = get_model_manager()  # HACK

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
        for model_name in config.preload_models:
            model_manager.load_model(model_name)
        yield

    app = FastAPI(lifespan=lifespan)

    app.include_router(stt_router)
    app.include_router(list_models_router)
    app.include_router(misc_router)

    if config.allow_origins is not None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.allow_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    if config.enable_ui:
        import gradio as gr

        from faster_whisper_server.gradio_app import create_gradio_demo

        app = gr.mount_gradio_app(app, create_gradio_demo(config), path="/")

    return app


if __name__ == "__main__":
    import uvicorn
    logging.info("Starting server...")
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
