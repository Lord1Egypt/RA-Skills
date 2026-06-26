import json
import time
from datetime import datetime
from pathlib import Path

import requests

from providers.base_provider import BaseImageProvider
from config_manager import get_api_key, get_output_dir

CREATE_TASK_URL = "https://api.kie.ai/api/v1/jobs/createTask"
RECORD_INFO_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"

DEFAULT_MODELS = [
    "nano-banana-2",
    "flux-ai",
    "midjourney",
    "google-4o-image",
    "ghibli-ai",
]


class KieProvider(BaseImageProvider):
    name = "kie"

    def __init__(self, config: dict):
        self.config = config
        self.provider_config = config.get("providers", {}).get("kie", {})
        self.default_model = self.provider_config.get("default_model", "google-4o-image")
        self.poll_interval = self.provider_config.get("poll_interval", 5)
        self.max_wait = self.provider_config.get("max_wait", 300)

    def validate_config(self, config: dict) -> bool:
        try:
            get_api_key("kie")
            return True
        except EnvironmentError:
            return False

    def list_models(self) -> list:
        return DEFAULT_MODELS

    def generate(self, prompt: str, model: str = None, output_path: str = None, input_image: str = None) -> dict:
        api_key = get_api_key("kie")
        model = model or self.default_model

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        input_block = {
            "prompt": prompt,
            "aspect_ratio": "auto",
            "resolution": "1K",
            "output_format": "jpg",
        }

        # Add input image for editing (Kie expects URLs)
        if input_image:
            input_block["image_input"] = [input_image]

        payload = {
            "model": model,
            "input": input_block,
        }

        response = requests.post(CREATE_TASK_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        task_data = response.json()
        task_id = task_data.get("taskId") or task_data.get("data", {}).get("taskId")

        if not task_id:
            return {
                "status": "error",
                "error": f"No taskId in response: {json.dumps(task_data)[:300]}",
                "provider": self.name,
                "model": model,
            }

        result_url = self._poll_until_done(task_id, headers)

        if result_url is None:
            return {
                "status": "error",
                "error": f"Task {task_id} timed out after {self.max_wait}s",
                "provider": self.name,
                "model": model,
            }

        if output_path is None:
            output_dir = get_output_dir(self.config)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = output_dir / f"img_{timestamp}.jpg"
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        img_response = requests.get(result_url, timeout=60)
        img_response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(img_response.content)

        return {
            "status": "ok",
            "image_path": str(output_path.resolve()),
            "model": model,
            "provider": self.name,
            "metadata": {
                "task_id": task_id,
                "size_bytes": len(img_response.content),
            },
        }

    def _poll_until_done(self, task_id: str, headers: dict) -> str | None:
        elapsed = 0
        interval = self.poll_interval

        while elapsed < self.max_wait:
            time.sleep(interval)
            elapsed += interval

            resp = requests.get(
                RECORD_INFO_URL, headers=headers, params={"taskId": task_id}, timeout=15
            )
            resp.raise_for_status()
            data = resp.json()

            state = data.get("state")
            if state == "success":
                result_json = data.get("resultJson", "{}")
                result_urls = json.loads(result_json).get("resultUrls", [])
                return result_urls[0] if result_urls else None
            if state == "fail":
                return None

            interval = min(interval * 1.5, 30)

        return None
