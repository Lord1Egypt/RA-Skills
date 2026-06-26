from pathlib import Path

import modal

import src.config as config


volume_data = modal.Volume.from_name(config.VOLUME_DATA_NAME, create_if_missing=True)
volume_models = modal.Volume.from_name(
    config.VOLUME_MODELS_NAME, create_if_missing=True
)


_src_dir = str(Path(__file__).parent)

image_whisper = (
    modal.Image.from_registry(
        "nvidia/cuda:12.8.1-cudnn-runtime-ubuntu22.04", add_python="3.12"
    )
    .entrypoint([])
    .apt_install("ffmpeg")
    .pip_install("faster-whisper", "stable-ts")
    .env({"TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS": "1"})
    .add_local_dir(_src_dir, remote_path="/root/src")
)


app_whisper = modal.App(config.APP_NAME)
