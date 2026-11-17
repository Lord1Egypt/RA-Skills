"""Predictable output paths, collision handling, and immediate URL downloads."""

from __future__ import annotations

import base64
import binascii
import mimetypes
import re
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Any

from .errors import SkillError
from .http import ApiClient


def slugify(text: str, fallback: str = "result") -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return value[:48] or fallback


def media_extension(data: bytes, fallback: str = "bin") -> str:
    """Return an extension from common media signatures without trusting API metadata."""
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return fallback.lstrip(".") or "bin"


class OutputManager:
    def __init__(self, config: dict[str, Any], category: str, override: str = "") -> None:
        configured = override or str(config["output"].get("directory", "./showmeai-output"))
        root = Path(configured).expanduser()
        if not root.is_absolute():
            root = Path.cwd() / root
        self.directory = root / category
        self.directory.mkdir(parents=True, exist_ok=True)

    def path(self, stem: str, extension: str, filename: str = "") -> Path:
        extension = extension.lstrip(".") or "bin"
        if filename:
            supplied = Path(filename)
            if supplied.is_absolute() or supplied.name != filename or supplied.name in {"", ".", ".."}:
                raise SkillError("OUTPUT_FILENAME_INVALID", "Output filename must be a plain filename without directories.")
            candidate = self.directory / supplied.name
            if not candidate.suffix:
                candidate = candidate.with_suffix(f".{extension}")
        else:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            candidate = self.directory / f"{timestamp}-{slugify(stem)}.{extension}"
        if not candidate.exists():
            return candidate
        counter = 2
        while True:
            revised = candidate.with_name(f"{candidate.stem}-{counter}{candidate.suffix}")
            if not revised.exists():
                return revised
            counter += 1

    def write_base64(self, encoded: str, stem: str, extension: str, filename: str = "") -> Path:
        try:
            data = base64.b64decode(encoded, validate=True)
        except (ValueError, binascii.Error) as error:
            raise SkillError("OUTPUT_INVALID", "API returned invalid base64 media.") from error
        actual_extension = media_extension(data, extension)
        actual_filename = filename
        if filename and Path(filename).suffix.lower() != f".{actual_extension}":
            actual_filename = str(Path(filename).with_suffix(f".{actual_extension}"))
        path = self.path(stem, actual_extension, actual_filename)
        path.write_bytes(data)
        return path.resolve()

    def write_bytes(self, data: bytes, stem: str, extension: str, filename: str = "") -> Path:
        path = self.path(stem, extension, filename)
        path.write_bytes(data)
        return path.resolve()

    def download(self, client: ApiClient, url: str, stem: str, filename: str = "") -> Path:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            raise SkillError("OUTPUT_URL_INVALID", "Only HTTP(S) result URLs are accepted.")
        suffix = Path(parsed.path).suffix.lstrip(".")
        if not suffix:
            suffix = mimetypes.guess_extension("application/octet-stream", strict=False).lstrip(".") or "bin"
        raw, _headers = client.request("GET", url, timeout=300)
        return self.write_bytes(raw, stem, suffix, filename)
