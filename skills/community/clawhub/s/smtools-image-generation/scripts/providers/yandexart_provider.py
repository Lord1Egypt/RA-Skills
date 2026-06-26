import base64
import json
import time
from datetime import datetime
from pathlib import Path

import requests

from providers.base_provider import BaseImageProvider
from config_manager import get_api_key, get_output_dir

GENERATE_URL = "https://ai.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"
OPERATION_URL = "https://operation.api.cloud.yandex.net:443/operations"

DEFAULT_MODELS = [
    "yandex-art/latest",
]


class YandexArtProvider(BaseImageProvider):
    name = "yandexart"

    def __init__(self, config: dict):
        self.config = config
        self.provider_config = config.get("providers", {}).get("yandexart", {})
        self.default_model = self.provider_config.get("default_model", "yandex-art/latest")
        self.poll_interval = self.provider_config.get("poll_interval", 5)
        self.max_wait = self.provider_config.get("max_wait", 600)
        self.folder_id = self.provider_config.get("folder_id") or self._get_folder_id()

    def _get_folder_id(self) -> str:
        import os
        fid = os.getenv("YANDEX_FOLDER_ID", "")
        return fid

    def validate_config(self, config: dict) -> bool:
        try:
            get_api_key("yandexart")
            return bool(self.folder_id)
        except EnvironmentError:
            return False

    def list_models(self) -> list:
        return DEFAULT_MODELS

    def generate(self, prompt: str, model: str = None, output_path: str = None, input_image: str = None) -> dict:
        api_key = get_api_key("yandexart")
        model = model or self.default_model

        if not self.folder_id:
            return {
                "status": "error",
                "error": "YANDEX_FOLDER_ID not set. Required for YandexART.",
                "provider": self.name,
            }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        model_uri = f"art://{self.folder_id}/{model}"

        payload = {
            "modelUri": model_uri,
            "generationOptions": {
                "aspectRatio": {
                    "widthRatio": "1",
                    "heightRatio": "1",
                },
            },
            "messages": [
                {"text": prompt, "weight": "1"},
            ],
        }

        response = requests.post(GENERATE_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        op_data = response.json()
        operation_id = op_data.get("id")

        if not operation_id:
            return {
                "status": "error",
                "error": f"No operation ID in response: {json.dumps(op_data)[:300]}",
                "provider": self.name,
                "model": model,
            }

        image_b64 = self._poll_until_done(operation_id, headers)

        if image_b64 is None:
            return {
                "status": "error",
                "error": f"Operation {operation_id} timed out after {self.max_wait}s",
                "provider": self.name,
                "model": model,
            }

        image_bytes = base64.b64decode(image_b64)

        if output_path is None:
            output_dir = get_output_dir(self.config)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = output_dir / f"img_{timestamp}.png"
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_bytes)

        return {
            "status": "ok",
            "image_path": str(output_path.resolve()),
            "model": model,
            "provider": self.name,
            "metadata": {
                "operation_id": operation_id,
                "size_bytes": len(image_bytes),
            },
        }

    def _poll_until_done(self, operation_id: str, headers: dict) -> str | None:
        elapsed = 0
        interval = self.poll_interval

        while elapsed < self.max_wait:
            time.sleep(interval)
            elapsed += interval

            resp = requests.get(
                f"{OPERATION_URL}/{operation_id}",
                headers=headers,
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()

            if data.get("done"):
                return data.get("response", {}).get("image")
            if data.get("error"):
                return None

            interval = min(interval * 1.5, 30)

        return None
