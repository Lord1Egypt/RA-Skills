from __future__ import annotations

import base64
import io
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
from PIL import Image, ImageDraw, ImageFont

from .models import ImageGenerationConfig, ProviderConfig
from .utils import ensure_dir, normalize_whitespace


@dataclass(frozen=True)
class CoverTemplate:
    name: str
    prompt_suffix: str
    title_fill: tuple[int, int, int]
    subtitle_fill: tuple[int, int, int]
    accent_fill: tuple[int, int, int]


TEMPLATES: dict[str, CoverTemplate] = {
    "magazine": CoverTemplate(
        name="magazine",
        prompt_suffix="editorial cover, modern Chinese business magazine, premium layout, clean focal area for text",
        title_fill=(255, 255, 255),
        subtitle_fill=(240, 245, 255),
        accent_fill=(87, 181, 231),
    ),
    "minimal": CoverTemplate(
        name="minimal",
        prompt_suffix="minimal Chinese social media cover, soft gradient background, spacious composition",
        title_fill=(34, 40, 49),
        subtitle_fill=(70, 86, 108),
        accent_fill=(47, 128, 237),
    ),
    "insight": CoverTemplate(
        name="insight",
        prompt_suffix="deep insight cover, warm editorial tone, visual metaphor, high contrast title area",
        title_fill=(255, 248, 238),
        subtitle_fill=(255, 232, 204),
        accent_fill=(245, 158, 11),
    ),
}


class CoverGenerationError(RuntimeError):
    pass


def _pick_provider(config: ImageGenerationConfig, provider_name: str) -> ProviderConfig:
    provider = (provider_name or config.provider or "doubao").strip().lower()
    return config.qwen if provider == "qwen" else config.doubao


def _decode_image_data(payload: dict[str, Any]) -> bytes:
    data = payload.get("data") or []
    if not data:
        raise CoverGenerationError("图像接口未返回图片数据")
    item = data[0]
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    if item.get("url"):
        response = requests.get(item["url"], timeout=60)
        response.raise_for_status()
        return response.content
    raise CoverGenerationError("图像接口返回格式无法识别")


def _generate_with_doubao(provider: ProviderConfig, prompt: str, size: str, quality: str) -> bytes:
    if not provider.api_key or not provider.model:
        raise CoverGenerationError("豆包图像生成配置不完整，请补充 api_key 和 model")
    base_url = provider.base_url or "https://ark.cn-beijing.volces.com/api/v3"
    response = requests.post(
        f"{base_url.rstrip('/')}/images/generations",
        headers={"Authorization": f"Bearer {provider.api_key}", "Content-Type": "application/json"},
        json={"model": provider.model, "prompt": prompt, "size": size, "quality": quality, "response_format": "b64_json"},
        timeout=120,
    )
    response.raise_for_status()
    return _decode_image_data(response.json())


def _generate_with_qwen(provider: ProviderConfig, prompt: str, size: str) -> bytes:
    if not provider.api_key or not provider.model:
        raise CoverGenerationError("通义千问图像生成配置不完整，请补充 api_key 和 model")
    base_url = provider.base_url or "https://dashscope.aliyuncs.com/api/v1"
    response = requests.post(
        f"{base_url.rstrip('/')}/services/aigc/text2image/image-synthesis",
        headers={
            "Authorization": f"Bearer {provider.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable",
        },
        json={"model": provider.model, "input": {"prompt": prompt}, "parameters": {"size": size}},
        timeout=120,
    )
    response.raise_for_status()
    payload = response.json()
    task_id = payload.get("output", {}).get("task_id")
    if not task_id:
        raise CoverGenerationError(f"通义千问未返回 task_id: {payload}")

    status_url = f"{base_url.rstrip('/')}/tasks/{task_id}"
    for _ in range(30):
        poll = requests.get(status_url, headers={"Authorization": f"Bearer {provider.api_key}"}, timeout=60)
        poll.raise_for_status()
        result = poll.json()
        task_status = result.get("output", {}).get("task_status")
        if task_status == "SUCCEEDED":
            results = result.get("output", {}).get("results") or []
            if not results or not results[0].get("url"):
                raise CoverGenerationError("通义千问任务成功但未返回图片 URL")
            image_response = requests.get(results[0]["url"], timeout=120)
            image_response.raise_for_status()
            return image_response.content
        if task_status in {"FAILED", "CANCELED"}:
            raise CoverGenerationError(f"通义千问封面生成失败: {result}")
        time.sleep(2)
    raise CoverGenerationError("通义千问封面生成超时")


def _font(size: int, bold: bool = False):
    candidates = [
        "C:\\Windows\\Fonts\\msyhbd.ttc" if bold else "C:\\Windows\\Fonts\\msyh.ttc",
        "C:\\Windows\\Fonts\\simhei.ttf",
        "C:\\Windows\\Fonts\\simsun.ttc",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _draw_text_overlay(image: Image.Image, title: str, subtitle: str, template: CoverTemplate) -> Image.Image:
    canvas = image.convert("RGBA")
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    width, height = canvas.size
    draw.rounded_rectangle((48, height - 190, width - 48, height - 40), radius=28, fill=(0, 0, 0, 145))
    draw.rounded_rectangle((48, 42, 180, 84), radius=18, fill=template.accent_fill + (225,))
    draw.text((78, 55), "公众号草稿", font=_font(24, bold=True), fill=(255, 255, 255, 255))

    clean_title = normalize_whitespace(title)[:34]
    clean_subtitle = normalize_whitespace(subtitle)[:48]
    draw.text((70, height - 165), clean_title, font=_font(48, bold=True), fill=template.title_fill + (255,))
    if clean_subtitle:
        draw.text((72, height - 98), clean_subtitle, font=_font(24), fill=template.subtitle_fill + (240,))
    return Image.alpha_composite(canvas, overlay).convert("RGB")


def generate_cover(
    image_config: ImageGenerationConfig,
    title: str,
    output_path: Path,
    provider_name: str = "",
    template_name: str = "magazine",
    subtitle: str = "",
) -> Path:
    provider_name = (provider_name or image_config.provider or "doubao").strip().lower()
    template = TEMPLATES.get(template_name, TEMPLATES["magazine"])
    provider = _pick_provider(image_config, provider_name)
    prompt = (
        f"为微信公众号文章生成封面背景图，主题标题是《{normalize_whitespace(title)}》。"
        f"风格要求：{template.prompt_suffix}。不要在图中直接写任何文字。"
    )
    if provider_name == "qwen":
        image_bytes = _generate_with_qwen(provider, prompt, image_config.size)
    else:
        image_bytes = _generate_with_doubao(provider, prompt, image_config.size, image_config.quality)

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((900, 383))
    image = _draw_text_overlay(image, title, subtitle, template)
    ensure_dir(output_path.parent)
    image.save(output_path, "JPEG", quality=92)
    return output_path
