#!/usr/bin/env python3
"""
Sophie Auto Memory - 全自动智能记忆系统

自动监听对话，识别重要信息并存储
"""

import re
import sys
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/mem0_config.json")

# 自动触发模式配置
AUTO_TRIGGERS = {
    # 用户自我介绍
    "self_intro": {
        "patterns": [
            r"我叫(.+)",
            r"我是(.+)，(.+)了",
            r"我的名字叫(.+)",
            r"我叫(.+)，(.+)岁",
        ],
        "extractors": ["name", "profession", "age", "location"],
        "priority": "high"
    },
    # 用户偏好
    "preference": {
        "patterns": [
            r"我喜欢(.+)",
            r"我比较喜欢(.+)",
            r"我倾向于(.+)",
            r"我更偏好(.+)",
            r"我一般(.+)",
        ],
        "extractors": ["liking"],
        "priority": "medium"
    },
    # 用户习惯
    "habit": {
        "patterns": [
            r"我通常(.+)",
            r"我习惯(.+)",
            r"我一般(.+)点",
            r"我经常(.+)",
        ],
        "extractors": ["habit"],
        "priority": "medium"
    },
    # 待办/承诺
    "todo": {
        "patterns": [
            r"(记得|别忘了|要记住)(.+)",
            r"(答应|承诺|保证)(.+)",
            r"(计划|打算)(.+)",
            r"(周一|周二|周三|周四|周五|周六|周日)(.+?)出发",
        ],
        "extractors": ["todo"],
        "priority": "high"
    },
    # 用户纠正
    "correction": {
        "patterns": [
            r"(不对|错了|应该|不是(.+)而是)",
            r"我之前说过(.+)",
            r"其实(.+)",
        ],
        "extractors": ["correction"],
        "priority": "medium"
    },
    # 重要事实
    "fact": {
        "patterns": [
            r"我在(.+)工作",
            r"我在(.+)做(.+)",
            r"我在(.+)住(.+)年",
        ],
        "extractors": ["fact"],
        "priority": "high"
    },
    # 情感状态
    "emotion": {
        "patterns": [
            r"(今天|最近|最近有点)(累|忙|烦|开心|难过|焦虑)",
            r"感觉(.+)了",
        ],
        "extractors": ["emotion"],
        "priority": "low"
    }
}


def load_config() -> dict:
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def extract_memories(text: str) -> List[Dict]:
    """从文本中自动提取记忆"""
    memories = []
    
    for category, config in AUTO_TRIGGERS.items():
        for pattern in config["patterns"]:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                if category == "self_intro" and len(groups) >= 1:
                    memory = f"用户是{groups[0]}"
                    if len(groups) >= 2:
                        memory += f"，{groups[1]}"
                    memories.append({
                        "content": memory,
                        "category": category,
                        "priority": config["priority"],
                        "raw": text
                    })
                elif category == "preference":
                    memories.append({
                        "content": f"用户喜欢{groups[0]}",
                        "category": category,
                        "priority": config["priority"],
                        "raw": text
                    })
                elif category == "habit":
                    memories.append({
                        "content": f"用户习惯{groups[0]}",
                        "category": category,
                        "priority": config["priority"],
                        "raw": text
                    })
                elif category == "todo":
                    todo_content = groups[1] if len(groups) > 1 else groups[0]
                    memories.append({
                        "content": f"用户要求记住：{todo_content}",
                        "category": category,
                        "priority": config["priority"],
                        "raw": text
                    })
                elif category == "correction":
                    memories.append({
                        "content": f"用户纠正：{text}",
                        "category": category,
                        "priority": config["priority"],
                        "raw": text
                    })
                elif category == "fact":
                    facts = "，".join([g for g in groups if g])
                    memories.append({
                        "content": f"用户事实：{facts}",
                        "category": category,
                        "priority": config["priority"],
                        "raw": text
                    })
                elif category == "emotion":
                    memories.append({
                        "content": f"用户情绪状态：{groups[0]}{groups[1] if len(groups) > 1 else ''}",
                        "category": category,
                        "priority": config["priority"],
                        "raw": text
                    })
                break
    
    return memories


def store_memories(memories: List[Dict], user_id: str = "sophie") -> List[str]:
    """存储记忆到mem0"""
    try:
        config = load_config()
        from mem0.memory.main import Memory
        client = Memory.from_config(config)
    except Exception as e:
        print(f"❌ 初始化失败: {e}", file=sys.stderr)
        return []
    
    stored_ids = []
    
    for memory in memories:
        try:
            result = client.add(
                messages=memory["content"],
                user_id=user_id,
                metadata={
                    "category": memory["category"],
                    "priority": memory["priority"],
                    "source": "auto_extract",
                    "raw_text": memory["raw"][:200]
                }
            )
            stored_ids.append(str(result.get("id", "unknown")))
        except Exception as e:
            print(f"⚠️ 存储失败: {e}", file=sys.stderr)
    
    return stored_ids


def auto_monitor(text: str, user_id: str = "sophie") -> Tuple[int, List[str]]:
    """自动监控文本，返回(存储数量, 记忆ID列表)"""
    if not text or len(text) < 5:
        return 0, []
    
    memories = extract_memories(text)
    if not memories:
        return 0, []
    
    try:
        stored_ids = store_memories(memories, user_id)
        return len(stored_ids), stored_ids
    except Exception as e:
        print(f"❌ Auto memory error: {e}", file=sys.stderr)
        return 0, []


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Sophie Auto Memory - 全自动智能记忆")
    subparsers = parser.add_subparsers(dest="command")
    
    # auto 命令 - 自动监控
    auto_parser = subparsers.add_parser("auto", help="自动监控文本")
    auto_parser.add_argument("--text", "-t", required=True, help="要监控的文本")
    auto_parser.add_argument("--user", "-u", default="sophie", help="用户ID")
    
    # extract 命令 - 仅提取
    extract_parser = subparsers.add_parser("extract", help="仅提取不存储")
    extract_parser.add_argument("--text", "-t", required=True, help="要提取的文本")
    
    args = parser.parse_args()
    
    if args.command == "auto":
        count, ids = auto_monitor(args.text, args.user)
        if count > 0:
            print(f"✅ 自动存储{count}条记忆")
        else:
            print("🔍 没有发现需要记忆的内容")
        sys.exit(0)
    
    elif args.command == "extract":
        memories = extract_memories(args.text)
        if memories:
            print(f"🔍 发现{len(memories)}条可记忆信息：\n")
            for i, m in enumerate(memories, 1):
                print(f"{i}. [{m['priority']}] {m['content']}")
        else:
            print("🔍 没有发现需要记忆的内容")
        sys.exit(0)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
