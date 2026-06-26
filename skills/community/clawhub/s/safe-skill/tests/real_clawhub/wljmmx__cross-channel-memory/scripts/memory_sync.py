#!/usr/bin/env python3
"""
跨渠道记忆同步工具
支持在 QQ、飞书等渠道间同步用户记忆
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
import hashlib

# 配置
MAPPING_FILE = Path("/home/wljmmx/.openclaw/data/cross-channel-users.json")
WORKSPACE_BASE = Path("/home/wljmmx/.openclaw/workspace")

def load_mapping():
    """加载用户映射文件"""
    if not MAPPING_FILE.exists():
        return {"users": {}, "lookupIndex": {}}
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_user_memory_paths(channel: str, user_id: str, account_id: str = None):
    """获取用户在指定 agent 的记忆路径（支持按 agent 精确匹配）"""
    mapping = load_mapping()
    
    if channel not in mapping["lookupIndex"]:
        return {"error": f"Channel '{channel}' not found"}
    
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
        return {"error": f"User '{user_id}' (account: {account_id}) not found in channel '{channel}'"}
    
    unified_user_id = matched_entry["userId"]
    target_account = matched_entry.get("accountId", account_id or "default")
    
    # 只返回对应 agent 的记忆路径（精确匹配）
    memory_paths = [{
        "accountId": target_account,
        "memoryPath": str(WORKSPACE_BASE / target_account / "memory")
    }]
    
    return {
        "userId": unified_user_id,
        "displayName": mapping["users"][unified_user_id].get("displayName", unified_user_id),
        "memoryPaths": memory_paths,
        "accountId": target_account
    }

def write_memory_record(channel: str, user_id: str, message: dict, account_id: str = None):
    """
    写入记忆记录（按 agent 精确写入）
    
    Args:
        channel: 渠道名称
        user_id: 用户 ID
        message: {
            "type": "user" | "assistant",
            "content": str,
            "timestamp": str (ISO format),
            "context": str (可选)
        }
        account_id: agent 标识（精确匹配）
    """
    paths_info = get_user_memory_paths(channel, user_id, account_id)
    
    if "error" in paths_info:
        return {"success": False, "error": paths_info["error"]}
    
    # 创建今天的记忆文件
    today = datetime.now().strftime("%Y-%m-%d")
    records = []
    
    for path_info in paths_info["memoryPaths"]:
        memory_dir = Path(path_info["memoryPath"])
        memory_dir.mkdir(parents=True, exist_ok=True)
        
        daily_file = memory_dir / f"{today}.md"
        
        # 生成记忆记录内容
        timestamp = message.get("timestamp", datetime.now().isoformat())
        record_content = f"""## [{message['type']}] {timestamp}

**渠道**: {channel}
**用户**: {paths_info['displayName']} ({user_id})
**Agent**: {path_info['accountId']}

{message['content']}

---

"""
        
        # 写入文件末尾
        if daily_file.exists():
            with open(daily_file, 'a', encoding='utf-8') as f:
                f.write(record_content)
        else:
            with open(daily_file, 'w', encoding='utf-8') as f:
                # 添加文件头
                f.write(f"# {today} 的记忆\n\n")
                f.write(f"**跨渠道记忆同步记录**\n\n")
                f.write(record_content)
        
        records.append({
            "accountId": path_info["accountId"],
            "file": str(daily_file),
            "written": True
        })
    
    return {
        "success": True,
        "records": records,
        "message": f"Written to {len(records)} agent memory files"
    }

def init_user_mapping(channel: str, user_id: str, unified_user_id: str, 
                     account_id: str = "default", display_name: str = None):
    """初始化用户映射"""
    mapping = load_mapping()
    
    # 如果统一用户不存在，创建
    if unified_user_id not in mapping["users"]:
        mapping["users"][unified_user_id] = {
            "displayName": display_name or unified_user_id,
            "channels": {}
        }
    
    # 初始化渠道索引
    if channel not in mapping["lookupIndex"]:
        mapping["lookupIndex"][channel] = {}
    
    # 添加映射
    mapping["lookupIndex"][channel][user_id] = {
        "userId": unified_user_id,
        "accountId": account_id
    }
    
    # 记录用户在该渠道的信息
    if channel not in mapping["users"][unified_user_id]["channels"]:
        mapping["users"][unified_user_id]["channels"][channel] = {}
    
    mapping["users"][unified_user_id]["channels"][channel][account_id] = user_id
    
    # 保存
    MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    return {
        "success": True,
        "message": f"Initialized user mapping for {unified_user_id}"
    }

def main():
    parser = argparse.ArgumentParser(description="跨渠道记忆同步工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # lookup 命令
    lookup_parser = subparsers.add_parser("lookup", help="查找用户记忆路径")
    lookup_parser.add_argument("--channel", required=True, help="渠道名称")
    lookup_parser.add_argument("--id", required=True, help="用户 ID")
    lookup_parser.add_argument("--account", help="agent 标识（可选，用于精确匹配）")
    
    # write 命令
    write_parser = subparsers.add_parser("write", help="写入记忆记录")
    write_parser.add_argument("--channel", required=True, help="渠道名称")
    write_parser.add_argument("--id", required=True, help="用户 ID")
    write_parser.add_argument("--account", help="agent 标识（精确匹配）")
    write_parser.add_argument("--type", required=True, choices=["user", "assistant"], help="消息类型")
    write_parser.add_argument("--content", required=True, help="消息内容")
    write_parser.add_argument("--timestamp", default=datetime.now().isoformat(), help="时间戳")
    
    # init 命令
    init_parser = subparsers.add_parser("init", help="初始化用户映射")
    init_parser.add_argument("--channel", required=True, help="渠道名称")
    init_parser.add_argument("--user-id", required=True, help="渠道用户 ID")
    init_parser.add_argument("--unified-id", required=True, help="统一用户 ID")
    init_parser.add_argument("--account-id", default="default", help="agent 标识")
    init_parser.add_argument("--display-name", help="显示名称")
    
    args = parser.parse_args()
    
    if args.command == "lookup":
        result = get_user_memory_paths(args.channel, args.id, getattr(args, 'account', None))
    elif args.command == "write":
        result = write_memory_record(
            channel=args.channel,
            user_id=args.id,
            message={
                "type": args.type,
                "content": args.content,
                "timestamp": args.timestamp
            },
            account_id=getattr(args, 'account', None)
        )
    elif args.command == "init":
        result = init_user_mapping(
            channel=args.channel,
            user_id=args.user_id,
            unified_user_id=args.unified_id,
            account_id=args.account_id,
            display_name=args.display_name
        )
    else:
        parser.print_help()
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
