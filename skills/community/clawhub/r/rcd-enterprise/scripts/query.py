#!/usr/bin/env python3
"""
企业信息查询脚本
根据关键词和分类查询企业信息
"""

import argparse
import json
import os
import sys


# 导入特殊的 requests 模块
try:
    from coze_workload_identity import requests
except ImportError:
    import requests


API_URL = "https://rcd-test.dfwycredit.com/s1/skill/enterprise"


def query_enterprise(keyword: str, category: str = None, API_KEY: str = None):
    """
    调用企业信息查询接口

    Args:
        keyword: 企业名称关键词（必填）
        category: 企业分类（可选）
        API_KEY: API密钥（必填）

    Returns:
        dict: API 返回结果
    """
    # 构建请求参数，将 API_KEY 包含在 JSON body 中
    params = {
        "keyword": keyword,
        "API_KEY": API_KEY
    }
    
    if category:
        params["category"] = category

    try:
        response = requests.post(API_URL, json=params, timeout=10)
        response.raise_for_status()

        # 尝试解析 JSON 响应
        try:
            result = response.json()
        except ValueError:
            result = {
                "status": "error",
                "message": "Invalid JSON response",
                "data": response.text
            }

        return result

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "message": "Request timeout",
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Request failed: {str(e)}",
        }


def main():
    parser = argparse.ArgumentParser(description="企业信息查询")
    parser.add_argument("--keyword", required=True, help="企业名称关键词（必填）")
    parser.add_argument("--category", help="企业分类（可选）")
    parser.add_argument("--API_KEY", required=True, help="API密钥（必填）")

    args = parser.parse_args()

    # 执行查询
    result = query_enterprise(args.keyword, args.category, args.API_KEY)

    # 输出 JSON 结果
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 根据结果状态返回退出码
    if result.get("status") == "error":
        sys.exit(1)

    return 0


if __name__ == "__main__":
    main()
