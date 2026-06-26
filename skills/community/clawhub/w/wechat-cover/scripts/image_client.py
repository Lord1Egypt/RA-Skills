"""Shared interface and utilities for image generation providers."""

import base64
import io
from pathlib import Path
from typing import Protocol

from PIL import Image

# WeChat cover: 2.35:1 aspect ratio
WECHAT_COVER_WIDTH = 900
WECHAT_COVER_HEIGHT = 383


class ImageGenerationError(Exception):
    """Raised when image generation fails."""
    pass


class ImageClient(Protocol):
    """
    Abstract interface for image generation providers.

    Raises:
        ImageGenerationError: On network failure, auth failure, or generation error.
    """

    def generate(
        self,
        prompt: str,
        filename: str,
        resolution: str,
        api_key: str,
    ) -> Path:
        """
        Generate an image from a text prompt.

        Args:
            prompt: Image description/prompt
            filename: Output filename (including path)
            resolution: Resolution tier ("1K", "2K", "4K")
            api_key: API key for authentication

        Returns:
            Path to the generated image file

        Raises:
            ImageGenerationError: On any failure
        """
        ...


def crop_to_wechat_cover(image_bytes: bytes) -> bytes:
    """Crop and resize image to WeChat cover dimensions (900x383, 2.35:1).

    Centers a 2.35:1 crop from the generated image, then downscales
    to 900x383. Works with any input aspect ratio.

    Args:
        image_bytes: Raw image bytes (PNG, JPEG, etc.)

    Returns:
        PNG bytes at 900x383
    """
    img = Image.open(io.BytesIO(image_bytes))
    src_w, src_h = img.size
    target_ratio = WECHAT_COVER_WIDTH / WECHAT_COVER_HEIGHT
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))

    img = img.resize((WECHAT_COVER_WIDTH, WECHAT_COVER_HEIGHT), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
