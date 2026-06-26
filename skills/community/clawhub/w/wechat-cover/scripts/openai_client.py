"""OpenAI-compatible image generation client.

Supports two API formats:
1. /v1/images/generations - Standard OpenAI DALL-E format
2. /v1/chat/completions (streaming) - Chat-based image generation
   used by some gateways (e.g. palebluedot) for models like Seedream.
"""

import base64
from pathlib import Path

from openai import OpenAI

from image_client import ImageClient, ImageGenerationError, crop_to_wechat_cover

# DALL-E 3 supported sizes
DALLE3_SIZES = {
    "1K": "1024x1024",
    "2K": "1792x1024",
    "4K": "1792x1024",
}

# DALL-E 2 supported sizes
DALLE2_SIZES = {
    "1K": "1024x1024",
    "2K": "1024x1024",
    "4K": "1024x1024",
}

# Prefix for base64 data URIs
_DATA_URI_PREFIX = "data:image/"


class OpenAIImageClient(ImageClient):
    """OpenAI-compatible image generation.

    Tries /v1/images/generations first, falls back to
    /v1/chat/completions streaming (for Seedream-style gateways).
    """

    def __init__(
        self,
        model: str = "dall-e-3",
        base_url: str | None = None,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/") if base_url else None

    def _resolve_resolution(self, resolution: str) -> str:
        """Map resolution tier to provider-specific size string."""
        if "dall-e-3" in self.model:
            return DALLE3_SIZES.get(resolution, "1792x1024")
        return DALLE2_SIZES.get(resolution, "1024x1024")

    def generate(
        self,
        prompt: str,
        filename: str,
        resolution: str,
        api_key: str,
    ) -> Path:
        """
        Generate image using OpenAI-compatible API.

        Raises:
            ImageGenerationError: On any failure
        """
        if not prompt or not prompt.strip():
            raise ImageGenerationError("Prompt cannot be empty")
        if not api_key or not api_key.strip():
            raise ImageGenerationError("API key cannot be empty")
        if not self.base_url:
            raise ImageGenerationError("base_url is required")

        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        client = OpenAI(base_url=self.base_url, api_key=api_key, timeout=120)

        try:
            image_bytes = self._try_images_api(client, prompt, resolution)
        except ImageGenerationError:
            image_bytes = self._try_chat_completions_api(client, prompt, resolution)

        if not image_bytes:
            raise ImageGenerationError("Failed to generate image")

        output_path.write_bytes(crop_to_wechat_cover(image_bytes))
        return output_path.resolve()

    # ------------------------------------------------------------------
    # Format 1: /v1/images/generations (standard DALL-E)
    # ------------------------------------------------------------------

    def _try_images_api(
        self, client: OpenAI, prompt: str, resolution: str
    ) -> bytes | None:
        """Try standard /v1/images/generations endpoint."""
        size = self._resolve_resolution(resolution)

        try:
            response = client.images.generate(
                model=self.model,
                prompt=prompt,
                n=1,
                size=size,
                response_format="b64_json",
            )
        except Exception as e:
            raise ImageGenerationError(f"Images API error: {e}") from e

        data = response.data[0]
        b64 = getattr(data, "b64_json", None) or getattr(data, "url", None)
        if not b64:
            return None

        # b64_json returns raw base64; url returns a URL string
        if b64.startswith("http"):
            try:
                import urllib.request
                with urllib.request.urlopen(b64, timeout=120) as resp:
                    return resp.read()
            except Exception as e:
                raise ImageGenerationError(f"Download failed: {e}") from e

        return base64.b64decode(b64)

    # ------------------------------------------------------------------
    # Format 2: /v1/chat/completions streaming (Seedream-style)
    # ------------------------------------------------------------------

    def _try_chat_completions_api(
        self, client: OpenAI, prompt: str, resolution: str
    ) -> bytes:
        """Try /v1/chat/completions with streaming to extract image.

        Gateways like palebluedot return image data in non-standard
        ``delta.images`` field. The SDK preserves these via extra="allow".
        """
        size = self._resolve_resolution(resolution)
        try:
            stream = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": f"{prompt}\n\n[Image size: {size}]"}],
                stream=True,
            )
        except Exception as e:
            raise ImageGenerationError(f"Chat completions error: {e}") from e

        chunks: list[str] = []

        for part in stream:
            delta = part.choices[0].delta
            # Non-standard field preserved by SDK's extra="allow"
            images = getattr(delta, "images", None) or []
            for img in images:
                img_url = img.get("image_url", {}).get("url", "")
                if img_url.startswith(_DATA_URI_PREFIX):
                    chunks.append(img_url.split(",", 1)[1])

        if not chunks:
            raise ImageGenerationError("No image data found in stream")

        return base64.b64decode("".join(chunks))
