#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Westmoon QR-code generation client.
"""

import base64
import os
import platform
import subprocess
import time
from pathlib import Path
from typing import Dict, Optional, Tuple
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import requests


class QRCodeClient:
    def __init__(
        self,
        base_url: str,
        generate_endpoint: str,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.generate_endpoint = generate_endpoint
        self.session = session or requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                ),
                "Accept": "application/json, text/plain, */*",
            }
        )

    def generate_qr_code(self, params: Dict[str, str]) -> Tuple[bool, Optional[Dict], Optional[str]]:
        url = self._build_url(params)
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            result = response.json()
            if result.get("code") != 0 or not result.get("data"):
                return False, result, url
            return True, result, url
        except requests.RequestException as exc:
            return False, {"error": str(exc)}, url

    def decode_wxacode(self, data_uri: str) -> Tuple[bool, Optional[bytes], Optional[str]]:
        if not data_uri or "," not in data_uri:
            return False, None, None
        header, encoded = data_uri.split(",", 1)
        image_format = "png"
        if ";" in header and "/" in header:
            image_format = header.split("/")[1].split(";")[0].strip()
        try:
            return True, base64.b64decode(encoded), image_format
        except Exception:
            return False, None, image_format

    def save_qr_image(
        self, image_bytes: bytes, image_format: str = "png", output_path: Optional[str] = None
    ) -> Optional[str]:
        try:
            if output_path:
                file_path = Path(output_path)
            else:
                save_dir = Path.home() / ".westmoon-user-login" / "qr_codes"
                save_dir.mkdir(parents=True, exist_ok=True)
                file_path = save_dir / f"login_qr_{int(time.time())}.{image_format}"
            with file_path.open("wb") as handle:
                handle.write(image_bytes)
            return str(file_path)
        except Exception as exc:
            print(f"[QRCodeClient] 保存二维码失败: {exc}")
            return None

    def open_qr_image(self, file_path: str) -> bool:
        try:
            system = platform.system()
            if system == "Darwin":
                subprocess.run(["open", file_path], check=True)
            elif system == "Linux":
                subprocess.run(["xdg-open", file_path], check=True)
            elif system == "Windows":
                os.startfile(file_path)
            else:
                return False
            return True
        except Exception as exc:
            print(f"[QRCodeClient] 打开二维码失败: {exc}")
            return False

    def cleanup_qr_files(self) -> None:
        qr_dir = Path.home() / ".westmoon-user-login" / "qr_codes"
        if not qr_dir.exists():
            return
        for file_path in qr_dir.iterdir():
            try:
                file_path.unlink()
            except Exception:
                pass

    def _build_url(self, params: Dict[str, str]) -> str:
        raw_url = f"{self.base_url}{self.generate_endpoint}"
        parsed = urlparse(raw_url)
        query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        query.update({key: value for key, value in params.items() if value is not None})
        return urlunparse(parsed._replace(query=urlencode(query)))
