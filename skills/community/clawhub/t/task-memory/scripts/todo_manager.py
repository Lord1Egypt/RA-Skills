#!/usr/bin/env python3
"""
todo_manager.py — 结构化任务管理系统
用法:
  python3 todo_manager.py --add "任务描述" --tag paper_trading --system
  python3 todo_manager.py --done <id>
  python3 todo_manager.py --check        # 检查过期项
  python3 todo_manager.py --list         # 列出所有
  python3 todo_manager.py --list --tag paper_trading
  python3 todo_manager.py --remove <id>
  python3 todo_manager.py --update <id> --title "新描述"
"""
import json
import os
import sys
import uuid
from datetime import datetime, timedelta

TODO_FILE = "/home/openclaw/.openclaw/workspace/backtest/todo.json"

def load():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE) as f:
            return json.load(f)
    return {"version": "1.0", "updated": "", "items": []}

def save(data):
    data["updated"] = datetime.now().isoformat()
    with open(TODO_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _validate_deadline(deadline):
    """验证 deadline 格式，不合法则报错退出"""
    if not deadline:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
        try:
            datetime.strptime(deadline.replace("+08:00", "").replace("+00:00", ""), fmt)
            return deadline
        except ValueError:
            continue
    print(f"❌ deadline 格式错误: '{deadline}'")
    print(f"   正确格式: YYYY-MM-DD (如 2026-04-05)")
    sys.exit(1)

def add(title, tag=None, deadline=None, system=False, notes=None):
    _validate_deadline(deadline)
    data = load()
    item = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "created": datetime.now().isoformat(),
        "deadline": deadline,
        "status": "pending",
        "tag": tag,
        "system": system,
        "notes": notes
    }
    data["items"].append(item)
    save(data)
    print(f"✅ 添加: [{item['id']}] {title} {'(系统任务)' if system else ''}")
    if deadline:
        print(f"   截止: {deadline}")
    return item["id"]

def done(id_):
    data = load()
    for item in data["items"]:
        if item["id"] == id_:
            item["status"] = "completed"
            item["completed_at"] = datetime.now().isoformat()
            # 自动归档：移动到 archive 列表
            if "archive" not in data:
                data["archive"] = []
            data["archive"].append(item)
            data["items"] = [x for x in data["items"] if x["id"] != id_]
            save(data)
            print(f"✅ 完成并归档: {item['title']}")
            return
    print(f"❌ 未找到: {id_}")

def remove(id_):
    data = load()
    before = len(data["items"])
    data["items"] = [x for x in data["items"] if x["id"] != id_]
    if len(data["items"]) < before:
        save(data)
        print(f"🗑️  删除: {id_}")
    else:
        print(f"❌ 未找到: {id_}")

def check():
    """检查过期未完成项，返回要推送的消息"""
    data = load()
    now = datetime.now()
    overdue = []
    upcoming = []
    
    for item in data["items"]:
        if item["status"] in ("completed", "cancelled"):
            continue
        if item.get("deadline"):
            try:
                dl = datetime.fromisoformat(item["deadline"])
                if dl < now:
                    overdue.append(item)
                elif dl < now + timedelta(hours=24):
                    upcoming.append(item)
            except:
                pass
    
    return overdue, upcoming

def list_items(tag=None, status=None):
    data = load()
    items = data["items"]
    if tag:
        items = [x for x in items if x.get("tag") == tag]
    if status:
        items = [x for x in items if x.get("status") == status]
    
    if not items:
        print("（无）")
        return
    
    now = datetime.now()
    for item in items:
        deadline_str = ""
        if item.get("deadline"):
            try:
                dl = datetime.fromisoformat(item["deadline"])
                overdue = "⚠️已过期" if dl < now and item["status"] != "completed" else ""
                deadline_str = f" | 截止: {item['deadline']} {overdue}"
            except:
                deadline_str = f" | 截止: {item['deadline']}"
        
        system_tag = "🤖" if item.get("system") else "👤"
        status_icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅", "cancelled": "❌"}.get(item["status"], "•")
        print(f"{status_icon} [{item['id']}] {system_tag} {item['title']}{deadline_str}")
        if item.get("notes"):
            print(f"   备注: {item['notes']}")

