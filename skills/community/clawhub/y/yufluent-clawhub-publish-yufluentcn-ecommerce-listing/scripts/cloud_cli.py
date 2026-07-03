"""ClawHub 薄客户端共用：读文件参数、打印 API 结果。"""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path
from typing import Any


def read_text_arg(value: str) -> str:
    """CLI 参数：若为现有文件路径则读文件，否则当作原文。"""
    raw = (value or "").strip()
    if not raw:
        return ""
    path = Path(raw)
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return raw


def encode_image_source(source: str) -> str:
    """本地路径 → data URI；http(s)/data: 原样返回（OpenClaw 云端 run 前编码）。"""
    raw = (source or "").strip()
    if not raw:
        raise ValueError("source_image is empty")
    if raw.startswith(("http://", "https://", "data:")):
        return raw
    path = Path(raw)
    if not path.is_file():
        raise ValueError(f"source_image file not found: {raw}")
    data = path.read_bytes()
    suffix = path.suffix.lower()
    if suffix == ".png":
        mime = "image/png"
    elif suffix == ".webp":
        mime = "image/webp"
    elif suffix in (".jpg", ".jpeg"):
        mime = "image/jpeg"
    else:
        mime = "image/jpeg"
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def print_skill_output(
    data: dict[str, Any],
    *,
    as_json: bool = False,
    prefer_formatted: bool = True,
) -> None:
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    text = ""
    if prefer_formatted:
        text = str(data.get("formatted_text") or "").strip()
    if not text:
        text = str(data.get("text") or "").strip()
    if not text:
        payload = data.get("data") or data.get("listing")
        if payload is not None:
            text = json.dumps(payload, ensure_ascii=False, indent=2)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


def print_run_meta(data: dict[str, Any], **extra: str) -> None:
    parts = [
        f"run_id={data.get('run_id')}",
        f"model={data.get('model_used')}",
    ]
    if data.get("total_tokens"):
        parts.append(f"tokens={data.get('total_tokens')}")
    for k, v in extra.items():
        if v:
            parts.append(f"{k}={v}")
    print(f"\n--- {' '.join(parts)} ---", file=sys.stderr)
