#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any
import os
import struct

MIN_W = 220
MIN_H = 220
MIN_BYTES = 12 * 1024


@dataclass
class QualityResult:
    accept: bool
    score_delta: int
    reasons: list[str]
    width: Optional[int] = None
    height: Optional[int] = None
    bytes_size: Optional[int] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "accept": self.accept,
            "score_delta": self.score_delta,
            "reasons": self.reasons,
            "width": self.width,
            "height": self.height,
            "bytes_size": self.bytes_size,
        }


def url_quality_hints(url: str) -> QualityResult:
    low = url.lower()
    delta = 0
    reasons: list[str] = []
    if any(x in low for x in ["logo", "sprite", "icon", "common_ued"]):
        return QualityResult(False, -20, ["site-asset-url"])
    if any(x in low for x in ["thumb", "thumbnail"]):
        delta -= 2
        reasons.append("thumbnail-url")
    return QualityResult(True, delta, reasons)


def _png_size(head: bytes):
    if len(head) >= 24 and head[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", head[16:24])
    return None


def _gif_size(head: bytes):
    if len(head) >= 10 and (head[:6] == b"GIF87a" or head[:6] == b"GIF89a"):
        return struct.unpack("<HH", head[6:10])
    return None


def _jpeg_size(path: str):
    with open(path, "rb") as f:
        data = f.read(2)
        if data != b"\xff\xd8":
            return None
        while True:
            byte = f.read(1)
            if not byte:
                return None
            if byte != b"\xff":
                continue
            marker = f.read(1)
            while marker == b"\xff":
                marker = f.read(1)
            if marker in [bytes([m]) for m in [0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF]]:
                seg_len = struct.unpack(">H", f.read(2))[0]
                precision = f.read(1)
                h, w = struct.unpack(">HH", f.read(4))
                return (w, h)
            else:
                seg_len_bytes = f.read(2)
                if len(seg_len_bytes) != 2:
                    return None
                seg_len = struct.unpack(">H", seg_len_bytes)[0]
                f.seek(seg_len - 2, 1)


def _webp_size(head: bytes):
    if len(head) < 30 or head[:4] != b"RIFF" or head[8:12] != b"WEBP":
        return None
    chunk = head[12:16]
    if chunk == b"VP8X" and len(head) >= 30:
        w = 1 + int.from_bytes(head[24:27], "little")
        h = 1 + int.from_bytes(head[27:30], "little")
        return (w, h)
    return None


def image_size(path: str):
    with open(path, "rb") as f:
        head = f.read(64)
    for fn in (_png_size, _gif_size, _webp_size):
        size = fn(head)
        if size:
            return size
    return _jpeg_size(path)


def inspect_file(path: str, intent: str = "portrait") -> QualityResult:
    reasons: list[str] = []
    score_delta = 0
    try:
        width, height = image_size(path) or (None, None)
    except Exception:
        width, height = None, None
    if width is None or height is None:
        return QualityResult(False, -20, ["not-a-decodable-image"])

    try:
        size = os.path.getsize(path)
    except Exception:
        size = None

    if size is not None and size < MIN_BYTES:
        return QualityResult(False, -20, ["too-small-file"], width, height, size)
    if width < MIN_W or height < MIN_H:
        return QualityResult(False, -20, ["too-small-dimensions"], width, height, size)

    ratio = width / max(height, 1)
    if intent == "wallpaper":
        if max(width, height) < 800:
            score_delta -= 3
            reasons.append("small-for-wallpaper")
        if 0.85 <= ratio <= 1.15:
            score_delta -= 2
            reasons.append("square-for-wallpaper")
    elif intent == "avatar":
        if 0.85 <= ratio <= 1.15:
            score_delta += 1
            reasons.append("square-avatar-friendly")
    elif intent in {"portrait", "official"}:
        if max(width, height) >= 800:
            score_delta += 1
            reasons.append("good-resolution")
    elif intent == "meme":
        if size is not None and size < 25 * 1024:
            score_delta -= 1
            reasons.append("small-meme-file")

    return QualityResult(True, score_delta, reasons, width, height, size)
