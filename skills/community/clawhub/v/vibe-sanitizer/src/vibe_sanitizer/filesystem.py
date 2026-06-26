from __future__ import annotations

from pathlib import Path


def is_binary_content(data: bytes) -> bool:
    return b"\x00" in data


def read_text_candidate(path: Path) -> str | None:
    data = path.read_bytes()
    if is_binary_content(data):
        return None
    return data.decode("utf-8", errors="replace")
