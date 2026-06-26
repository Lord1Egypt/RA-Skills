"""HTTP API client wrapping all Sparki C-end API endpoints."""

from pathlib import Path
from typing import Any

import httpx


class SparkiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._headers = {"X-API-Key": api_key}

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    async def validate_key(self) -> bool:
        async with httpx.AsyncClient() as c:
            resp = await c.get(self._url("/api/v1/account/info"),
                               headers=self._headers)
            return resp.status_code == 200

    async def upload_asset(self, file_path: Path) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=300) as c:
            with open(file_path, "rb") as f:
                files = {"file": (file_path.name, f,
                                  f"video/{file_path.suffix.lstrip('.').lower()}")}
                resp = await c.post(self._url("/api/v1/assets/upload"),
                                    headers=self._headers, files=files)
            return resp.json()

    async def list_assets(self, page: int = 1, page_size: int = 20) -> dict[str, Any]:
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        async with httpx.AsyncClient() as c:
            resp = await c.get(self._url("/api/v1/assets/user_assets"),
                               headers=self._headers, params=params)
            return resp.json()

    async def get_asset_status(self, object_key: str) -> dict[str, Any]:
        page = 1
        page_size = 50
        while True:
            result = await self.list_assets(page=page, page_size=page_size)
            data = result.get("data", {})
            items = data.get("assets", data.get("items", []))
            for item in items:
                if item.get("object_key") == object_key or item.get("objectKey") == object_key:
                    return {"code": result.get("code"), "data": item}
            if len(items) < page_size:
                break
            page += 1
        return {"code": result.get("code"), "data": None}

    async def create_project(
        self,
        object_keys: list[str],
        tags: list[str],
        user_input: str = "",
        aspect_ratio: str = "9:16",
        agent_type: str | None = None,
        duration_range: str | None = None,
    ) -> dict[str, Any]:
        resources = [{"idx": i, "s3_object_key": key}
                     for i, key in enumerate(object_keys)]
        body: dict[str, Any] = {
            "resources": resources,
            "user_input": user_input,
            "generation_preferences": {"aspect_ratio": aspect_ratio},
            "send_after_create": True,
        }
        if tags:
            body["tags"] = tags
        if agent_type:
            body["agent_type"] = agent_type
        if duration_range:
            body["generation_preferences"]["duration_range"] = duration_range
        async with httpx.AsyncClient() as c:
            resp = await c.post(self._url("/api/v1/projects/"),
                                headers=self._headers, json=body)
            return resp.json()

    async def get_project_status(self, task_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as c:
            resp = await c.get(self._url(f"/api/v1/projects/task/{task_id}"),
                               headers=self._headers)
            return resp.json()

    async def download_result(self, url: str, output_path: Path) -> int:
        async with httpx.AsyncClient(timeout=600, follow_redirects=True) as c:
            async with c.stream("GET", url) as resp:
                resp.raise_for_status()
                output_path.parent.mkdir(parents=True, exist_ok=True)
                total = 0
                with open(output_path, "wb") as f:
                    async for chunk in resp.aiter_bytes(chunk_size=1024 * 1024):
                        f.write(chunk)
                        total += len(chunk)
                return total