def archive_list():
    """列出归档（30天内）"""
    data = load()
    arch = data.get("archive", [])
    now = datetime.now()
    cutoff = now - timedelta(days=30)
    recent = []
    for item in arch:
        try:
            completed_at = datetime.fromisoformat(item.get("completed_at", "2020-01-01"))
            if completed_at > cutoff:
                recent.append((item, completed_at))
        except:
            pass
    if not recent:
        print("（无30天内归档）")
        return
    print(f"📦 归档（{len(recent)}条，保留30天）：")
    for item, ct in sorted(recent, key=lambda x: x[1], reverse=True):
        age = (now - ct).days
        print(f"  ✅ [{item['id']}] {item['title']} | 完成于: {ct.date()} ({age}天前)")
    print(f"\n超过30天的归档可用 --purge 清理")

def purge_archive():
    """清理30天前归档"""
    data = load()
    arch = data.get("archive", [])
    now = datetime.now()
    cutoff = now - timedelta(days=30)
    kept, removed = [], 0
    for item in arch:
        try:
            ct = datetime.fromisoformat(item.get("completed_at", "2020-01-01"))
            if ct > cutoff:
                kept.append(item)
            else:
                removed += 1
        except:
            kept.append(item)
    data["archive"] = kept
    save(data)
    print(f"🗑️  已清理 {removed} 条归档，保留 {len(kept)} 条")

def main():
    if len(sys.argv) == 1:
        print(__doc__)
        sys.exit(0)

    args = sys.argv[1:]
    
    if "--add" in args:
        idx = args.index("--add")
        title = args[idx + 1]
        tag = None
        deadline = None
        system = False
        notes = None
        if "--tag" in args:
            tag = args[args.index("--tag") + 1]
        if "--deadline" in args:
            deadline = args[args.index("--deadline") + 1]
        if "--system" in args:
            system = True
        if "--notes" in args:
            notes = args[args.index("--notes") + 1]
        add(title, tag=tag, deadline=deadline, system=system, notes=notes)
    
    elif "--done" in args:
        id_ = args[args.index("--done") + 1]
        done(id_)
    
    elif "--remove" in args:
        id_ = args[args.index("--remove") + 1]
        remove(id_)
    
    elif "--check" in args:
        overdue, upcoming = check()
        if overdue:
            print("⚠️ 已过期:")
            for item in overdue:
                print(f"  [{item['id']}] {item['title']} (截止: {item['deadline']})")
        if upcoming:
            print("📅 即将到期 (24h内):")
            for item in upcoming:
                print(f"  [{item['id']}] {item['title']} (截止: {item['deadline']})")
        if not overdue and not upcoming:
            print("✅ 无过期项")
    
    elif "--archive" in args:
        archive_list()
    
    elif "--purge" in args:
        purge_archive()
    
    elif "--list" in args:
        tag = None
        status = None
        if "--tag" in args:
            tag = args[args.index("--tag") + 1]
        if "--status" in args:
            status = args[args.index("--status") + 1]
        list_items(tag=tag, status=status)
    
    elif "--update" in args:
        idx = args.index("--update")
        id_ = args[idx + 1]
        data = load()
        for item in data["items"]:
            if item["id"] == id_:
                if "--title" in args:
                    item["title"] = args[args.index("--title") + 1]
                if "--deadline" in args:
                    item["deadline"] = args[args.index("--deadline") + 1]
                if "--status" in args:
                    item["status"] = args[args.index("--status") + 1]
                save(data)
                print(f"✅ 更新: [{id_}] {item['title']}")
                break
        else:
            print(f"❌ 未找到: {id_}")
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
