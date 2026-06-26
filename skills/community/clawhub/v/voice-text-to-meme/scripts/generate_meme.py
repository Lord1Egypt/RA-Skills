#!/usr/bin/env python3
import argparse
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Dict, Optional

import requests
from openai import OpenAI

DEFAULT_BASE_URL = os.getenv("MEME_MODEL_BASE_URL", "https://models.audiozen.cn/v1")
DEFAULT_MODEL = os.getenv("MEME_MODEL_NAME", "doubao-seedream-4-5-251128")
_DEFAULT_OUTPUT_ROOT = os.getenv("MEME_OUTPUT_DIR", "")
DEFAULT_OUTPUT_FORMAT = os.getenv("MEME_MODEL_OUTPUT_FORMAT", "jpeg")
DEFAULT_RESPONSE_FORMAT = os.getenv("MEME_MODEL_RESPONSE_FORMAT", "url")

TONE_MAP = [
    (r"(哈哈|笑死|太好笑|乐死|绝了)", "轻松搞笑"),
    (r"(无语|服了|会谢|离谱|真行|行吧)", "吐槽无语"),
    (r"(求求|帮帮|救命|完了|崩溃|裂开)", "委屈求助"),
    (r"(牛|稳了|拿下|赢了|爽)", "得意庆祝"),
    (r"(快点|赶紧|别忘了|记得|马上)", "提醒催促"),
]


def choose_source_text(original_text: str, polished_text: Optional[str]) -> str:
    polished = (polished_text or "").strip()
    original = (original_text or "").strip()
    if polished:
        return polished
    if original:
        return original
    raise ValueError("至少提供 original_text 或 polished_text 之一")


def infer_tone(text: str, manual_style: Optional[str]) -> str:
    if manual_style:
        return manual_style
    for pattern, tone in TONE_MAP:
        if re.search(pattern, text):
            return tone
    if text.endswith("?") or text.endswith("？"):
        return "轻松疑问"
    if len(text) <= 8:
        return "日常轻松"
    return "日常聊天"


def compress_caption(text: str) -> str:
    text = re.sub(r"[\s\n]+", "", text)
    text = re.sub(r"^(嗯+|啊+|那个+|就是+)", "", text)
    text = text.strip("，。！？!?,.")
    if len(text) <= 12:
        return text
    if "，" in text:
        text = text.split("，", 1)[0]
    if len(text) > 14:
        text = text[:14]
    return text


