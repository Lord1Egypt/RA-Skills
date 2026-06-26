"""
OpenClaw Task Runner Skill - API 客户端
"""

import os
import httpx
import uuid
import json
from typing import Optional
from datetime import datetime
from decimal import Decimal

from .config import SkillConfig


class TaskAPIError(Exception):
    """API错误"""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"API Error {code}: {message}")


class AvailableTask:
    """可接单任务"""

    def __init__(
        self,
        id: uuid.UUID,
        title: str,
        category: str,
        bounty: Decimal,
        deadline: datetime,
        created_at: datetime,
    ):
        self.id = id
        self.title = title
        self.category = category
        self.bounty = bounty
        self.deadline = deadline
        self.created_at = created_at


class TaskDetail:
    """任务详情"""

    def __init__(
        self,
        id: uuid.UUID,
        title: str,
        description: Optional[str],
        category: str,
        bounty: Decimal,
        deadline: datetime,
        status: str,
        visibility: str,
        creator_id: str,
        assigned_claw_id: Optional[str],
        started_at: Optional[datetime],
        finished_at: Optional[datetime],
        created_at: datetime,
        updated_at: Optional[datetime],
    ):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.bounty = bounty
        self.deadline = deadline
        self.status = status
        self.visibility = visibility
        self.creator_id = creator_id
        self.assigned_claw_id = assigned_claw_id
        self.started_at = started_at
        self.finished_at = finished_at
        self.created_at = created_at
        self.updated_at = updated_at


class TaskAPIClient:
    """任务系统API客户端"""

    def __init__(self, config: SkillConfig):
        self.config = config
        self.base_url = config.api_base_url.rstrip("/")
        self.api_key = config.api_key
        self.api_secret = config.api_secret

    def _make_url(self, path: str) -> str:
        """构建完整URL"""
        return f"{self.base_url}{self.config.api_prefix}{path}"

    def _get_headers(self) -> dict:
        """
        生成认证请求头

        Returns:
            请求头字典
        """
        headers = {
            "Content-Type": "application/json",
        }

        # API Key 和 Secret 认证
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        if self.api_secret:
            headers["X-API-Secret"] = self.api_secret

        return headers

    async def _request(
        self,
        method: str,
        path: str,
        params: dict = None,
        json_data: dict = None,
    ) -> dict:
        """发送认证请求"""
        url = self._make_url(path)
        headers = self._get_headers()

        async with httpx.AsyncClient() as client:
            if method.upper() == "GET":
                response = await client.get(url, params=params, headers=headers)
            elif method.upper() == "POST":
                response = await client.post(url, json=json_data, headers=headers)
            elif method.upper() == "PUT":
                response = await client.put(url, json=json_data, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

    async def get_available_tasks(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[AvailableTask], int]:
        """
        获取可接单任务列表

        Returns:
            (任务列表, 总数)
        """
        path = "/bots/tasks/available"
        params = {"page": page, "page_size": page_size}

        data = await self._request("GET", path, params=params)

        if data.get("code") != 0:
            raise TaskAPIError(data.get("code", -1), data.get("message", "Unknown error"))

        items_data = data["data"]["items"]
        total = data["data"]["total"]

        tasks = [
            AvailableTask(
                id=uuid.UUID(item["id"]),
                title=item["title"],
                category=item["category"],
                bounty=Decimal(str(item["bounty"])),
                deadline=datetime.fromisoformat(item["deadline"].replace("Z", "+00:00")),
                created_at=datetime.fromisoformat(item["created_at"].replace("Z", "+00:00")),
            )
            for item in items_data
        ]

        return tasks, total

    async def grab_task(self, task_id: uuid.UUID) -> bool:
        """
        尝试抢单

        Returns:
            True: 抢单成功
            False: 抢单失败(已被抢或不可抢)
        """
        path = f"/bots/tasks/{task_id}/grab"

        data = await self._request("POST", path)

        if data.get("code") == 0:
            return True

        # 抢单失败
        return False

    async def get_task_detail(self, task_id: uuid.UUID) -> Optional[TaskDetail]:
        """
        获取任务详情

        Returns:
            任务详情，如果不存在返回None
        """
        path = f"/bots/tasks/{task_id}"

        data = await self._request("GET", path)

        if data.get("code") != 0:
            return None

        item = data["data"]
        return TaskDetail(
            id=uuid.UUID(item["id"]),
            title=item["title"],
            description=item.get("description"),
            category=item["category"],
            bounty=Decimal(str(item["bounty"])),
            deadline=datetime.fromisoformat(item["deadline"].replace("Z", "+00:00")),
            status=item["status"],
            visibility=item["visibility"],
            creator_id=item["creator_id"],
            assigned_claw_id=item.get("assigned_claw_id"),
            started_at=(
                datetime.fromisoformat(item["started_at"].replace("Z", "+00:00"))
                if item.get("started_at")
                else None
            ),
            finished_at=(
                datetime.fromisoformat(item["finished_at"].replace("Z", "+00:00"))
                if item.get("finished_at")
                else None
            ),
            created_at=datetime.fromisoformat(item["created_at"].replace("Z", "+00:00")),
            updated_at=(
                datetime.fromisoformat(item["updated_at"].replace("Z", "+00:00"))
                if item.get("updated_at")
                else None
            ),
        )

    async def update_task_status(
        self, task_id: uuid.UUID, status: str
    ) -> bool:
        """
        更新任务状态

        Args:
            task_id: 任务ID
            status: 新状态 (in_progress/completed/cancelled)

        Returns:
            True: 更新成功
            False: 更新失败
        """
        path = f"/bots/tasks/{task_id}/status"
        payload = {"status": status}

        data = await self._request("PUT", path, json_data=payload)

        return data.get("code") == 0

    async def upload_deliverable(
        self,
        task_id: uuid.UUID,
        result_description: str,
        zip_file_path: str | None = None,
    ) -> dict:
        """
        上传任务交付物

        Args:
            task_id: 任务ID
            result_description: 任务结果描述/执行报告
            zip_file_path: ZIP包文件路径（可选）

        Returns:
            上传结果 {
                "result_zip_url": str,
                "result_description_url": str,
                "uploaded_at": datetime
            }
        """
        path = f"/bots/tasks/{task_id}/deliverable"
        url = self._make_url(path)

        headers = self._get_headers()
        headers.pop("Content-Type", None)  # multipart 需要 boundary

        async with httpx.AsyncClient() as client:
            data = {"result_description": result_description}

            if zip_file_path and os.path.exists(zip_file_path):
                zip_filename = os.path.basename(zip_file_path)
                with open(zip_file_path, "rb") as f:
                    zip_content = f.read()
                response = await client.post(
                    url,
                    data=data,
                    files={"zip_file": (zip_filename, zip_content, "application/zip")},
                    headers=headers,
                )
            else:
                response = await client.post(
                    url,
                    data=data,
                    files=None,
                    headers=headers,
                )

            response.raise_for_status()
            result = response.json()

            if result.get("code") != 0:
                raise TaskAPIError(
                    result.get("code", -1),
                    result.get("message", "Upload failed")
                )

            return result.get("data", {})
