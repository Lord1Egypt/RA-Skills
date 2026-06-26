#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📕 小红书账号管理模块
功能：多账号管理、Cookie 管理、登录状态追踪
"""

import json
from pathlib import Path
from datetime import datetime

# 配置文件路径
ACCOUNTS_FILE = Path(__file__).parent / "xhs_accounts.json"


def load_accounts():
    """加载账号配置"""
    if ACCOUNTS_FILE.exists():
        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"accounts": {}, "default": None}


def save_accounts(data):
    """保存账号配置"""
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_account(name, alias=None, notes=""):
    """
    添加账号
    
    Args:
        name: 账号唯一标识
        alias: 显示名称
        notes: 备注
        
    Returns:
        dict: 账号信息
    """
    data = load_accounts()
    
    if name in data["accounts"]:
        return {"success": False, "error": "账号已存在"}
    
    data["accounts"][name] = {
        "alias": alias or name,
        "notes": notes,
        "created": datetime.now().isoformat(),
        "last_login": None,
        "last_publish": None,
        "publish_count": 0
    }
    
    # 如果没有默认账号，设为默认
    if data["default"] is None:
        data["default"] = name
    
    save_accounts(data)
    
    return {
        "success": True,
        "account": data["accounts"][name]
    }


def remove_account(name, delete_profile=False):
    """
    删除账号
    
    Args:
        name: 账号名称
        delete_profile: 是否删除 Cookie 配置
        
    Returns:
        dict: 删除结果
    """
    data = load_accounts()
    
    if name not in data["accounts"]:
        return {"success": False, "error": "账号不存在"}
    
    del data["accounts"][name]
    
    # 如果删除的是默认账号，清除默认设置
    if data["default"] == name:
        data["default"] = None
    
    save_accounts(data)
    
    return {"success": True, "message": "账号已删除"}


def set_default(name):
    """
    设置默认账号
    
    Args:
        name: 账号名称
        
    Returns:
        dict: 设置结果
    """
    data = load_accounts()
    
    if name not in data["accounts"]:
        return {"success": False, "error": "账号不存在"}
    
    data["default"] = name
    save_accounts(data)
    
    return {"success": True, "default": name}


def get_default():
    """获取默认账号"""
    data = load_accounts()
    return data["default"]


def list_accounts():
    """
    列出所有账号
    
    Returns:
        list: 账号列表
    """
    data = load_accounts()
    
    accounts = []
    for name, info in data["accounts"].items():
        account = {
            "name": name,
            "alias": info.get("alias", name),
            "notes": info.get("notes", ""),
            "is_default": name == data["default"],
            "created": info.get("created", ""),
            "last_login": info.get("last_login", ""),
            "last_publish": info.get("last_publish", ""),
            "publish_count": info.get("publish_count", 0)
        }
        accounts.append(account)
    
    return accounts


def update_account(name, **kwargs):
    """
    更新账号信息
    
    Args:
        name: 账号名称
        **kwargs: 要更新的字段
        
    Returns:
        dict: 更新结果
    """
    data = load_accounts()
    
    if name not in data["accounts"]:
        return {"success": False, "error": "账号不存在"}
    
    # 更新指定字段
    for key, value in kwargs.items():
        if key in data["accounts"][name]:
            data["accounts"][name][key] = value
    
    save_accounts(data)
    
    return {"success": True}


def record_publish(name):
    """
    记录发布
    
    Args:
        name: 账号名称
        
    Returns:
        dict: 记录结果
    """
    data = load_accounts()
    
    if name not in data["accounts"]:
        return {"success": False, "error": "账号不存在"}
    
    # 更新发布信息
    data["accounts"][name]["last_publish"] = datetime.now().isoformat()
    data["accounts"][name]["publish_count"] = data["accounts"][name].get("publish_count", 0) + 1
    
    save_accounts(data)
    
    return {"success": True}


def record_login(name):
    """
    记录登录
    
    Args:
        name: 账号名称
        
    Returns:
        dict: 记录结果
    """
    data = load_accounts()
    
    if name not in data["accounts"]:
        return {"success": False, "error": "账号不存在"}
    
    data["accounts"][name]["last_login"] = datetime.now().isoformat()
    save_accounts(data)
    
    return {"success": True}


def get_account_stats(name):
    """
    获取账号统计
    
    Args:
        name: 账号名称
        
    Returns:
        dict: 统计信息
    """
    data = load_accounts()
    
    if name not in data["accounts"]:
        return None
    
    info = data["accounts"][name]
    
    return {
        "name": name,
        "alias": info.get("alias", name),
        "created": info.get("created", ""),
        "last_login": info.get("last_login", ""),
        "last_publish": info.get("last_publish", ""),
        "publish_count": info.get("publish_count", 0),
        "is_default": name == data["default"]
    }


# 测试
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("📕 小红书账号管理 - 测试")
    print("=" * 60)
    
    # 添加测试账号
    print("\n添加测试账号...")
    result = add_account("test_account", "测试账号", "用于测试")
    print(f"添加结果：{result}")
    
    # 列出账号
    print("\n账号列表:")
    accounts = list_accounts()
    for acc in accounts:
        default_mark = " (默认)" if acc["is_default"] else ""
        print(f"  - {acc['alias']}{default_mark} - 发布 {acc['publish_count']} 次")
    
    # 设置默认
    print("\n设置默认账号...")
    result = set_default("test_account")
    print(f"设置结果：{result}")
    
    # 获取统计
    print("\n账号统计:")
    stats = get_account_stats("test_account")
    print(f"  账号：{stats['alias']}")
    print(f"  发布次数：{stats['publish_count']}")
    print(f"  最后发布：{stats['last_publish']}")
