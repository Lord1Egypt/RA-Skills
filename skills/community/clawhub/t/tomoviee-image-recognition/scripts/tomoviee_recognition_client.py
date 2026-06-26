#!/usr/bin/env python3
"""Tomoviee AI - recognition API client"""

import base64, json, time
from typing import Dict, Optional, Any
import requests

class TomovieeClient:
    BASE_URL = "https://openapi.wondershare.cc/v1/open/capacity/application"
    RESULT_ENDPOINT = "https://openapi.wondershare.cc/v1/open/pub/task"
    ENDPOINT = "tm_reference_img2mask"
    
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
            "Authorization": f"Basic {self.access_token}"
        }
    
    def _make_request(self, payload: Dict[str, Any]) -> str:
        url = f"{self.BASE_URL}/{self.ENDPOINT}"
        response = requests.post(url, headers=self._get_headers(), json=payload)
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"API Error: {result.get('msg')}")
        return result["data"]["task_id"]
    
    def get_result(self, task_id: str) -> Dict[str, Any]:
        response = requests.post(self.RESULT_ENDPOINT, headers=self._get_headers(), json={"task_id": task_id})
        result = response.json()
        if result.get("code") != 0 and not result.get("data"):
            raise Exception(f"API Error: {result.get('msg')}")
        return result["data"]
    
    def poll_until_complete(self, task_id: str, poll_interval: int = 10, timeout: int = 600) -> Dict[str, Any]:
        elapsed = 0
        while elapsed < timeout:
            result = self.get_result(task_id)
            if result["status"] == 3:
                return result
            elif result["status"] in [4, 5, 6]:
                raise Exception(f"Task failed: {result.get('reason')}")
            time.sleep(poll_interval)
            elapsed += poll_interval
        raise TimeoutError(f"Task did not complete within {timeout} seconds")
