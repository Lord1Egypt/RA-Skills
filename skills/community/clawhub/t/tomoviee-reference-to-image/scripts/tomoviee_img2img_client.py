#!/usr/bin/env python3
"""Tomoviee AI - Image-to-Image API client."""

import base64
import json
import time
from typing import Any, Dict, Optional

import requests


class TomovieeImg2ImgClient:
    """Image-to-Image API client for Tomoviee AI."""

    BASE_URL = "https://openapi.wondershare.cc/v1/open/capacity/application"
    RESULT_ENDPOINT = "https://openapi.wondershare.cc/v1/open/pub/task"
    ENDPOINT = "tm_reference_img2img"
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

    def image_to_image(
        self,
        prompt: str,
        reference_image: Optional[str] = None,
        control_type: str = "2",
        init_image: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
        batch_size: int = 1,
        control_intensity: float = 0.5,
        callback: Optional[str] = None,
        params: Optional[str] = None,
        image: Optional[str] = None,
        image_num: Optional[int] = None,
    ) -> str:
        """Create an image-to-image task and return task_id.

        Backward compatibility:
        - `image` is treated as `reference_image`.
        - `image_num` is treated as `batch_size`.
        """
        ref = reference_image or image
        if not ref:
            raise ValueError("reference_image is required")

        if image_num is not None:
            batch_size = image_num

        if width < 512 or width > 2048:
            raise ValueError("width must be in range 512..2048")
        if height < 512 or height > 2048:
            raise ValueError("height must be in range 512..2048")
        if batch_size < 1 or batch_size > 4:
            raise ValueError("batch_size must be in range 1..4")
        if control_intensity < 0 or control_intensity > 1:
            raise ValueError("control_intensity must be in range 0..1")

        ct = str(control_type)
        if ct not in {"0", "1", "2", "3"}:
            raise ValueError("control_type must be one of: 0, 1, 2, 3")

        payload: Dict[str, Any] = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "batch_size": batch_size,
            "control_intensity": control_intensity,
            "control_type": ct,
            "reference_image": ref,
        }

        if ct == "2":
            payload["init_image"] = init_image or ref
        elif init_image:
            payload["init_image"] = init_image

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
TomovieeClient = TomovieeImg2ImgClient


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 5:
        print(
            "Usage: python scripts/tomoviee_img2img_client.py "
            "<app_key> <app_secret> <prompt> <reference_image_url> "
            "[control_type] [width] [height] [batch_size] [control_intensity] [init_image_url]"
        )
        sys.exit(1)

    app_key = sys.argv[1]
    app_secret = sys.argv[2]
    prompt = sys.argv[3]
    reference_image = sys.argv[4]
    control_type = sys.argv[5] if len(sys.argv) > 5 else "2"
    width = int(sys.argv[6]) if len(sys.argv) > 6 else 1024
    height = int(sys.argv[7]) if len(sys.argv) > 7 else 1024
    batch_size = int(sys.argv[8]) if len(sys.argv) > 8 else 1
    control_intensity = float(sys.argv[9]) if len(sys.argv) > 9 else 0.5
    init_image = sys.argv[10] if len(sys.argv) > 10 else None

    client = TomovieeImg2ImgClient(app_key, app_secret)

    try:
        print("Creating image-to-image task...")
        task_id = client.image_to_image(
            prompt=prompt,
            reference_image=reference_image,
            control_type=control_type,
            width=width,
            height=height,
            batch_size=batch_size,
            control_intensity=control_intensity,
            init_image=init_image,
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