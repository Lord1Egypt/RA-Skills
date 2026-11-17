"""
Virsical HTTP API 客户端。

提供带自动认证和重试的 HTTP 请求能力。
所有 API 调用通过此客户端发出，自动管理 token 刷新。
"""

import json
import time
import urllib.parse
from typing import Optional, Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from .config import get_config, VirsicalConfig
from .auth_manager import TokenManager


class VirsicalClient:
    """Virsical API 客户端。

    封装所有 HTTP 请求，自动处理：
    - Token 管理（加载、刷新）
    - 401 重试（刷新 token 后重试）
    - 请求超时
    """

    def __init__(self, config: Optional[VirsicalConfig] = None,
                 token_manager: Optional[TokenManager] = None):
        """初始化客户端。

        Args:
            config: 配置对象，默认使用全局配置
            token_manager: Token 管理器，默认创建新的
        """
        self.config = config or get_config()
        self.token_manager = token_manager or TokenManager(self.config)
        self.timeout = 30  # 默认 30 秒超时

    def _get_token(self) -> str:
        """获取有效的 access token，失败时抛出异常。"""
        token = self.token_manager.get_access_token()
        if not token:
            raise Exception(
                "Not authenticated. Please login first with: "
                "python -m scripts.auth_manager login"
            )
        return token

    def request(self, method: str, api_path: str,
                body: Optional[dict] = None,
                query: Optional[dict] = None,
                retry_on_401: bool = True) -> dict:
        """发送 API 请求。

        Args:
            method: HTTP 方法 (GET/POST/PUT)
            api_path: API 路径（如 /vsk/smt-meeting/ai/rooms/occupied）
            body: 请求体字典（JSON）
            query: Query 参数字典
            retry_on_401: 是否在 401 时重试

        Returns:
            API 响应数据（已解析的 JSON）

        Raises:
            Exception: 请求失败
        """
        # 构建完整 URL
        query_string = ""
        if query:
            # 过滤 None 值
            clean_query = {k: v for k, v in query.items() if v is not None}
            query_string = urllib.parse.urlencode(clean_query)

        url = f"{self.config.base_url}{api_path}"
        if query_string:
            url += f"?{query_string}"

        # 准备请求体
        body_bytes = None
        body_str = ""
        if body is not None:
            body_str = json.dumps(body, ensure_ascii=False)
            body_bytes = body_str.encode("utf-8")

        try:
            return self._do_request(method, url, api_path, query_string,
                                    body_bytes, body_str)
        except HTTPError as e:
            if e.code == 401 and retry_on_401:
                # 尝试刷新 token 并重试
                refreshed = self.token_manager._refresh()
                if refreshed:
                    return self._do_request(method, url, api_path, query_string,
                                            body_bytes, body_str)
                else:
                    self.token_manager.clear_token()
                    raise Exception("Token expired and refresh failed. Please login again.")
            elif e.code == 400:
                # 检查是否是签名错误
                try:
                    error_body = json.loads(e.read().decode())
                    error_code = error_body.get("code", "")
                    error_msg_code = error_body.get("msg", "")
                    # 有些微服务（如 cloud-oms）将错误码放在 msg 字段
                    if str(error_code) in ("101040", "101043") or str(error_msg_code) in ("101040", "101043"):
                        raise Exception(
                            f"Signature verification failed (code: {error_code or error_msg_code}). "
                            f"Please check system clock synchronization or SIGNATURE_KEY configuration."
                        )
                except json.JSONDecodeError:
                    pass
                raise Exception(f"Bad request: {e.code} - {e.reason}")
            else:
                raise Exception(f"HTTP error: {e.code} - {e.reason}")
        except URLError as e:
            raise Exception(f"Network error: {e.reason}")
        except Exception as e:
            raise Exception(f"Request failed: {e}")

    def _do_request(self, method: str, full_url: str, api_path: str,
                    query_string: str, body_bytes: Optional[bytes],
                    body_str: str) -> dict:
        """执行单次 HTTP 请求。"""
        token = self._get_token()

        # 设置标准头
        auth_headers = {"Authorization": f"Bearer {token}"}
        headers = {
            "Content-Type": "application/json",
            **auth_headers,
        }

        req = Request(full_url, data=body_bytes, headers=headers, method=method)

        with urlopen(req, timeout=self.timeout) as resp:
            response_data = json.loads(resp.read().decode())

        return response_data

    def get(self, api_path: str, query: Optional[dict] = None) -> dict:
        """发送 GET 请求。

        Args:
            api_path: API 路径
            query: Query 参数字典

        Returns:
            API 响应数据
        """
        return self.request("GET", api_path, query=query)

    def post(self, api_path: str, body: Optional[dict] = None,
             query: Optional[dict] = None) -> dict:
        """发送 POST 请求。

        Args:
            api_path: API 路径
            body: 请求体
            query: Query 参数

        Returns:
            API 响应数据
        """
        return self.request("POST", api_path, body=body, query=query)

    def put(self, api_path: str, body: Optional[dict] = None,
            query: Optional[dict] = None) -> dict:
        """发送 PUT 请求。

        Args:
            api_path: API 路径
            body: 请求体
            query: Query 参数

        Returns:
            API 响应数据
        """
        return self.request("PUT", api_path, body=body, query=query)


# 便捷函数：创建客户端实例
def get_client() -> VirsicalClient:
    """获取 VirsicalClient 实例。

    Returns:
        VirsicalClient 实例
    """
    return VirsicalClient()
