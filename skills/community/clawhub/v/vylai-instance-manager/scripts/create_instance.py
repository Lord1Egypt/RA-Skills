#!/usr/bin/env python3
"""创建无阶未来GPU容器实例"""

import argparse
import json
import os
import sys
import time
import uuid

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


def create_instance(app_id, gpu_id, task_id=None, gpu_num=0, accessory=None):
    """
    创建GPU容器实例
    
    Args:
        app_id: 应用ID
        gpu_id: GPU资源ID (1=4090, 2=3090, 3=A100-SXM, 4=A100-PCIE, 12=4090-48G, 13=5090, 14=CPU)
        task_id: 任务唯一标识符（幂等控制），默认自动生成
        gpu_num: GPU数量 (0-8)，0表示使用应用默认值
        accessory: 自定义附加信息
    
    Returns:
        dict: API响应结果
    """
    if task_id is None:
        task_id = f"task-{uuid.uuid4().hex[:16]}"
    
    url = f"{API_BASE_URL}/api/v1/app/create"
    headers = {
        "X-Auth-Token": get_api_token(),
        "Content-Type": "application/json"
    }
    
    payload = {
        "task_id": task_id,
        "app_id": str(app_id),
        "gpu_id": gpu_id,
        "gpu_num": gpu_num
    }
    
    if accessory:
        payload["accessory"] = accessory
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code >= 400:
            return {
                "success": False,
                "error": f"HTTP请求失败: {response.status_code}",
                "details": response.text
            }
        
        result = response.json()
        
        # 处理业务错误码
        code = result.get("code")
        if code == 200:
            return {
                "success": True,
                "task_id": result["data"]["task_id"],
                "container_id": result["data"]["container_id"],
                "container_status": result["data"]["container_status"],
                "create_time": result["data"]["create_time"],
                "message": result.get("msg", "创建成功")
            }
        elif code == 234:
            # 任务已存在（幂等性）
            return {
                "success": True,
                "task_id": result["data"]["task_id"],
                "container_id": result["data"]["container_id"],
                "container_status": result["data"]["container_status"],
                "create_time": result["data"]["create_time"],
                "message": result.get("msg", "任务已存在"),
                "idempotent": True
            }
        else:
            return {
                "success": False,
                "error": result.get("msg", "未知错误"),
                "code": code
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"请求失败: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(description="创建无阶未来GPU容器实例")
    parser.add_argument("--app-id", required=True, help="应用ID")
    parser.add_argument("--gpu-id", type=int, default=1, 
                        help="GPU资源ID (1=4090, 2=3090, 3=A100, 4=A100-PCIE, 12=4090-48G, 13=5090, 14=CPU)")
    parser.add_argument("--task-id", help="任务唯一标识符（幂等控制）")
    parser.add_argument("--gpu-num", type=int, default=0, 
                        help="GPU数量 (0-8)，0表示使用应用默认值")
    parser.add_argument("--accessory", help="自定义附加信息（JSON格式）")
    
    args = parser.parse_args()
    
    accessory = None
    if args.accessory:
        try:
            accessory = json.loads(args.accessory)
        except json.JSONDecodeError:
            print(json.dumps({"success": False, "error": "accessory参数必须是有效JSON"}))
            sys.exit(1)
    
    result = create_instance(
        app_id=args.app_id,
        gpu_id=args.gpu_id,
        task_id=args.task_id,
        gpu_num=args.gpu_num,
        accessory=accessory
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
