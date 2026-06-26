from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


def slugify(text: str) -> str:
    value = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", (text or "").strip().lower())
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "wechat-article"


def trim_utf8_bytes(text: str, max_bytes: int) -> str:
    raw = (text or "").encode("utf-8")
    if len(raw) <= max_bytes:
        return text or ""
    return raw[:max_bytes].decode("utf-8", errors="ignore")


def decode_escaped_unicode(text: str) -> str:
    if not text or "\\u" not in text:
        return text or ""
    if not re.search(r"\\u[0-9a-fA-F]{4}", text):
        return text
    try:
        return text.encode("utf-8").decode("unicode_escape")
    except Exception:
        return text


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def write_json(data: dict[str, Any]) -> None:
    payload = json.dumps(data, ensure_ascii=False)
    stream = sys.stdout
    try:
        stream.write(payload + "\n")
    except UnicodeEncodeError:
        stream.write(json.dumps(data, ensure_ascii=True) + "\n")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path
