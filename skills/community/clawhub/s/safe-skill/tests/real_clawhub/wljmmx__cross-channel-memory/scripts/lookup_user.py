#!/usr/bin/env python3
"""
跨渠道用户查找工具
根据渠道和用户 ID 查找统一的用户标识和记忆路径
"""

import json
import argparse
import os
from pathlib import Path

# 共享映射文件路径
MAPPING_FILE = Path("/home/wljmmx/.openclaw/data/cross-channel-users.json")

def load_mapping():
    """加载用户映射文件"""
    if not MAPPING_FILE.exists():
        return {
            "users": {},
            "lookupIndex": {}
        }
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def lookup_user(channel: str, user_id: str, account_id: str = None):
    """
    根据渠道、用户 ID 和 agent ID 查找统一用户信息（支持按 agent 精确匹配）
    
    Args:
        channel: 渠道名称 (qqbot, feishu 等)
        user_id: 该渠道下的用户 ID
        account_id: agent 标识（可选，用于精确匹配）
        
    Returns:
        dict: {
            "found": bool,
            "userId": str,           # 统一用户 ID
            "displayName": str,      # 显示名称
            "memoryPaths": list,     # 记忆路径列表
            "channelId": str         # 渠道内标识
        }
    """
    mapping = load_mapping()
    
    # 在查找索引中搜索
    if channel not in mapping["lookupIndex"]:
        return {
            "found": False,
            "error": f"Channel '{channel}' not found in mapping"
        }
    
    channel_index = mapping["lookupIndex"][channel]
    
    # 尝试精确匹配（带 account_id）或模糊匹配
    matched_entry = None
    
    if account_id:
        # 精确匹配：user_id_account_id
        composite_key = f"{user_id}_{account_id}"
        if composite_key in channel_index:
            matched_entry = channel_index[composite_key]
    
    # 如果没有精确匹配，尝试只按 user_id 查找
    if not matched_entry and user_id in channel_index:
        matched_entry = channel_index[user_id]
    
    if not matched_entry:
        return {
            "found": False,
            "error": f"User ID '{user_id}' (account: {account_id}) not found in channel '{channel}'"
        }
    
    # 获取用户详情
    user_info = mapping["users"].get(unified_user_id, {})
    display_name = user_info.get("displayName", unified_user_id)
    
    # 计算记忆路径列表（根据 account_id 返回对应路径）
    workspace_base = Path("/home/wljmmx/.openclaw/workspace")
    memory_paths = []
    
    if account_id:
        # 精确匹配：只返回指定 agent 的记忆路径
        memory_paths.append({
            "accountId": account_id,
            "memoryPath": str(workspace_base / account_id / "memory")
        })
    else:
        # 返回该用户在所有关联 agent 的记忆路径
        for acct_id in user_info.get("channels", {}).get(channel, {}).keys():
            memory_paths.append({
                "accountId": acct_id,
                "memoryPath": str(workspace_base / acct_id / "memory")
            })
    
    return {
        "found": True,
        "userId": unified_user_id,
        "displayName": display_name,
        "memoryPaths": memory_paths,
        "channelId": channel,
        "channelUserId": user_id
    }

def add_mapping(channel: str, user_id: str, unified_user_id: str, account_id: str = "default", display_name: str = None):
    """
    添加用户映射
    
    Args:
        channel: 渠道名称
        user_id: 该渠道下的用户 ID
        unified_user_id: 统一用户 ID
        account_id: agent 标识
        display_name: 显示名称（可选）
    """
    mapping = load_mapping()
    
    # 初始化渠道索引
    if channel not in mapping["lookupIndex"]:
        mapping["lookupIndex"][channel] = {}
    
    # 添加映射
    mapping["lookupIndex"][channel][user_id] = {
        "userId": unified_user_id,
        "accountId": account_id
    }
    
    # 更新用户信息
    if unified_user_id not in mapping["users"]:
        mapping["users"][unified_user_id] = {
            "displayName": display_name or unified_user_id,
            "channels": {}
        }
    
    # 记录渠道信息
    if channel not in mapping["users"][unified_user_id]["channels"]:
        mapping["users"][unified_user_id]["channels"][channel] = {}
    
    mapping["users"][unified_user_id]["channels"][channel][account_id] = user_id
    
    # 保存映射文件
    MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    return {
        "success": True,
        "message": f"Added mapping for {unified_user_id} on {channel}"
    }

def main():
    parser = argparse.ArgumentParser(description="跨渠道用户查找工具")
    parser.add_argument("--channel", required=True, help="渠道名称 (qqbot, feishu)")
    parser.add_argument("--id", required=True, help="用户 ID")
    parser.add_argument("--account", help="agent 标识（可选，用于精确匹配）")
    parser.add_argument("--add", action="store_true", help="添加新映射")
    parser.add_argument("--user-id", help="统一用户 ID（添加时使用）")
    parser.add_argument("--account-id", default="default", help="agent 标识（添加时使用）")
    parser.add_argument("--display-name", help="显示名称（添加时使用）")
    
    args = parser.parse_args()
    
    if args.add:
        if not args.user_id:
            print(json.dumps({"success": False, "error": "--user-id is required when adding"}))
            return
        
        result = add_mapping(
            channel=args.channel,
            user_id=args.id,
            unified_user_id=args.user_id,
            account_id=args.account_id,
            display_name=args.display_name
        )
    else:
        result = lookup_user(args.channel, args.id, args.account)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
