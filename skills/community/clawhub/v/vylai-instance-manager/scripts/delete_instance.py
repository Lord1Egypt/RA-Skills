#!/usr/bin/env python3
"""删除无阶未来GPU实例"""

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


def delete_by_task_id(task_id):
    """
    通过task_id删除实例
    
    Args:
        task_id: 任务标识符
    
    Returns:
        dict: API响应结果
    """
    url = f"{API_BASE_URL}/api/v1/app/delete/{task_id}"
    headers = {
        "X-Auth-Token": get_api_token()
    }
    
    try:
        response = requests.delete(url, headers=headers, timeout=30)
        
        if response.status_code >= 400:
            return {
                "success": False,
                "error": f"HTTP请求失败: {response.status_code}",
                "details": response.text
            }
        
        result = response.json()
        code = result.get("code")
        
        if code == 200:
            return {
                "success": True,
                "task_id": task_id,
                "message": result.get("msg", "删除成功")
            }
        else:
            return {
                "success": False,
                "error": result.get("msg", "未知错误"),
                "code": code,
                "task_id": task_id
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"请求失败: {str(e)}"
        }


def delete_by_deploy_name(deploy_name):
    """
    通过deploy_name删除实例
    
    Args:
        deploy_name: 容器部署名称（实例ID）
    
    Returns:
        dict: API响应结果
    """
    url = f"{API_BASE_URL}/api/v1/deploy/delete/{deploy_name}"
    headers = {
        "X-Auth-Token": get_api_token()
    }
    
    try:
        response = requests.delete(url, headers=headers, timeout=30)
        
        if response.status_code >= 400:
            return {
                "success": False,
                "error": f"HTTP请求失败: {response.status_code}",
                "details": response.text
            }
        
        result = response.json()
        code = result.get("code")
        
        if code == 200:
            return {
                "success": True,
                "deploy_name": deploy_name,
                "message": result.get("msg", "删除成功")
            }
        else:
            return {
                "success": False,
                "error": result.get("msg", "未知错误"),
                "code": code,
                "deploy_name": deploy_name
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"请求失败: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(description="删除无阶未来GPU实例")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--task-id", help="通过task_id删除")
    group.add_argument("--deploy-name", help="通过deploy_name（实例ID）删除")
    
    args = parser.parse_args()
    
    if args.task_id:
        result = delete_by_task_id(args.task_id)
    else:
        result = delete_by_deploy_name(args.deploy_name)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
