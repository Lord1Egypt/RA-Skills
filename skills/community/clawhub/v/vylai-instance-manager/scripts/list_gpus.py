#!/usr/bin/env python3
"""获取无阶未来平台GPU资源列表"""

import argparse
import json
import os
import sys

import requests


SKILL_ID = "7641796136130461732"
API_BASE_URL = "https://api.vylai.com"


def get_api_token():
    """从环境变量获取API Token"""
    # 优先使用标准环境变量
    token = os.getenv("VYLAI_API_TOKEN")
    if token:
        return token
    # 兼容 Coze 平台格式
    token = os.getenv("COZE_VYLAI_API_7641796136130461732")
    if token:
        return token
    raise ValueError("缺少API Token凭证，请设置环境变量 VYLAI_API_TOKEN（获取地址：https://vylai.com/console/api）")


def list_gpus():
    """
    获取平台所有GPU资源列表
    
    Returns:
        dict: API响应结果，包含GPU资源信息
    """
    url = f"{API_BASE_URL}/market/allgpus"
    headers = {
        "X-Auth-Token": get_api_token()
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code >= 400:
            return {
                "success": False,
                "error": f"HTTP请求失败: {response.status_code}",
                "details": response.text
            }
        
        result = response.json()
        
        if result.get("code") == 200:
            data = result.get("data", {})
            return {
                "success": True,
                "gpu_types": data.get("toptype_dict", {}),
                "gpu_dict": data.get("gpu_dict", {}),
                "total": data.get("total", 0),
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


def format_gpu_types(gpu_types):
    """格式化GPU类型信息为易读格式"""
    formatted = []
    for gpu_id, info in gpu_types.items():
        formatted.append({
            "gpu_id": gpu_id,
            "name": info.get("name"),
            "tflops": info.get("tflops"),
            "memory_gb": info.get("mem"),
            "price_per_hour": info.get("price_per_hour"),
            "price_per_day": info.get("price_per_day"),
            "available_gpu_nums": info.get("availableGpu", [])
        })
    return formatted


def main():
    parser = argparse.ArgumentParser(description="获取无阶未来平台GPU资源列表")
    parser.add_argument("--format", choices=["detailed", "simple"], default="simple",
                        help="输出格式：detailed=完整信息，simple=简化信息")
    
    args = parser.parse_args()
    
    result = list_gpus()
    
    if result.get("success") and args.format == "simple":
        # 简化输出，只显示GPU类型信息
        gpu_types = result.get("gpu_types", {})
        result["gpu_types"] = format_gpu_types(gpu_types)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
