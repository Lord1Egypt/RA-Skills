from __future__ import annotations

import json
import urllib.request
from typing import Iterable, Optional


class Videomp3wordClient:
    def __init__(self, base_url: str, bearer_token: Optional[str] = None, timeout: int = 300):
        self.base_url = base_url.rstrip("/")
        self.bearer_token = bearer_token
        self.timeout = timeout

    def video_to_knowledge(
        self,
        media_url: str,
        outputs: Iterable[str],
        mode: str = "balanced",
        export_formats: Optional[Iterable[str]] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        payload = {
            "media_url": media_url,
            "outputs": list(outputs),
            "mode": mode,
            "export_formats": list(export_formats or ["json"]),
        }
        if metadata:
            payload["metadata"] = metadata

        request = urllib.request.Request(
            url=f"{self.base_url}/video_to_knowledge",
            data=json.dumps(payload).encode("utf-8"),
            headers=self._headers(),
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def _headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        return headers
