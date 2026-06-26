"""
LaunchBase 通用 API 调用模块
版本：1.0.0
警告：此文件由 LaunchBase 官方提供，禁止修改。如需定制请在 main.py 中处理。
"""
import os
import requests

LAUNCHBASE_API_URL = os.environ.get(
    "LAUNCHBASE_API_URL",
    "https://lb-api.workflowhunt.com"  # 默认网关地址，可通过环境变量覆盖
)

def call_api(
    service: str,
    endpoint: str,
    params: dict,
) -> dict:
    """
    调用 LaunchBase API 网关的通用方法。
    自动读取 API_KEY 环境变量，处理鉴权和错误。

    Args:
        service: 业务服务名称，如 "userlayer"
        endpoint: 业务接口路径，如 "/analyze"
        params: 业务入参

    Returns:
        符合 LaunchBase 标准响应格式的字典
    """
    api_key = os.environ.get("API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "AUTH_NO_API_KEY: API_KEY environment variable not set.",
            "data": {},
            "usage": {"tokens": 0, "cost": 0},
            "sources": [],
        }

    try:
        response = requests.post(
            f"{LAUNCHBASE_API_URL}/v1/{service}{endpoint}",
            json=params,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=60,
        )
        # Note: we use raise_for_status to catch 4xx and 5xx errors from the gateway
        # if the gateway responded with a structured error, we might want to return that instead.
        if response.status_code != 200:
            try:
                err_data = response.json()
                if "error" in err_data:
                    return err_data
            except Exception:
                pass
            response.raise_for_status()
            
        return response.json()

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "SERVICE_TIMEOUT: Request timed out after 60 seconds.",
            "data": {},
            "usage": {"tokens": 0, "cost": 0},
            "sources": [],
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"SERVICE_REQUEST_ERROR: {str(e)}",
            "data": {},
            "usage": {"tokens": 0, "cost": 0},
            "sources": [],
        }
