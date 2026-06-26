#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
notebook - 待办事项管理脚本
支持添加、完成、查询、删除待办事项
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 数据文件路径
DATA_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / "todos.json"

def load_todos():
    """加载待办事项"""
    if not DATA_FILE.exists():
        return {"todos": [], "next_id": 1}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_todos(data):
    """保存待办事项"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_todo(title, due=None, priority="normal"):
    """添加待办事项"""
    data = load_todos()
    todo = {
        "id": data["next_id"],
        "title": title,
        "created_at": datetime.now().isoformat(),
        "due": due,
        "priority": priority,
        "status": "pending",
        "completed_at": None
    }
    data["todos"].append(todo)
    data["next_id"] += 1
    save_todos(data)
    print(f"✅ 已添加待办 #{todo['id']}: {title}")
    if due:
        print(f"   截止时间：{due}")
    return todo["id"]

def complete_todo(todo_id):
    """标记事项为已完成"""
    data = load_todos()
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            todo["status"] = "completed"
            todo["completed_at"] = datetime.now().isoformat()
            save_todos(data)
            print(f"✅ 已完成 #{todo_id}: {todo['title']}")
            return True
    print(f"❌ 未找到事项 #{todo_id}")
    return False

def delete_todo(todo_id):
    """删除事项"""
    data = load_todos()
    for i, todo in enumerate(data["todos"]):
        if todo["id"] == todo_id:
            deleted = data["todos"].pop(i)
            save_todos(data)
            print(f"🗑️  已删除 #{todo_id}: {deleted['title']}")
            return True
    print(f"❌ 未找到事项 #{todo_id}")
    return False

def list_todos(status=None, today=False, since=None, until=None, pending_future=False):
    """查询待办事项"""
    data = load_todos()
    todos = data["todos"]
    now = datetime.now()
    
    # 过滤
    filtered = []
    for todo in todos:
        # 状态过滤
        if status and todo["status"] != status:
            continue
        
        # 今日过滤
        if today:
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            created = datetime.fromisoformat(todo["created_at"])
            if status == "completed":
                completed = datetime.fromisoformat(todo["completed_at"]) if todo["completed_at"] else None
                if not completed or not (today_start <= completed < today_end):
                    continue
            else:
                if not (today_start <= created < today_end):
                    continue
        
        # 时间范围过滤
        if since:
            since_dt = datetime.fromisoformat(since)
            if status == "completed":
                completed = datetime.fromisoformat(todo["completed_at"]) if todo["completed_at"] else None
                if not completed or completed < since_dt:
                    continue
            else:
                created = datetime.fromisoformat(todo["created_at"])
                if created < since_dt:
                    continue
        
        if until:
            until_dt = datetime.fromisoformat(until)
            if status == "completed":
                completed = datetime.fromisoformat(todo["completed_at"]) if todo["completed_at"] else None
                if not completed or completed > until_dt:
                    continue
        
        # 未来待办过滤
        if pending_future:
            if todo["status"] != "pending":
                continue
            if not todo["due"]:
                continue
            due_dt = datetime.fromisoformat(todo["due"])
            if due_dt <= now:
                continue
        
        filtered.append(todo)
    
    # 显示
    if not filtered:
        print("📭 没有找到相关事项")
        return
    
    print(f"📋 共找到 {len(filtered)} 项:\n")
    for todo in filtered:
        status_icon = "✅" if todo["status"] == "completed" else "⏳"
        priority_icon = {"high": "🔴", "normal": "🟡", "low": "🟢"}.get(todo["priority"], "🟡")
        
        print(f"{status_icon} {priority_icon} #{todo['id']}: {todo['title']}")
        if todo["due"]:
            due_dt = datetime.fromisoformat(todo["due"])
            print(f"   截止：{due_dt.strftime('%Y-%m-%d %H:%M')}")
        if todo["completed_at"]:
            completed_dt = datetime.fromisoformat(todo["completed_at"])
            print(f"   完成：{completed_dt.strftime('%Y-%m-%d %H:%M')}")
        print()

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  notebook.py add <标题> [--due YYYY-MM-DDTHH:MM:SS] [--priority high|normal|low]")
        print("  notebook.py complete <ID>")
        print("  notebook.py delete <ID>")
        print("  notebook.py list [--today] [--pending|--completed] [--since YYYY-MM-DD] [--until YYYY-MM-DD]")
        print("  notebook.py list --future  # 查询未来待完成")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "add":
        if len(sys.argv) < 3:
            print("❌ 请提供待办标题")
            sys.exit(1)
        title = sys.argv[2]
        due = None
        priority = "normal"
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--due" and i + 1 < len(sys.argv):
                due = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                priority = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        add_todo(title, due, priority)
    
    elif cmd == "complete":
        if len(sys.argv) < 3:
            print("❌ 请提供事项 ID")
            sys.exit(1)
        try:
            todo_id = int(sys.argv[2])
            complete_todo(todo_id)
        except ValueError:
            print("❌ ID 必须是数字")
            sys.exit(1)
    
    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("❌ 请提供事项 ID")
            sys.exit(1)
        try:
            todo_id = int(sys.argv[2])
            delete_todo(todo_id)
        except ValueError:
            print("❌ ID 必须是数字")
            sys.exit(1)
    
    elif cmd == "list":
        status = None
        today = False
        since = None
        until = None
        pending_future = False
        
        for arg in sys.argv[2:]:
            if arg == "--pending":
                status = "pending"
            elif arg == "--completed":
                status = "completed"
            elif arg == "--today":
                today = True
            elif arg == "--since" and sys.argv.index(arg) + 1 < len(sys.argv):
                since = sys.argv[sys.argv.index(arg) + 1]
            elif arg == "--until" and sys.argv.index(arg) + 1 < len(sys.argv):
                until = sys.argv[sys.argv.index(arg) + 1]
            elif arg == "--future":
                pending_future = True
        
        list_todos(status=status, today=today, since=since, until=until, pending_future=pending_future)
    
    else:
        print(f"❌ 未知命令：{cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
