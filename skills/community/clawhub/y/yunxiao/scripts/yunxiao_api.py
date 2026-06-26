#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""云效 API 基础模块"""

import json
import os
import requests
from typing import Optional, Dict, Any, List

# 配置文件路径
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')

# API 基础 URL
BASE_URL = "https://openapi-rdc.aliyuncs.com"


def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_headers(config: Optional[Dict] = None) -> Dict[str, str]:
    """获取请求头"""
    if config is None:
        config = load_config()
    return {
        'Content-Type': 'application/json',
        'x-yunxiao-token': config['token']
    }


def list_workitems(
    space_id: str,
    workitem_type_id: Optional[str] = None,
    assigned_to: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20
) -> List[Dict[str, Any]]:
    """
    查询工作项列表
    
    注意：此接口需要指定项目空间 ID
    
    Args:
        space_id: 项目空间 ID（必填）
        workitem_type_id: 工作项类型 ID
        assigned_to: 负责人 userId
        status: 状态 ID
        page: 页码
        page_size: 每页数量
    
    Returns:
        工作项列表
    """
    config = load_config()
    org_id = config['org_id']
    
    url = f"{BASE_URL}/oapi/v1/projex/organizations/{org_id}/workitems:search"
    
    body = {
        "spaceId": space_id,
        "page": page,
        "pageSize": page_size
    }
    
    if workitem_type_id:
        body["workitemTypeId"] = workitem_type_id
    if assigned_to:
        body["assignedTo"] = assigned_to
    if status:
        body["status"] = status
    
    response = requests.post(url, headers=get_headers(config), json=body)
    response.raise_for_status()
    
    return response.json()


def get_workitem(workitem_id: str) -> Dict[str, Any]:
    """
    获取工作项详情
    
    Args:
        workitem_id: 工作项 ID
    
    Returns:
        工作项详情
    """
    config = load_config()
    org_id = config['org_id']
    
    url = f"{BASE_URL}/oapi/v1/projex/organizations/{org_id}/workitems/{workitem_id}"
    
    response = requests.get(url, headers=get_headers(config))
    response.raise_for_status()
    
    return response.json()


def create_workitem(
    subject: str,
    space_id: str,
    workitem_type_id: str,
    assigned_to: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    sprint: Optional[str] = None,
    labels: Optional[List[str]] = None,
    participants: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    创建工作项
    
    Args:
        subject: 标题
        space_id: 项目空间 ID
        workitem_type_id: 工作项类型 ID
        assigned_to: 负责人 userId
        description: 描述
        priority: 优先级 ID
        sprint: 迭代 ID
        labels: 标签 ID 列表
        participants: 参与人 userId 列表
    
    Returns:
        创建结果，包含工作项 ID
    """
    config = load_config()
    org_id = config['org_id']
    
    url = f"{BASE_URL}/oapi/v1/projex/organizations/{org_id}/workitems"
    
    body = {
        "subject": subject,
        "spaceId": space_id,
        "workitemTypeId": workitem_type_id
    }
    
    if assigned_to:
        body["assignedTo"] = assigned_to
    else:
        # 默认指派给自己
        body["assignedTo"] = config['user_id']
    
    if description:
        body["description"] = description
    
    if priority:
        body["customFieldValues"] = [
            {
                "fieldId": "priority",
                "values": [{"identifier": priority}]
            }
        ]
    
    if sprint:
        body["sprint"] = sprint
    
    if labels:
        body["labels"] = labels
    
    if participants:
        body["participants"] = participants
    
    response = requests.post(url, headers=get_headers(config), json=body)
    response.raise_for_status()
    
    return response.json()


def update_workitem(workitem_id: str, updates: Dict[str, Any]) -> bool:
    """
    更新工作项
    
    Args:
        workitem_id: 工作项 ID
        updates: 更新内容，格式为 {"fieldId": "value"}
    
    Returns:
        是否成功
    """
    config = load_config()
    org_id = config['org_id']
    
    url = f"{BASE_URL}/oapi/v1/projex/organizations/{org_id}/workitems/{workitem_id}"
    
    response = requests.put(url, headers=get_headers(config), json=updates)
    response.raise_for_status()
    
    return True


def list_projects() -> List[Dict[str, Any]]:
    """
    获取项目列表
    
    Returns:
        项目列表
    """
    config = load_config()
    org_id = config['org_id']
    
    url = f"{BASE_URL}/oapi/v1/projex/organizations/{org_id}/spaces"
    
    response = requests.get(url, headers=get_headers(config))
    response.raise_for_status()
    
    return response.json()


def list_workitem_types(space_id: str) -> List[Dict[str, Any]]:
    """
    获取工作项类型列表
    
    Args:
        space_id: 项目空间 ID
    
    Returns:
        工作项类型列表
    """
    config = load_config()
    org_id = config['org_id']
    
    url = f"{BASE_URL}/oapi/v1/projex/organizations/{org_id}/workitemTypes?spaceId={space_id}"
    
    response = requests.get(url, headers=get_headers(config))
    response.raise_for_status()
    
    return response.json()


def search_projects(
    name: Optional[str] = None,
    page: int = 1,
    per_page: int = 50
) -> List[Dict[str, Any]]:
    """
    搜索项目列表
    
    Args:
        name: 项目名称（模糊搜索）
        page: 页码
        per_page: 每页数量
    
    Returns:
        项目列表
    """
    config = load_config()
    org_id = config['org_id']
    
    url = f"{BASE_URL}/oapi/v1/projex/organizations/{org_id}/projects:search"
    
    body = {
        "page": page,
        "perPage": per_page
    }
    
    if name:
        body["conditions"] = json.dumps({
            "conditionGroups": [[{
                "className": "string",
                "fieldIdentifier": "name",
                "format": "input",
                "operator": "BETWEEN",
                "toValue": None,
                "value": [name]
            }]]
        })
    
    response = requests.post(url, headers=get_headers(config), json=body)
    response.raise_for_status()
    
    return response.json()


if __name__ == "__main__":
    # 测试 API 连接
    print("测试云效 API 连接...")
    
    try:
        config = load_config()
        print(f"组织 ID: {config['org_id']}")
        print(f"用户 ID: {config['user_id']}")
        
        # 测试查询工作项
        items = list_workitems(assigned_to=config['user_id'])
        print(f"查询到 {len(items)} 个工作项")
        
        if items:
            print("\n工作项列表:")
            for item in items[:5]:
                print(f"  - {item.get('subject', 'N/A')} ({item.get('serialNumber', 'N/A')})")
    except Exception as e:
        print(f"错误: {e}")