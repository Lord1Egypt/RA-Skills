from __future__ import annotations

import json
import os
import subprocess
from typing import Any


DEFAULT_CONFIG_PATH = "/Users/ailor/.openclaw/workspace/config/mcporter.json"


class XHSClient:
    def __init__(self, server_name: str = "xiaohongshu-mcp", config_path: str | None = None) -> None:
        self.server_name = server_name
        self.config_path = config_path or os.environ.get("MCPORTER_CONFIG_PATH", DEFAULT_CONFIG_PATH)

    def search_feeds(self, keyword: str) -> dict[str, Any]:
        return self._call_json_with_timeout(f'{self.server_name}.search_feeds(keyword: "{self._escape(keyword)}")', timeout_ms=45000)

    def get_feed_detail(self, feed_id: str, xsec_token: str, load_all_comments: bool = False, limit: int = 20) -> dict[str, Any]:
        expr = (
            f'{self.server_name}.get_feed_detail(feed_id: "{self._escape(feed_id)}", '
            f'xsec_token: "{self._escape(xsec_token)}", '
            f'load_all_comments: {str(load_all_comments).lower()}, limit: {int(limit)})'
        )
        return self._call_json_with_timeout(expr, timeout_ms=60000)

    def publish_content(self, title: str, content: str, images: list[str]) -> str:
        image_literals = ", ".join(f'"{self._escape(path)}"' for path in images)
        expr = (
            f'{self.server_name}.publish_content('
            f'content: "{self._escape(content)}", '
            f'images: [{image_literals}], '
            f'title: "{self._escape(title)}")'
        )
        return self._call_text(expr, timeout_ms=240000)

    def check_login_status(self) -> str:
        return self._call_text(f'{self.server_name}.check_login_status()')

    def _call_json(self, expr: str) -> dict[str, Any]:
        return json.loads(self._run(expr))

    def _call_json_with_timeout(self, expr: str, timeout_ms: int) -> dict[str, Any]:
        return json.loads(self._run(expr, timeout_ms=timeout_ms))

    def _call_text(self, expr: str, timeout_ms: int = 180000) -> str:
        return self._run(expr, timeout_ms=timeout_ms)

    def _run(self, expr: str, timeout_ms: int = 180000) -> str:
        command = ["mcporter", "call", "--config", self.config_path, "--timeout", str(timeout_ms), expr]
        completed = subprocess.run(command, capture_output=True, text=True)
        if completed.returncode != 0:
            raise RuntimeError(
                f"mcporter call failed: expr={expr}\nstdout={completed.stdout.strip()}\nstderr={completed.stderr.strip()}"
            )
        stdout = completed.stdout.strip()
        return stdout or completed.stderr.strip()

    @staticmethod
    def _escape(value: str) -> str:
        return value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
