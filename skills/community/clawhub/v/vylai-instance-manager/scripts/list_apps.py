#!/usr/bin/env python3
"""获取无阶未来平台应用列表"""

import argparse
import json
import os
import sys

import requests


SKILL_ID = "7641796136130461732"
API_BASE_URL = "https://api.vylai.com"


def get_api_token():
    """从环境变量获取API Token（可选）"""
    # 优先使用标准环境变量
    token = os.getenv("VYLAI_API_TOKEN")
    if token:
        return token
    # 兼容 Coze 平台格式
    token = os.getenv("COZE_VYLAI_API_7641796136130461732")
    if token:
        return token
    return None


def list_apps(page=1, limit=20, search_string="", include_token=True):
    """
    获取平台应用列表
    
    说明：
    - 不带token：返回公开应用列表
    - 带token：返回公开应用 + 用户的私有应用
    
    Args:
        page: 页码，默认1
        limit: 每页数量，默认20
        search_string: 搜索关键词
        include_token: 是否使用token（默认True）
    
    Returns:
        dict: API响应结果，包含应用列表
    """
    url = f"{API_BASE_URL}/app/app"
    headers = {}
    
    if include_token:
        token = get_api_token()
        if token:
            headers["X-Auth-Token"] = token
    
    params = {
        "page": page,
        "limit": limit,
        "search_string": search_string
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code >= 400:
            return {
                "success": False,
                "error": f"HTTP请求失败: {response.status_code}",
                "details": response.text
            }
        
        result = response.json()
        
        if result.get("code") == 200:
            data = result.get("data", {})
            apps = data.get("list", [])
            
            # 格式化输出，只保留关键字段
            formatted_apps = []
            for app in apps:
                formatted_apps.append({
                    "id": app.get("id"),
                    "name": app.get("name"),
                    "description": app.get("image_description", "")[:100] if app.get("image_description") else "",
                    "owner": app.get("owner_name"),
                    "gpu_num": app.get("gpu_num"),
                    "price": app.get("price")
                })
            
            return {
                "success": True,
                "total": data.get("total", 0),
                "apps": formatted_apps,
                "message": "查询成功"
            }
        else:
            return {
                "success": False,
                "error": result.get("msg", "未知错误"),
                "code": result.get("code")
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"请求失败: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(description="获取无阶未来平台应用列表")
    parser.add_argument("--page", type=int, default=1, help="页码，默认1")
    parser.add_argument("--limit", type=int, default=20, help="每页数量，默认20")
    parser.add_argument("--search", default="", help="搜索关键词")
    parser.add_argument("--no-token", action="store_true", help="不使用token（仅获取公开应用）")
    
    args = parser.parse_args()
    
    result = list_apps(
        page=args.page,
        limit=args.limit,
        search_string=args.search,
        include_token=not args.no_token
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
