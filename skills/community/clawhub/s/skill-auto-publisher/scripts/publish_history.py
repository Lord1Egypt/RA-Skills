#!/usr/bin/env python3
"""发布历史管理脚本"""

import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path("/root/.openclaw/workspace/skills/.publish_history.json")

def load_history():
    """加载发布历史"""
    if HISTORY_FILE.exists():
        return json.load(open(HISTORY_FILE))
    return {}

def save_history(history):
    """保存发布历史"""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_file_hash(file_path):
    """计算文件 MD5"""
    return hashlib.md5(file_path.read_bytes()).hexdigest()[:12]

def get_skill_snapshot(skill_path):
    """获取技能文件快照"""
    skill_dir = Path(skill_path)
    snapshot = {}
    
    for file in skill_dir.rglob("*"):
        if file.is_file() and not file.name.startswith("."):
            rel_path = str(file.relative_to(skill_dir))
            snapshot[rel_path] = f"hash:{get_file_hash(file)}"
    
    return snapshot

def get_last_publish(skill_name):
    """获取上次发布记录"""
    history = load_history()
    return history.get(skill_name)

def record_publish(skill_name, version, changelog, skill_path):
    """记录发布"""
    history = load_history()
    
    history[skill_name] = {
        "last_version": version,
        "last_published_at": datetime.now().isoformat(),
        "files": get_skill_snapshot(skill_path),
        "changelog": changelog
    }
    
    save_history(history)
    print(f"📝 已记录发布历史: {skill_name}@{version}")

def show_history(skill_name):
    """显示发布历史"""
    record = get_last_publish(skill_name)
    
    if not record:
        print(f"❌ 未找到 {skill_name} 的发布记录")
        return
    
    print(f"📋 {skill_name} 发布记录")
    print(f"  版本: {record['last_version']}")
    print(f"  时间: {record['last_published_at']}")
    print(f"  Changelog: {record['changelog']}")
    print(f"  文件数: {len(record['files'])}")

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 publish_history.py show <skill-name>")
        print("  python3 publish_history.py record <skill-name> <version> <changelog> <skill-path>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "show":
        if len(sys.argv) < 3:
            print("❌ 缺少 skill-name")
            sys.exit(1)
        show_history(sys.argv[2])
    
    elif cmd == "record":
        if len(sys.argv) < 6:
            print("❌ 参数不足")
            sys.exit(1)
        record_publish(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    
    else:
        print(f"❌ 未知命令: {cmd}")

if __name__ == "__main__":
    main()
