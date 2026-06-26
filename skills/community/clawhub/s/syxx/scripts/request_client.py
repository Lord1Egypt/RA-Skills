from typing import Any, Optional

import requests


class APIError(Exception):
    """接口业务错误：HTTP 200 但响应体中 error 非 0。"""

    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class RequestClient:
    """人人商城龙虾助手 API 请求客户端，基于 requests.Session 复用连接，支持 GET/POST/PUT/PATCH/DELETE。"""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30,
    ) -> None:
        if not base_url:
            raise ValueError("base_url 不能为空")
        if not api_key:
            raise ValueError("api_key 不能为空")

        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
        })

    def _build_url(self, path: str) -> str:
        base_url = self.base_url.rstrip("/")
        path = path.lstrip("/")
        return f"{base_url}/{path}"

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any] | list[Any]] = None,
        **kwargs: Any,
    ) -> dict[str, Any] | list[Any] | None:
        """
        统一请求封装：拼接 URL、超时、状态码校验、安全 JSON 解析，并校验业务错误码 error。
        后端以 error 字段表示业务状态：0 为成功，非 0 时抛出 APIError，错误信息在 message 字段。
        """
        url = self._build_url(path)
        response = self.session.request(
            method,
            url,
            params=params,
            data=data,
            json=json,
            timeout=self.timeout,
            **kwargs,
        )
        response.raise_for_status()

        if not response.content:
            return None
        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            return None
        try:
            data = response.json()
        except ValueError:
            return None

        if isinstance(data, dict) and data.get("error", 0) != 0:
            raise APIError(
                code=int(data.get("error", -1)),
                message=str(data.get("message", "未知错误")),
            )
        return data

    def get(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any] | list[Any] | None:
        """发送 GET 请求，返回 JSON 或 None。"""
        return self._request("GET", path, params=params)

    def post(
        self,
        path: str,
        data: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any] | list[Any] | None:
        """发送 POST 请求，参数以 form data 提交，返回 JSON 或 None。"""
        return self._request("POST", path, data=data)


_client: Optional[RequestClient] = None


def get_client(
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = 30,
) -> RequestClient:
    """
    获取全局 RequestClient 单例。
    首次调用时必须传入 base_url 和 api_key 以完成初始化；后续调用可省略参数直接复用。
    """
    global _client
    if _client is None:
        if not base_url or not api_key:
            raise ValueError("首次调用 get_client() 必须提供 base_url 和 api_key")
        _client = RequestClient(base_url, api_key, timeout)
    return _client
