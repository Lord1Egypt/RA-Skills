from pathlib import Path

import modal

import src.config as config


volume_data = modal.Volume.from_name(config.VOLUME_DATA_NAME, create_if_missing=True)
volume_models = modal.Volume.from_name(
    config.VOLUME_MODELS_NAME, create_if_missing=True
)


_src_dir = str(Path(__file__).parent)

image_denoise = (
    modal.Image.debian_slim(python_version=config.PYTHON_VERSION)
    .apt_install("ffmpeg")
    .pip_install(
        [
            "clearvoice",
            "torch>=2.0.1",
            "torchaudio>=2.0.2",
        ]
    )
    .env({"TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS": "1"})
    .add_local_dir(_src_dir, remote_path="/root/src", copy=True)
)


app = modal.App(config.APP_NAME)
