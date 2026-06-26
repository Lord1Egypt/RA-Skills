#!/usr/bin/env python3
"""
UCTOO API Client Script
提供与 uctoo 后端 API 交互的功能
"""

import sys
import json
import requests
from typing import Optional, Dict, Any

BACKEND_URL = "https://javatoarktsapi.uctoo.com"


def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    token: Optional[str] = None
) -> str:
    """
    发送 HTTP 请求到 uctoo 后端 API
    
    参数:
        method: HTTP 方法 (GET, POST)
        endpoint: API 端点
        data: JSON 请求体
        token: 认证令牌
    
    返回:
        JSON 格式的响应字符串
    """
    url = f"{BACKEND_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=data)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            return json.dumps({"error": f"Unsupported method: {method}"})
        
        return response.text
    except Exception as e:
        return json.dumps({"error": str(e)})


def main():
    """
    命令行入口
    
    用法: python api_client.py <method> <endpoint> [data_json] [token]
    """
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python api_client.py <method> <endpoint> [data_json] [token]"}))
        sys.exit(1)
    
    method = sys.argv[1]
    endpoint = sys.argv[2]
    data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    token = sys.argv[4] if len(sys.argv) > 4 else None
    
    result = make_request(method, endpoint, data, token)
    print(result)


if __name__ == "__main__":
    main()
