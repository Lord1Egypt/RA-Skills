#!/usr/bin/env python3
"""
虾尊 Memory 自动扫描脚本 V2
增量扫描：只处理新消息，不遗漏不重复
同时读取 user + assistant 消息
"""
import os
import json
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
TODAY = datetime.now().strftime("%Y-%m-%d")
MEMORY_FILE = os.path.join(MEMORY_DIR, f"{TODAY}.md")
LAST_WRITE_FILE = os.path.join(MEMORY_DIR, "last-memory-write.json")
SCAN_STATE_FILE = os.path.join(MEMORY_DIR, "scan-state.json")

# 从环境变量获取 transcript 路径（兼容不同 session key）
def find_latest_transcript():
    import glob
    sessions_dir = os.path.expanduser("~/.openclaw/agents/main/sessions/")
    files = sorted(glob.glob(os.path.join(sessions_dir, "*.jsonl")), key=os.path.getmtime, reverse=True)
    for f in files:
        # 跳过 subagent 和 cron 的 transcript，只找主会话
        basename = os.path.basename(f)
        if "subagent" not in basename and "cron" not in basename:
            return f
    return files[0] if files else None

TRANSCRIPT = os.environ.get("MEMORY_SCAN_TRANSCRIPT") or find_latest_transcript()

# 读取上次扫描状态
last_scan_ts = 0
if os.path.exists(SCAN_STATE_FILE):
    with open(SCAN_STATE_FILE, 'r') as f:
        state = json.load(f)
        last_scan_ts = state.get("last_scan_ts", 0)

print(f"[memory-scan] 上次扫描截止时间戳: {last_scan_ts}")

# 读取所有消息，只取 timestamp > last_scan_ts 的新消息
new_messages = []
latest_ts = last_scan_ts

if os.path.exists(TRANSCRIPT):
    with open(TRANSCRIPT, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            msg = entry.get("message", entry)
            
            # 获取时间戳
            ts = entry.get("ts", 0) or msg.get("timestamp", 0) or 0
            
            if isinstance(ts, str):
                try:
                    from email.utils import parsedate_to_datetime
                    ts = parsedate_to_datetime(ts).timestamp()
                except:
                    ts = 0
            
            if ts > latest_ts:
                latest_ts = ts
            
            # 只处理新消息
            if ts > last_scan_ts:
                role = msg.get("role", "")
                if role in ("user", "assistant"):
                    content = msg.get("content", "")
                    if isinstance(content, list):
                        for c in content:
                            if isinstance(c, dict) and c.get("type") == "text":
                                text = c.get("text", "")[:1500]
                                if text.strip():
                                    prefix = "[用户]" if role == "user" else "[AI]"
                                    new_messages.append(f"{prefix} {text}")
                    elif isinstance(content, str) and content.strip():
                        prefix = "[用户]" if role == "user" else "[AI]"
                        new_messages.append(f"{prefix} {content[:1500]}")
        except Exception as e:
            pass
else:
    print(f"[memory-scan] 警告：未找到 transcript 文件: {TRANSCRIPT}")

print(f"[memory-scan] 本次新消息数: {len(new_messages)}")

if not new_messages:
    print("[memory-scan] 无新消息")
    with open(SCAN_STATE_FILE, 'w') as f:
        json.dump({"last_scan_ts": latest_ts, "last_scan_time": datetime.now().isoformat()}, f, ensure_ascii=False)
    print(f"[memory-scan] 已更新scan-state.json (latest_ts={latest_ts})")
    exit(0)

# 输出供 AI 分析（最多30条）
print("\n=== 新消息 ===")
print("\n".join(new_messages[-30:]))

print("\n=== 当前Memory文件 ===")
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, 'r') as f:
        print(f.read()[:1000])
else:
    print("(今日文件不存在)")

print(f"\n=== 已更新 scan-state.ts = {latest_ts} ===")
with open(SCAN_STATE_FILE, 'w') as f:
    json.dump({"last_scan_ts": latest_ts, "last_scan_time": datetime.now().isoformat()}, f, ensure_ascii=False)