def build_template_caption(text: str) -> Dict[str, str]:
    text = re.sub(r"[\s\n]+", "", text).strip("，。！？!?,.")
    if len(text) <= 10:
        return {"single_caption": text}
    midpoint = min(max(len(text) // 2, 4), 10)
    return {
        "top_text": text[:midpoint],
        "bottom_text": text[midpoint: midpoint + 10],
    }


def build_prompt(text: str, tone: str, mode: str, size: str) -> str:
    caption = compress_caption(text)
    base = (
        "生成一张适合聊天发送的中文表情包图片，单主体，方图构图，背景简洁，主角表情夸张，信息一眼可懂，"
        "整体更像即时通讯里会发出去的梗图或贴纸，而不是海报或摄影大片。"
    )
    tone_map = {
        "轻松搞笑": "整体氛围轻松搞笑，夸张、有趣、带一点荒诞感。",
        "吐槽无语": "整体氛围吐槽、无语、翻白眼、略带阴阳怪气。",
        "委屈求助": "整体氛围委屈、可怜、求助感强，但仍适合聊天表情包。",
        "得意庆祝": "整体氛围得意、庆祝、扬眉吐气。",
        "提醒催促": "整体氛围提醒、催促、强调感强，动作指向明确。",
        "轻松疑问": "整体氛围疑惑、轻松、带一点问号感。",
        "日常轻松": "整体氛围轻松日常、可爱、适合聊天。",
        "日常聊天": "整体氛围自然、日常、适合即时通讯。",
    }
    style = tone_map.get(tone, tone_map["日常聊天"])
    if mode == "direct-text":
        return (
            f"{base}{style}"
            f"请直接在图里渲染清晰、短促、好读的中文大字，文案控制在很短的范围内：{caption}。"
            f"文字要像表情包常见排版，留白足够，不要塞满画面。目标尺寸：{size}。"
        )
    return (
        f"{base}{style}"
        "不要在图中渲染任何可见文字，但请预留适合后续叠字的空白区域。"
        f"目标尺寸：{size}。"
    )


def _normalize_output_format(value: str) -> str:
    value = (value or "jpeg").strip().lower()
    if value == "jepg":
        return "jpeg"
    if value not in {"jpeg", "jpg"}:
        return "jpeg"
    return "jpeg" if value == "jpg" else value


def _extension_for_format(value: str) -> str:
    fmt = _normalize_output_format(value)
    return ".jpg" if fmt == "jpeg" else f".{fmt}"


def _build_client() -> OpenAI:
    api_key = os.getenv("MEME_MODEL_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 MEME_MODEL_API_KEY 环境变量")
    return OpenAI(api_key=api_key, base_url=DEFAULT_BASE_URL)


def _call_image_api(prompt: str, size: str) -> dict:
    client = _build_client()
    output_format = _normalize_output_format(DEFAULT_OUTPUT_FORMAT)
    response = client.images.generate(
        model=DEFAULT_MODEL,
        prompt=prompt,
        size=size,
        output_format=output_format,
        response_format=DEFAULT_RESPONSE_FORMAT,
    )
    return response.model_dump()


def _download_image(url: str) -> bytes:
    image_resp = requests.get(url, timeout=120)
    image_resp.raise_for_status()
    return image_resp.content


def _extract_image_bytes(result: dict) -> bytes:
    data = result.get("data") or []
    if not data:
        raise RuntimeError("图片接口未返回 data")
    first = data[0]
    if first.get("url"):
        return _download_image(first["url"])
    if first.get("b64_json"):
        import base64
        return base64.b64decode(first["b64_json"])
    raise RuntimeError("当前返回既没有 url 也没有 b64_json")


def _default_output_root() -> Path:
    if _DEFAULT_OUTPUT_ROOT:
        return Path(_DEFAULT_OUTPUT_ROOT)
    cwd = Path.cwd() / "meme_outputs"
    return cwd


def _safe_output_path(mode: str, output_format: str) -> Path:
    suffix = "direct" if mode == "direct-text" else "template"
    ext = _extension_for_format(output_format)
    preferred = _default_output_root() / f"meme_{suffix}{ext}"
    try:
        preferred.parent.mkdir(parents=True, exist_ok=True)
        return preferred
    except OSError:
        fallback_dir = Path(tempfile.gettempdir()) / "meme_outputs"
        fallback_dir.mkdir(parents=True, exist_ok=True)
        return fallback_dir / f"meme_{suffix}{ext}"


def save_image_bytes(content: bytes, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(content)


def main() -> None:
    parser = argparse.ArgumentParser(description="根据语音文本生成单张表情包图片")
    parser.add_argument("--text", dest="original_text", default="", help="原始文本")
    parser.add_argument("--polished-text", default="", help="润色后文本，可选")
    parser.add_argument("--mode", choices=["direct-text", "template"], default="direct-text")
    parser.add_argument("--style", default="", help="手动指定风格，可选")
    parser.add_argument("--size", default="2K", help="图片尺寸，默认 2K")
    parser.add_argument("--output", default="", help="输出文件路径，默认自动生成 .jpg")
    args = parser.parse_args()

    source_text = choose_source_text(args.original_text, args.polished_text)
    tone = infer_tone(source_text, args.style or None)
    prompt = build_prompt(source_text, tone, args.mode, args.size)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = _safe_output_path(args.mode, DEFAULT_OUTPUT_FORMAT)

    result = _call_image_api(prompt, args.size)
    content = _extract_image_bytes(result)
    save_image_bytes(content, output_path)

    payload = {
        "source_text": source_text,
        "tone": tone,
        "mode": args.mode,
        "prompt": prompt,
        "image_path": str(output_path),
        "model": DEFAULT_MODEL,
        "base_url": DEFAULT_BASE_URL,
        "output_format": _normalize_output_format(DEFAULT_OUTPUT_FORMAT),
        "response_format": DEFAULT_RESPONSE_FORMAT,
    }
    if args.mode == "template":
        payload["caption_template"] = build_template_caption(source_text)
    else:
        payload["caption"] = compress_caption(source_text)

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
