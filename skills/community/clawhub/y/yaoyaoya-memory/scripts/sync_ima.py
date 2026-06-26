#!/usr/bin/env python3
"""
IMA 同步脚本 - IMA Knowledge Sync

用法：
    python sync_ima.py                    # 同步所有
    python sync_ima.py --note 日记        # 同步指定笔记
    python sync_ima.py --file MEMORY.md   # 同步指定文件

依赖：
    pip install requests

配置（通过环境变量或 config.json）：
    IMA_CLIENT_ID
    IMA_API_KEY
"""

import os
import sys
import json
import time
import argparse
import urllib.request
from datetime import datetime

# ============== 配置 ==============
DEFAULT_CONFIG = {
    "client_id": "your-ima-client-id",
    "api_key": "your-ima-api-key",
    "notes_mapping": {
        "AI记忆库": "7445750904545580",
        "日记": "7445750912911573",
        "决策库": "7445750929715125",
        "用户档案": "7445750942269901",
        "经验总结": "7445750959047844",
        "项目": "7445750967460566"
    }
}

IMA_API_BASE = "https://ima.qq.com/"


def load_config():
    """加载配置"""
    config = DEFAULT_CONFIG.copy()
    
    # 环境变量覆盖
    if os.environ.get("IMA_CLIENT_ID"):
        config["client_id"] = os.environ["IMA_CLIENT_ID"]
    if os.environ.get("IMA_API_KEY"):
        config["api_key"] = os.environ["IMA_API_KEY"]
    
    # config.json 覆盖
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = json.load(f)
            if "knowledge_sync" in user_config:
                ks = user_config["knowledge_sync"]
                if "client_id" in ks:
                    config["client_id"] = ks["client_id"]
                if "api_key" in ks:
                    config["api_key"] = ks["api_key"]
                if "notes_mapping" in ks:
                    config["notes_mapping"] = ks["notes_mapping"]
    
    return config


def ima_call(path, body, client_id, api_key):
    """调用 IMA API"""
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(IMA_API_BASE + path, data=data)
    req.add_header("ima-openapi-clientid", client_id)
    req.add_header("ima-openapi-apikey", api_key)
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  [ERROR] API call failed: {e}")
        return {"code": -1, "msg": str(e)}


def append_to_note(note_name, content, config):
    """追加内容到指定笔记"""
    if note_name not in config["notes_mapping"]:
        print(f"  [SKIP] Unknown note: {note_name}")
        return False
    
    doc_id = config["notes_mapping"][note_name]
    
    # 构建带时间戳的内容
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    full_content = f"\n\n---\n\n## {timestamp}\n\n{content}"
    
    # 调用 API
    body = {
        "doc_id": doc_id,
        "content_format": 1,
        "content": full_content
    }
    
    result = ima_call("openapi/note/v1/append_doc", body, 
                      config["client_id"], config["api_key"])
    
    if result.get("code") == 0:
        print(f"  [OK] {note_name}")
        return True
    else:
        print(f"  [FAIL] {note_name}: {result.get('msg', 'unknown error')}")
        return False


def sync_file_to_notes(file_path, note_name, config):
    """同步文件内容到指定笔记"""
    if not os.path.exists(file_path):
        print(f"  [ERROR] File not found: {file_path}")
        return False
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if not content.strip():
        print(f"  [SKIP] Empty file: {file_path}")
        return False
    
    # 获取文件名作为标题
    filename = os.path.basename(file_path)
    
    formatted_content = f"### {filename}\n\n{content}"
    return append_to_note(note_name, formatted_content, config)


def sync_all(config, workspace_path):
    """同步所有内容到 IMA"""
    print("=== IMA Sync Started ===\n")
    
    workspace = workspace_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. 同步 MEMORY.md 到 AI记忆库
    print("1. AI记忆库 (MEMORY.md)...")
    memory_file = os.path.join(workspace, "MEMORY.md")
    if os.path.exists(memory_file):
        sync_file_to_notes(memory_file, "AI记忆库", config)
    else:
        print("  [SKIP] MEMORY.md not found")
    
    time.sleep(0.5)
    
    # 2. 同步 learnings 到 经验总结
    print("\n2. 经验总结 (.learnings/)...")
    learnings_dir = os.path.join(workspace, ".learnings")
    if os.path.exists(learnings_dir):
        for filename in os.listdir(learnings_dir):
            if filename.endswith(".md"):
                file_path = os.path.join(learnings_dir, filename)
                sync_file_to_notes(file_path, "经验总结", config)
                time.sleep(0.3)
    else:
        print("  [SKIP] .learnings/ not found")
    
    print("\n=== Sync Complete ===")


def main():
    parser = argparse.ArgumentParser(description="IMA Knowledge Sync Tool")
    parser.add_argument("--note", help="Sync to specific note (e.g., 日记)")
    parser.add_argument("--file", help="Sync specific file to note")
    parser.add_argument("--workspace", help="Workspace directory path")
    parser.add_argument("--config", help="Config file path")
    args = parser.parse_args()
    
    config = load_config()
    workspace = args.workspace
    
    if args.file and args.note:
        # 指定文件和笔记
        print(f"Syncing {args.file} to {args.note}...")
        sync_file_to_notes(args.file, args.note, config)
    elif args.note:
        # 只同步指定笔记
        print(f"Appending to {args.note}...")
        content = input("Enter content (Ctrl+D to finish):\n")
        append_to_note(args.note, content, config)
    else:
        # 同步所有
        sync_all(config, workspace)


if __name__ == "__main__":
    main()
