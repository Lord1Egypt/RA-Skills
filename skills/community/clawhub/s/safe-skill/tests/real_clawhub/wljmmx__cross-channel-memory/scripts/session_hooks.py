#!/usr/bin/env python3
"""
Session Hooks - 跨渠道记忆同步钩子
在新 session 开始时自动核对和更新用户映射关系
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

# 配置路径
MAPPING_FILE = Path("/home/wljmmx/.openclaw/data/cross-channel-users.json")
WORKSPACE_BASE = Path("/home/wljmmx/.openclaw/workspace")
SESSION_STATE_DIR = Path("/home/wljmmx/.openclaw/data/session-states")

def load_mapping():
    """加载用户映射文件"""
    if not MAPPING_FILE.exists():
        return {"users": {}, "lookupIndex": {}, "metadata": {}}
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_mapping(mapping):
    """保存用户映射文件"""
    MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
    mapping["metadata"]["lastUpdated"] = datetime.now().isoformat()
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

def get_session_state_file(agent_id: str, channel: str, session_id: str) -> Path:
    """获取 session 状态文件路径"""
    SESSION_STATE_DIR.mkdir(parents=True, exist_ok=True)
    return SESSION_STATE_DIR / f"{agent_id}_{channel}_{session_id}.json"

def load_session_state(agent_id: str, channel: str, session_id: str) -> dict:
    """加载 session 状态"""
    state_file = get_session_state_file(agent_id, channel, session_id)
    if not state_file.exists():
        return {"checked": False, "lastCheck": None, "updates": []}
    with open(state_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_session_state(agent_id: str, channel: str, session_id: str, state: dict):
    """保存 session 状态"""
    state_file = get_session_state_file(agent_id, channel, session_id)
    state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def check_and_update_mapping(agent_id: str, channel: str, user_id: str, 
                              unified_user_id: str = None, display_name: str = None,
                              session_id: str = None, auto_create: bool = True) -> dict:
    """
    检查并更新用户映射
    
    Args:
        agent_id: agent 标识
        channel: 渠道名称
        user_id: 渠道用户 ID
        unified_user_id: 统一用户 ID（可选，用于新建用户）
        display_name: 显示名称（可选）
        session_id: 会话 ID（可选，用于 session 状态追踪）
        auto_create: 是否自动创建新用户
        
    Returns:
        dict: {
            "status": "ok" | "updated" | "created" | "error",
            "changed": bool,
            "message": str,
            "userId": str,
            "displayName": str,
            "updates": list
        }
    """
    mapping = load_mapping()
    updates = []
    changed = False
    
    # 检查用户是否已存在
    composite_key = f"{user_id}_{agent_id}"
    lookup_index = mapping.get("lookupIndex", {})
    channel_index = lookup_index.get(channel, {})
    
    if composite_key in channel_index:
        # 用户已存在，检查映射是否一致
        existing = channel_index[composite_key]
        unified_id = existing["userId"]
        
        # 检查 users 中的映射是否一致
        user_info = mapping["users"].get(unified_id, {})
        channels_info = user_info.get("channels", {}).get(channel, {})
        
        if channels_info.get(agent_id) != user_id:
            # 映射不一致，需要更新
            channels_info[agent_id] = user_id
            updates.append(f"Updated {agent_id} mapping for {channel}")
            changed = True
        
        display_name = user_info.get("displayName", unified_id)
        status = "ok"
        message = "映射关系核对完成，无变化"
        
    elif auto_create:
        # 用户不存在，自动创建
        if not unified_user_id:
            # 生成临时统一用户 ID
            unified_user_id = f"user_{user_id[:8]}"
        
        if unified_user_id not in mapping["users"]:
            mapping["users"][unified_user_id] = {
                "displayName": display_name or unified_user_id,
                "channels": {},
                "created": datetime.now().isoformat()
            }
        
        # 添加渠道映射
        if channel not in mapping["users"][unified_user_id]["channels"]:
            mapping["users"][unified_user_id]["channels"][channel] = {}
        mapping["users"][unified_user_id]["channels"][channel][agent_id] = user_id
        
        # 添加到查找索引
        if channel not in mapping.get("lookupIndex", {}):
            mapping["lookupIndex"][channel] = {}
        mapping["lookupIndex"][channel][composite_key] = {
            "userId": unified_user_id,
            "accountId": agent_id,
            "channelUserId": user_id
        }
        
        # 保存更新
        save_mapping(mapping)
        
        updates.append(f"Created new user mapping: {unified_user_id}")
        updates.append(f"Linked {channel}:{user_id} -> {agent_id}")
        changed = True
        display_name = display_name or unified_user_id
        status = "created"
        message = f"新建用户映射：{display_name} ({unified_user_id})"
        
    else:
        return {
            "status": "error",
            "changed": False,
            "message": f"User not found and auto_create is disabled",
            "userId": None,
            "displayName": None,
            "updates": []
        }
    
    # 保存 session 状态
    if session_id:
        state = load_session_state(agent_id, channel, session_id)
        state["checked"] = True
        state["lastCheck"] = datetime.now().isoformat()
        state["userId"] = unified_user_id or existing["userId"]
        state["channel"] = channel
        state["agentId"] = agent_id
        if updates:
            state["updates"] = state.get("updates", []) + updates
        save_session_state(agent_id, channel, session_id, state)
    
    return {
        "status": status,
        "changed": changed,
        "message": message,
        "userId": unified_user_id or existing["userId"],
        "displayName": display_name,
        "updates": updates
    }

def session_hook(agent_id: str, channel: str, user_id: str, 
                  session_id: str = None, unified_user_id: str = None,
                  display_name: str = None) -> dict:
    """
    Session 钩子 - 在新 session 开始时调用
    
    Args:
        agent_id: agent 标识
        channel: 渠道名称 (qqbot, feishu)
        user_id: 渠道用户 ID
        session_id: 会话 ID
        unified_user_id: 统一用户 ID（可选）
        display_name: 显示名称（可选）
        
    Returns:
        dict: 钩子执行结果，包含是否需要通知用户
    """
    # 检查是否已在此 session 中检查过
    if session_id:
        state = load_session_state(agent_id, channel, session_id)
        if state.get("checked", False):
            return {
                "status": "already_checked",
                "changed": False,
                "message": "此 session 已检查过映射关系",
                "notify": False,
                "userId": state.get("userId"),
                "displayName": None
            }
    
    # 执行检查和更新
    result = check_and_update_mapping(
        agent_id=agent_id,
        channel=channel,
        user_id=user_id,
        unified_user_id=unified_user_id,
        display_name=display_name,
        session_id=session_id,
        auto_create=True
    )
    
    # 判断是否需要通知用户
    notify = result["changed"] or result["status"] == "created"
    
    # 生成通知消息
    notify_message = ""
    if notify:
        if result["status"] == "created":
            notify_message = f"📋 已为您创建跨渠道用户映射：{result['displayName']}\n"
            notify_message += f"渠道：{channel}\n"
            notify_message += f"Agent：{agent_id}\n"
            notify_message += f"统一用户ID：{result['userId']}"
        elif result["status"] == "updated":
            notify_message = f"📋 用户映射已更新\n"
            notify_message += "\n".join(result["updates"])
    
    return {
        "status": result["status"],
        "changed": result["changed"],
        "message": result["message"],
        "notify": notify,
        "notifyMessage": notify_message,
        "userId": result["userId"],
        "displayName": result["displayName"],
        "updates": result["updates"]
    }

def main():
    parser = argparse.ArgumentParser(description="Session Hooks - 跨渠道记忆同步钩子")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # hook 命令 - session 钩子
    hook_parser = subparsers.add_parser("hook", help="执行 session 钩子")
    hook_parser.add_argument("--agent", required=True, help="agent 标识")
    hook_parser.add_argument("--channel", required=True, help="渠道名称")
    hook_parser.add_argument("--user-id", required=True, help="渠道用户 ID")
    hook_parser.add_argument("--session-id", help="会话 ID")
    hook_parser.add_argument("--unified-user-id", help="统一用户 ID")
    hook_parser.add_argument("--display-name", help="显示名称")
    
    # check 命令 - 检查映射
    check_parser = subparsers.add_parser("check", help="检查用户映射")
    check_parser.add_argument("--agent", required=True, help="agent 标识")
    check_parser.add_argument("--channel", required=True, help="渠道名称")
    check_parser.add_argument("--user-id", required=True, help="渠道用户 ID")
    check_parser.add_argument("--session-id", help="会话 ID")
    
    # status 命令 - 查看状态
    status_parser = subparsers.add_parser("status", help="查看 session 状态")
    status_parser.add_argument("--agent", required=True, help="agent 标识")
    status_parser.add_argument("--channel", required=True, help="渠道名称")
    status_parser.add_argument("--session-id", required=True, help="会话 ID")
    
    args = parser.parse_args()
    
    if args.command == "hook":
        result = session_hook(
            agent_id=args.agent,
            channel=args.channel,
            user_id=args.user_id,
            session_id=args.session_id,
            unified_user_id=getattr(args, 'unified_user_id', None),
            display_name=getattr(args, 'display_name', None)
        )
    elif args.command == "check":
        result = check_and_update_mapping(
            agent_id=args.agent,
            channel=args.channel,
            user_id=args.user_id,
            session_id=args.session_id,
            auto_create=False
        )
    elif args.command == "status":
        result = load_session_state(args.agent, args.channel, args.session_id)
    else:
        parser.print_help()
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()