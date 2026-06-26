import base64
import json
import re
import requests

from datetime import datetime
from pathlib import Path

from providers.base_provider import BaseImageProvider
from config_manager import get_api_key, get_output_dir

API_URL = "https://openrouter.ai/api/v1/chat/completions"

DEFAULT_MODELS = [
    "google/gemini-3.1-flash-image-preview",
    "openai/gpt-image-1",
    "google/imagen-4",
    "stabilityai/stable-diffusion-3",
]


class OpenRouterProvider(BaseImageProvider):
    name = "openrouter"

    def __init__(self, config: dict):
        self.config = config
        self.provider_config = config.get("providers", {}).get("openrouter", {})
        self.default_model = self.provider_config.get(
            "default_model", "google/gemini-3.1-flash-image-preview"
        )
        self.max_tokens = self.provider_config.get("max_tokens", 4096)

    def validate_config(self, config: dict) -> bool:
        try:
            get_api_key("openrouter")
            return True
        except EnvironmentError:
            return False

    def list_models(self) -> list:
        return DEFAULT_MODELS

    def generate(self, prompt: str, model: str = None, output_path: str = None, input_image: str = None) -> dict:
        api_key = get_api_key("openrouter")
        model = model or self.default_model

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # Build message content: text-only or image+text for editing
        if input_image:
            image_b64 = self._encode_image(input_image)
            content = [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
                {"type": "text", "text": prompt},
            ]
        else:
            content = prompt

        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": content}
            ],
            "modalities": ["image", "text"],
            "max_tokens": self.max_tokens,
        }

        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        data = response.json()
        image_data = self._extract_image(data)

        if image_data is None:
            return {
                "status": "error",
                "error": "No image found in API response",
                "provider": self.name,
                "model": model,
                "raw_response": json.dumps(data)[:500],
            }

        image_bytes = base64.b64decode(image_data)

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
                "size_bytes": len(image_bytes),
                "usage": data.get("usage", {}),
            },
        }

    @staticmethod
    def _encode_image(path: str) -> str:
        """Read an image file and return base64-encoded string."""
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    def _extract_image(self, data: dict) -> str:
        """Extract base64 image data from OpenRouter response.

        Checks multiple locations where OpenRouter may place image data:
        1. message.images[] — dedicated images array (documented format)
        2. message.content (list) — structured content blocks
        3. message.content (str) — inline base64 data URLs
        """
        choices = data.get("choices", [])
        if not choices:
            return None

        message = choices[0].get("message", {})

        # 1. Check message.images[] — primary documented format
        images = message.get("images", [])
        for img in images:
            if isinstance(img, dict) and img.get("type") == "image_url":
                url = img.get("image_url", {}).get("url", "")
                b64 = self._parse_data_url(url)
                if b64:
                    return b64

        # 2. Check message.content
        content = message.get("content")
        if content is None:
            return None

        # Structured content blocks (list of dicts)
        if isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "image_url":
                    url = block.get("image_url", {}).get("url", "")
                    b64 = self._parse_data_url(url)
                    if b64:
                        return b64
                if block.get("type") == "image":
                    b64 = block.get("data") or block.get("base64")
                    if b64:
                        return b64
                    url = block.get("url", "")
                    b64 = self._parse_data_url(url)
                    if b64:
                        return b64

        # String content — inline data URL or markdown image
        if isinstance(content, str):
            b64 = self._parse_data_url(content)
            if b64:
                return b64
            match = re.search(r"!\[.*?\]\((data:image/[^)]+)\)", content)
            if match:
                return self._parse_data_url(match.group(1))

        return None

    @staticmethod
    def _parse_data_url(url: str) -> str:
        """Extract base64 data from a data: URL."""
        match = re.match(r"data:image/[^;]+;base64,(.+)", url, re.DOTALL)
        return match.group(1).strip() if match else None
