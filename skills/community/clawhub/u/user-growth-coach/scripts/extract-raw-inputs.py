#!/usr/bin/env python3
"""
extract-raw-inputs.py
从 session transcript 中提取当日用户原始输入（去噪）。
输出纯文本，供 LLM 进一步总结。

用法：
  python3 extract-raw-inputs.py [--date YYYY-MM-DD]
  
输出到 stdout，供 cron 任务中 LLM 读取。
"""

import json
import os
import sys
import glob
from datetime import datetime, timedelta, timezone

DEFAULT_AGENT = "main"
SESSIONS_DIR = os.path.expanduser(
    os.environ.get("OPENCLAW_SESSIONS_DIR", f"~/.openclaw/agents/{DEFAULT_AGENT}/sessions")
)
TZ = timezone(timedelta(hours=8))


def parse_args():
    date_str = None
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--date" and i + 1 < len(args):
            date_str = args[i + 1]
            i += 2
        else:
            i += 1
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    return datetime.now(TZ).date()


def extract_user_text(content):
    """提取用户实际输入文本"""
    raw = ""
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                raw = item.get("text", "")
                break
    elif isinstance(content, str):
        raw = content
    if not raw:
        return None

    lines = raw.split("\n")
    
    # 提取 ou_xxx: 后面的内容
    user_text = None
    for line in lines:
        if line.startswith("ou_") and ": " in line:
            user_text = line.split(": ", 1)[1]
            break

    if not user_text:
        # 跳过 metadata，取实际内容
        in_meta = False
        text_parts = []
        for line in lines:
            if line.startswith("```json"):
                in_meta = True
                continue
            if in_meta and line.startswith("```"):
                in_meta = False
                continue
            if in_meta or line.startswith("[message_id:") or line.startswith("Conversation info") or line.startswith("Replied message"):
                continue
            if line.strip():
                text_parts.append(line.strip())
        user_text = " ".join(text_parts) if text_parts else None

    return user_text


def main():
    target_date = parse_args()
    events = []

    session_files = glob.glob(os.path.join(SESSIONS_DIR, "*.jsonl"))
    for sf in session_files:
        basename = os.path.basename(sf)
        if ".lock" in basename or ".deleted" in basename or ".reset" in basename:
            continue
        try:
            with open(sf, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if obj.get("type") != "message":
                        continue
                    msg = obj.get("message", {})
                    if msg.get("role") != "user":
                        continue
                    ts_str = obj.get("timestamp", "")
                    if not ts_str:
                        continue
                    try:
                        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                        ts_local = ts.astimezone(TZ)
                    except (ValueError, TypeError):
                        continue
                    if ts_local.date() != target_date:
                        continue
                    user_text = extract_user_text(msg.get("content", ""))
                    if user_text and len(user_text) > 2:
                        # 过滤 cron/heartbeat/system/session-startup 消息
                        skip_patterns = [
                            "HEARTBEAT", "heartbeat", "[cron:", 
                            "memsearch 自动索引", "Self-Evolution",
                            "A new session was started", "Execute your Session Startup",
                            "Read HEARTBEAT.md"
                        ]
                        if any(skip in user_text for skip in skip_patterns):
                            continue
                        events.append({
                            "time": ts_local.strftime("%H:%M"),
                            "text": user_text,
                            "ts": ts_local,
                        })
        except (IOError, PermissionError):
            continue

    events.sort(key=lambda x: x["ts"])

    # 输出纯文本时间线
    print(f"# {target_date} 用户交互原始记录")
    print(f"# 共 {len(events)} 条有效输入")
    print()
    for e in events:
        print(f"[{e['time']}] {e['text']}")
        print()


if __name__ == "__main__":
    main()
