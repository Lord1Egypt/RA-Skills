#!/usr/bin/env python3
"""Tomoviee AI - Text-to-Music API client."""

import base64
import json
import time
from typing import Any, Dict, Optional

import requests


class TomovieeText2MusicClient:
    """Text-to-Music API client for Tomoviee AI."""

    BASE_URL = "https://openapi.wondershare.cc/v1/open/capacity/application"
    RESULT_ENDPOINT = "https://openapi.wondershare.cc/v1/open/pub/task"
    ENDPOINT = "tm_text2music"
    REQUEST_TIMEOUT = 60

    def __init__(self, app_key: str, app_secret: str):
        self.app_key = app_key
        self.access_token = self._generate_token(app_key, app_secret)

    def _generate_token(self, app_key: str, app_secret: str) -> str:
        credentials = f"{app_key}:{app_secret}"
        return base64.b64encode(credentials.encode()).decode()

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-App-Key": self.app_key,
            "Authorization": f"Basic {self.access_token}",
        }

    def _safe_json(self, response: requests.Response) -> Dict[str, Any]:
        try:
            return response.json()
        except ValueError as exc:
            raise Exception(f"Invalid JSON response: {response.text}") from exc

    def _make_request(self, payload: Dict[str, Any]) -> str:
        url = f"{self.BASE_URL}/{self.ENDPOINT}"
        response = requests.post(
            url,
            headers=self._get_headers(),
            json=payload,
            timeout=self.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        result = self._safe_json(response)

        if result.get("code") != 0:
            raise Exception(f"API Error: {result.get('msg', 'Unknown error')}")

        task_id = result.get("data", {}).get("task_id")
        if not task_id:
            raise Exception(f"Missing task_id in response: {result}")
        return task_id

    def text_to_music(
        self,
        prompt: str,
        duration: int,
        qty: int,
        disable_translate: Optional[bool] = None,
        callback: Optional[str] = None,
        params: Optional[str] = None,
    ) -> str:
        """Create a text-to-music task and return task_id."""
        if duration < 0 or duration > 95:
            raise ValueError("duration must be in range 0..95")
        if qty < 1 or qty > 4:
            raise ValueError("qty must be in range 1..4")

        payload: Dict[str, Any] = {
            "prompt": prompt,
            "duration": duration,
            "qty": qty,
        }
        if disable_translate is not None:
            payload["disable_translate"] = disable_translate
        if callback:
            payload["callback"] = callback
        if params:
            payload["params"] = params

        return self._make_request(payload)

    def get_result(self, task_id: str) -> Dict[str, Any]:
        response = requests.post(
            self.RESULT_ENDPOINT,
            headers=self._get_headers(),
            json={"task_id": task_id},
            timeout=self.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        result = self._safe_json(response)

        if result.get("code") != 0 and not result.get("data"):
            raise Exception(f"API Error: {result.get('msg', 'Unknown error')}")

        data = result.get("data")
        if not data:
            raise Exception(f"Missing task data in response: {result}")
        return data

    def poll_until_complete(
        self,
        task_id: str,
        poll_interval: int = 10,
        timeout: int = 600,
    ) -> Dict[str, Any]:
        elapsed = 0
        while elapsed < timeout:
            result = self.get_result(task_id)
            status = result.get("status")

            if status == 3:
                return result
            if status in [4, 5, 6]:
                raise Exception(f"Task failed: {result.get('reason', 'Unknown error')}")

            time.sleep(poll_interval)
            elapsed += poll_interval

        raise TimeoutError(f"Task did not complete within {timeout} seconds")


# Backward-compatible alias
TomovieeClient = TomovieeText2MusicClient


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 6:
        print(
            "Usage: python scripts/tomoviee_text2music_client.py "
            "<app_key> <app_secret> <prompt> <duration> <qty> [disable_translate]"
        )
        sys.exit(1)

    app_key = sys.argv[1]
    app_secret = sys.argv[2]
    prompt = sys.argv[3]
    duration = int(sys.argv[4])
    qty = int(sys.argv[5])
    disable_translate = None
    if len(sys.argv) > 6:
        disable_translate = sys.argv[6].strip().lower() in ("1", "true", "yes", "y")

    client = TomovieeText2MusicClient(app_key, app_secret)

    try:
        print("Creating text-to-music task...")
        task_id = client.text_to_music(
            prompt=prompt,
            duration=duration,
            qty=qty,
            disable_translate=disable_translate,
        )
        print(f"Task created: {task_id}")
        print("Polling for result...")

        result = client.poll_until_complete(task_id)

        print("\nTask completed")
        print(f"Progress: {result.get('progress', 'N/A')}%")

        result_data = json.loads(result["result"])
        print(json.dumps(result_data, indent=2, ensure_ascii=False))

    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)
