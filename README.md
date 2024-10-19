# faster-whisper-server
Fork of [faster-whisper-server](https://github.com/fedirz/faster-whisper-server) - ready for local venv deploy to integration with [Open WebUI](https://github.com/open-webui/open-webui)

# OpenAI API Compatibility ++
See [OpenAI API reference](https://platform.openai.com/docs/api-reference/audio) for more information.
* Audio file transcription via POST /v1/audio/transcriptions endpoint.
* Unlike OpenAI's API, faster-whisper-server also supports streaming transcriptions (and translations). This is useful for when you want to process large audio files and would rather receive the transcription in chunks as they are processed, rather than waiting for the whole file to be transcribed. It works similarly to chat messages when chatting with LLMs.
* Audio file translation via POST /v1/audio/translations endpoint.
* Live audio transcription via WS /v1/audio/transcriptions endpoint.
        LocalAgreement2 (paper | original implementation) algorithm is used for live transcription.
        Only transcription of a single channel, 16000 sample rate, raw, 16-bit little-endian audio is supported.

> [!NOTE]
> This repoository includes cudnn and cuBLAS libraries for linux at: `./whisper-server/src/cudnn/`
> cuBLAS for CUDA 12
> cuDNN 8 for CUDA 12

# Installation for linux
1. Clone the repository
```git clone https://github.com/Lefox-DeMod/faster-whisper-server```
2. Go to  folder `cd ./faster-whisper-server` and run `source venv/bin/activate`
3. Run pip to run install from `requirements.txt`: `pip install -r requirements.txt`

# Usage
To run whisper-server: `./run-whisper-server.sh`

# Integration with Open WebUI
1. Go to admin panel of OpenWebUI and select audio settings
2. Select STT (speech to text) and switch OpenAI
3. Put local adress of running whisper-server to empty field such as: `http://127.0.0.1:8000/v1`
4. Select model of whisper to Speech recognition model field, avanable models:
    `tiny.en, tiny, base.en, base, small.en, small, medium.en, medium, large-v1, large-v2, large-v3, large, distil-large-v2, distil-medium.en, distil-small.en, distil-large-v3`

   Set default model you can in `./whisper-server/src/faster_whisper_server/routers/stt.py` in field  "return {"models": ["small"]}"
5. Field Key API can't be empty. Put something: `sk-111111111`
6. Save settings

# Gratio WebUI 
You can use WebUI to speech recognition localy go to `http://127.0.0.1:8000/`
