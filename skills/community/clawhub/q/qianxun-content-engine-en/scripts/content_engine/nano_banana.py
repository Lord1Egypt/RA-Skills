"""Nano Banana 图片生成 wrapper（通过 Ofox endpoint）。

Ofox 把"Nano Banana Pro"作为模型名包装了 google/gemini-3-pro-image-preview，
endpoint 是 OpenAI compat 风格的 /v1/images/generations。

设计原则：
- 沿用 v1 同款多源 token 解析（复用 llm.py 的 _load_ofox_key）
- 流式 / 大小限制（沿用 v2 的 video.py 模式）
- 不直接把图丢内存——base64 解出立刻写文件
"""

from __future__ import annotations
import base64
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from .llm import OfoxError, _load_ofox_key, OFOX_BASE_URL

# Ofox 上的 Nano Banana Pro 模型名
DEFAULT_IMAGE_MODEL = "google/gemini-3-pro-image-preview"
DEFAULT_TIMEOUT = 180  # 出图慢，180s 够稳
DEFAULT_SIZE = "1024x1792"  # XHS 竖版默认（接近 9:16）


def generate_image(
    prompt: str,
    out_path: Path,
    size: str = DEFAULT_SIZE,
    model: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> Path:
    """生成 1 张图，base64 解码后写入 out_path。

    Args:
        prompt: 完整 image prompt（含品牌一致性 / 拆解卡 layout / 我方产品描述）
        out_path: 输出文件路径（.png）
        size: WxH，默认 1024x1792（XHS 竖版）
        model: Ofox 上的模型名，默认 google/gemini-3-pro-image-preview
        api_key: 覆盖默认 token
        base_url: 覆盖默认 endpoint
        timeout: 整体超时（秒）

    Returns:
        out_path 的绝对路径

    Raises:
        OfoxError: API 错误 / 解析失败
    """
    api_key = api_key or _load_ofox_key()
    if not api_key:
        raise OfoxError("OFOX_API_KEY 未配置（生图必需）")

    base_url = (base_url or os.environ.get("OFOX_BASE_URL") or OFOX_BASE_URL).rstrip("/")
    model = model or os.environ.get("OFOX_IMAGE_MODEL") or DEFAULT_IMAGE_MODEL

    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "size": size,
        "response_format": "b64_json",
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url}/v1/images/generations",
        data=payload,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")[:500]
        raise OfoxError(
            f"HTTP {e.code} from /v1/images/generations: {err_body}",
            status=e.code,
        ) from e
    except urllib.error.URLError as e:
        raise OfoxError(f"Network error: {e}") from e
    except json.JSONDecodeError as e:
        raise OfoxError(f"Invalid JSON response: {e}") from e

    imgs = data.get("data", [])
    if not imgs or not imgs[0].get("b64_json"):
        raise OfoxError(f"No image in response: {json.dumps(data)[:300]}")

    img_bytes = base64.b64decode(imgs[0]["b64_json"])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(img_bytes)
    return out_path.absolute()


