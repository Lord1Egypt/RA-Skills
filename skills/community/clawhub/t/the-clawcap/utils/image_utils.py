"""
图像工具函数：加载、转换、验证
"""

import base64
import io
from typing import Tuple

import httpx
from PIL import Image

from config import MIN_IMAGE_SIZE, MAX_IMAGE_SIZE


async def load_image_from_url(url: str) -> Image.Image:
    """从 URL 下载并加载图像"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return Image.open(io.BytesIO(resp.content)).convert("RGBA")


def load_image_from_base64(b64_string: str) -> Image.Image:
    """从 Base64 字符串加载图像"""
    # 移除可能存在的 data:image/xxx;base64, 前缀
    if "," in b64_string:
        b64_string = b64_string.split(",", 1)[1]
    raw = base64.b64decode(b64_string)
    return Image.open(io.BytesIO(raw)).convert("RGBA")


def validate_image(img: Image.Image) -> None:
    """校验图像尺寸，不符合则抛出 ValueError"""
    w, h = img.size
    min_dim = min(w, h)
    max_dim = max(w, h)
    if min_dim < MIN_IMAGE_SIZE:
        raise ValueError(
            f"图像分辨率过低：{w}x{h}，最小要求 {MIN_IMAGE_SIZE}x{MIN_IMAGE_SIZE}"
        )
    if max_dim > MAX_IMAGE_SIZE:
        raise ValueError(
            f"图像分辨率过高：{w}x{h}，最大允许 {MAX_IMAGE_SIZE}x{MAX_IMAGE_SIZE}"
        )


def image_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    """将 PIL Image 转为字节流"""
    buf = io.BytesIO()
    # PNG 不支持 RGBA 以外的某些模式，确保兼容
    if fmt.upper() == "JPEG" and img.mode == "RGBA":
        img = img.convert("RGB")
    img.save(buf, format=fmt)
    return buf.getvalue()


def image_to_base64(img: Image.Image, fmt: str = "PNG") -> str:
    """将 PIL Image 转为 Base64 字符串"""
    raw = image_to_bytes(img, fmt)
    return base64.b64encode(raw).decode("utf-8")


def resize_for_processing(img: Image.Image, target: int = 1024) -> Image.Image:
    """
    将图像缩放到目标尺寸（保持宽高比），
    使最大边不超过 target。
    """
    w, h = img.size
    if max(w, h) <= target:
        return img.copy()
    ratio = target / max(w, h)
    new_size = (int(w * ratio), int(h * ratio))
    return img.resize(new_size, Image.LANCZOS)


def get_image_dimensions(img: Image.Image) -> Tuple[int, int]:
    """返回 (width, height)"""
    return img.size
