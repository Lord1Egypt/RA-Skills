"""
影刀 RPA API Python 客户端
"""

import os
import time
import requests
from typing import Optional, List, Dict, Any

class YingdaoError(Exception):
    """影刀 API 异常基类"""
    pass

class TokenExpiredError(YingdaoError):
    """令牌过期异常"""
    pass

class YingdaoAPI:
    """影刀 RPA API 客户端"""

    # API 端点
    AUTH_ENDPOINT = "https://api.yingdao.com/oapi/token/v2/token/create"
    BUSINESS_ENDPOINT = "https://api.winrobot360.com/oapi"

    def __init__(self, access_key_id: Optional[str] = None, access_key_secret: Optional[str] = None):
        """
        初始化客户端

        Args:
            access_key_id: Access Key ID，为空时从环境变量 YINGDAO_ACCESS_KEY_ID 读取
            access_key_secret: Access Key Secret，为空时从环境变量 YINGDAO_ACCESS_KEY_SECRET 读取
        """
        self.access_key_id = access_key_id or os.getenv("YINGDAO_ACCESS_KEY_ID")
        self.access_key_secret = access_key_secret or os.getenv("YINGDAO_ACCESS_KEY_SECRET")
        self._access_token = None
        self._token_expire_time = 0

        if not self.access_key_id or not self.access_key_secret:
            raise YingdaoError("未配置 YINGDAO_ACCESS_KEY_ID 或 YINGDAO_ACCESS_KEY_SECRET")

    def _ensure_token(self) -> str:
        """确保 access_token 有效，自动刷新"""
        if self._access_token is None or time.time() >= self._token_expire_time:
            self._refresh_token()
        return self._access_token

    def _refresh_token(self):
        """刷新 access_token"""
        try:
            # 根据文档：鉴权接口使用 GET，参数在 query string
            params = {
                "accessKeyId": self.access_key_id,
                "accessKeySecret": self.access_key_secret
            }
            resp = requests.get(self.AUTH_ENDPOINT, params=params, timeout=30)

            resp.raise_for_status()
            data = resp.json()

            if data.get("code") != 200 or not data.get("success"):
                raise YingdaoError(f"鉴权失败: {data.get('msg', '未知错误')} (code={data.get('code')}, success={data.get('success')})")

            self._access_token = data["data"]["accessToken"]
            expires_in = data["data"]["expiresIn"]
            self._token_expire_time = time.time() + expires_in - 300  # 提前5分钟刷新

        except requests.RequestException as e:
            raise YingdaoError(f"网络错误: {e}")
        except (KeyError, ValueError) as e:
            raise YingdaoError(f"响应解析错误: {e}")

    def _business_request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """发送业务接口请求"""
        token = self._ensure_token()
        url = f"{self.BUSINESS_ENDPOINT}{path}"
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        headers["Content-Type"] = "application/json"

        try:
            resp = requests.request(method, url, headers=headers, timeout=60, **kwargs)
            resp.raise_for_status()
            data = resp.json()

            # 影刀返回格式：{"code": 200, "success": true, "data": {...}}
            if data.get("code") != 200 or not data.get("success"):
                msg = data.get("msg", "未知错误")
                if "token" in str(msg).lower() or "auth" in str(msg).lower():
                    raise TokenExpiredError(msg)
                raise YingdaoError(msg)

            return data.get("data", {})
        except requests.RequestException as e:
            raise YingdaoError(f"请求失败: {e}")

    def list_schedules(self, key: str = "", enabled: Optional[bool] = None, page: int = 1, size: int = 50) -> List[Dict[str, Any]]:
        """
        查询任务列表

        Args:
            key: 关键词，用于搜索任务名
            enabled: 是否仅查询启用的任务
            page: 页码
            size: 每页数量

        Returns:
            任务列表，每个任务包含 scheduleUuid, scheduleName 等字段
        """
        payload = {
            "key": key,
            "page": page,
            "size": size
        }
        if enabled is not None:
            payload["enabled"] = enabled

        result = self._business_request("POST", "/dispatch/v2/schedule/list", json=payload)
        return result  # data 直接就是任务列表

    def get_schedule_detail(self, schedule_uuid: str) -> Dict[str, Any]:
        """
        获取任务详情

        Args:
            schedule_uuid: 任务 UUID

        Returns:
            任务详情对象
        """
        result = self._business_request("POST", "/dispatch/v2/schedule/detail", json={
            "scheduleUuid": schedule_uuid
        })
        return result

    def get_task_records(self, schedule_uuid: str, cursor_direction: str = "next", size: int = 20, next_id: Optional[str] = None, pre_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取任务的执行记录

        Args:
            schedule_uuid: 任务 UUID
            cursor_direction: 分页方向，"next" 或 "pre"
            size: 每页数量
            next_id: 下一页的游标（用于 next）
            pre_id: 上一页的游标（用于 pre）

        Returns:
            执行记录列表（即接口返回的 dataList；分页信息 nextId/preId 未在此返回）
        """
        payload = {
            "sourceUuid": schedule_uuid,
            "cursorDirection": cursor_direction,
            "size": size
        }
        if next_id:
            payload["nextId"] = next_id
        if pre_id:
            payload["preId"] = pre_id

        result = self._business_request("POST", "/dispatch/v2/task/list", json=payload)
        return result.get("dataList", [])

    def get_today_records(self, schedule_uuid: str) -> List[Dict[str, Any]]:
        """
        获取任务今天的执行记录（简化版，返回近期记录）

        Args:
            schedule_uuid: 任务 UUID

        Returns:
            执行记录列表
        """
        # get_task_records 已返回 dataList，直接返回列表
        return self.get_task_records(schedule_uuid, size=100)

    def start_task(self, schedule_uuid: str, params: Optional[List[Dict[str, Any]]] = None, robot_uuid: Optional[str] = None) -> Optional[str]:
        """
        启动任务

        Args:
            schedule_uuid: 要启动的任务 UUID
            params: 任务参数列表，格式：[{"name": "param_name", "value": "value", "type": "str"}]
            robot_uuid: 指定执行机器人 UUID（可选）

        Returns:
            任务实例 UUID (taskUuid)，接口未返回时为 None
        """
        payload = {
            "scheduleUuid": schedule_uuid
        }
        if params:
            payload["scheduleRelaParams"] = [{
                "robotUuid": robot_uuid or "",
                "params": params
            }]

        result = self._business_request("POST", "/dispatch/v2/task/start", json=payload)
        return result.get("taskUuid")

    def query_task_result(self, task_uuid: str) -> Dict[str, Any]:
        """
        查询任务执行结果

        Args:
            task_uuid: 任务实例 UUID（由 start_task 返回）

        Returns:
            任务执行结果对象，包含 status, outputs 等字段
        """
        return self._business_request("POST", "/dispatch/v2/task/query", json={
            "taskUuid": task_uuid
        })

    def find_task_by_name(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        根据关键词查找任务

        Args:
            keyword: 任务名称关键词

        Returns:
            找到的第一个任务详情，未找到返回 None
        """
        tasks = self.list_schedules(key=keyword, size=50)
        for task in tasks:
            if keyword.lower() in task.get("scheduleName", "").lower():
                return task
        return None


# 便捷函数

def get_client() -> YingdaoAPI:
    """获取默认客户端（从环境变量读取凭证）"""
    return YingdaoAPI()

def list_tasks(keyword: str = "", enabled: bool = False) -> List[Dict[str, Any]]:
    """
    快速查询任务列表

    Args:
        keyword: 搜索关键词
        enabled: 是否仅查询启用的任务

    Returns:
        任务列表
    """
    client = get_client()
    return client.list_schedules(key=keyword, enabled=enabled)

def get_task_logs(task_name: str) -> List[Dict[str, Any]]:
    """
    获取指定任务的执行日志（近期记录，最多 100 条；当前接口不支持按日期筛选）

    Args:
        task_name: 任务名称（支持模糊匹配）

    Returns:
        执行记录列表
    """
    client = get_client()
    task = client.find_task_by_name(task_name)
    if not task:
        return []
    return client.get_today_records(task["scheduleUuid"])