def build_prompt(
    layout_description: str,
    brand_anchors: str = "",
    product_description: str = "",
    negative: str = "",
    is_cover: bool = False,
    cover_text: str = "",
) -> str:
    """组装"三路约束"的图片 prompt。

    Args:
        layout_description: 来自拆解卡 §4「参考内容拆解」的画面描述
                            （决策 #3 的"路 1：layout reference from deconstruction"）
        brand_anchors: 来自 graph/brand/brand-voice 的视觉关键词
                       （路 2：brand style anchors）
        product_description: 我方产品图描述 + 我方产品卖点
                             （路 3：product visual reference — 文本形式，
                              v2.0 不做 image-to-image）
        negative: 排除项（来自 brand-voice 慎用词 + graph/engine/taboo）
        is_cover: 是否封面图（封面允许大字层；frame 严格无文字）
        cover_text: 封面大字的目标内容（仅 is_cover=True 用）

    Returns:
        组装好的完整 prompt 字符串
    """
    parts = []

    # ─── 关键开头：方向 + 单图约束 ───
    # 必须在 prompt 最前面，避免被后面 layout 描述覆盖
    parts.append("CRITICAL FORMAT REQUIREMENTS (must follow):")
    parts.append("- STRICTLY VERTICAL orientation, portrait 9:16 ratio (1024x1792)")
    parts.append("- ONE SINGLE photograph, one continuous frame, ONE subject only")
    parts.append("- NO collage, NO grid, NO multi-panel layout, NO photo-stack")
    parts.append("- NO split-screen, NO side-by-side comparison, NO multiple angles compiled")
    parts.append("- NO product showcase compilation, NO 'magazine catalog spread' style")
    parts.append("- The output is ONE photograph of ONE moment / ONE composition")
    parts.append("")

    if layout_description:
        parts.append("VISUAL DESCRIPTION (single image, follow this exactly):")
        # 清理掉容易误导成"拼图"的结构性词汇
        cleaned = _strip_collage_keywords(layout_description.strip())
        parts.append(cleaned)
        parts.append("")

    if brand_anchors:
        parts.append("BRAND STYLE ANCHORS:")
        parts.append(brand_anchors.strip())
        parts.append("")

    if product_description:
        parts.append("PRODUCT TO DEPICT:")
        parts.append(product_description.strip())
        parts.append("")

    parts.append("STYLE DIRECTIVES:")
    parts.append("- Cinematic still photography, magazine editorial quality")
    parts.append("- Soft natural light, premium feel, restrained palette")
    parts.append("- No watermarks, no logos")

    if is_cover and cover_text:
        # 封面允许文字大字层
        parts.append(f"- Include large overlay text reading: \"{cover_text.strip()}\"")
        parts.append("  (text positioned at upper-center or lower-center, "
                     "elegant Chinese typography, color matches scene)")
    else:
        # 普通 frame 严格禁文字
        parts.append("- ABSOLUTELY NO text, NO captions, NO Chinese characters in image")

    if negative:
        parts.append("")
        parts.append("AVOID:")
        parts.append(negative.strip())
    else:
        parts.append("")
        parts.append("AVOID: cheap saturated colors, vibrant highlights, busy composition, "
                     "casual smartphone-snapshot quality, generic AI-aesthetic, "
                     "stock photo feel, distorted hands or faces, "
                     "horizontal landscape orientation, multi-image collage, "
                     "panel layout, grid view, side-by-side comparison, "
                     "photo collection compiled together, multi-angle composite, "
                     "magazine catalog spread, product showcase array, "
                     "split frame, multiple subjects in separate panels")

    return "\n".join(parts)


# ─── 辅助：去掉"图 N"/"图组"等容易误导成拼图的结构性词汇 ───

import re as _re

# 整行清理（markdown H2 标题如 "## 图 1｜封面..."）
_COLLAGE_LINE = _re.compile(r"^#{1,3}\s*图\s*\d+[^\n]*$", _re.MULTILINE)
# 行内清理（仅"图 N"或"图 N｜"短形式 + 集合性 layout 词汇）
_COLLAGE_INLINE = _re.compile(
    r"图\s*\d+\s*[｜|]?(?![一-鿿的张图])|"   # "图 1" / "图 1｜"，但不吃"图样"等
    r"图组|整组叙事(?:逻辑)?|多图|拼图|对比图|"
    r"第\s*[\d一二三四五六七八九]+\s*张?\s*图|"
    r"image\s+\d+|grid layout|collage|multi-?panel|"
    # 集合性 layout 关键词（针对 frame_001 拼图 issue）
    r"两件并排|并列悬挂|三件同框|两件一起|多件并排|"
    r"对比展示|对照展示|侧对比|"
    r"作为(?:整组|本组)?\s*(?:目录|整体|总览)|"
    r"整组(?:目录|总览|结构)"
)


def _strip_collage_keywords(text: str) -> str:
    """从 layout 描述里移除容易让模型理解成"拼图"的结构性词汇。

    保留实际画面描述，只删结构性词汇。
    """
    # 先删整行 markdown 标题
    cleaned = _COLLAGE_LINE.sub("", text)
    # 再删行内短词
    cleaned = _COLLAGE_INLINE.sub("", cleaned)
    # 折叠多空白
    cleaned = _re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = _re.sub(r" {2,}", " ", cleaned)
    return cleaned.strip()
