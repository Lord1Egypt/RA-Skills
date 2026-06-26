#!/usr/bin/env python3
"""查询无阶未来GPU实例状态"""

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


def query_all_instances():
    """
    查询当前用户所有实例状态
    
    Returns:
        dict: API响应结果，包含实例列表
    """
    url = f"{API_BASE_URL}/api/v1/app/status"
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
            return {
                "success": True,
                "instances": result.get("data", {}).get("tasks", []),
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


def query_instances_by_ids(task_ids):
    """
    通过task_id数组查询指定实例状态
    
    Args:
        task_ids: task_id列表
    
    Returns:
        dict: API响应结果
    """
    url = f"{API_BASE_URL}/api/v1/app/status"
    headers = {
        "X-Auth-Token": get_api_token(),
        "Content-Type": "application/json"
    }
    payload = {"task_ids": task_ids}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code >= 400:
            return {
                "success": False,
                "error": f"HTTP请求失败: {response.status_code}",
                "details": response.text
            }
        
        result = response.json()
        
        if result.get("code") == 200:
            return {
                "success": True,
                "instances": result.get("data", {}).get("tasks", []),
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


def format_instance_info(instance):
    """格式化实例信息为易读格式"""
    container_info = instance.get("container_info") or {}
    return {
        "task_id": instance.get("task_id"),
        "container_id": instance.get("container_id"),
        "deploy_name": container_info.get("deploy_name"),
        "status": container_info.get("status"),
        "gpu_type": container_info.get("gpu_type"),
        "gpu_num": container_info.get("gpu_num"),
        "accessory": instance.get("accessory"),
        "create_time": instance.get("create_time"),
        "update_time": instance.get("update_time")
    }


def main():
    parser = argparse.ArgumentParser(description="查询无阶未来GPU实例状态")
    parser.add_argument("--task-id", help="指定查询的task_id")
    parser.add_argument("--task-ids", help="多个task_id，逗号分隔")
    
    args = parser.parse_args()
    
    if args.task_id:
        result = query_instances_by_ids([args.task_id])
    elif args.task_ids:
        task_ids = [tid.strip() for tid in args.task_ids.split(",")]
        result = query_instances_by_ids(task_ids)
    else:
        result = query_all_instances()
    
    # 格式化输出
    if result.get("success"):
        instances = result.get("instances", [])
        formatted_instances = [format_instance_info(inst) for inst in instances]
        result["instances"] = formatted_instances
        result["total"] = len(instances)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
