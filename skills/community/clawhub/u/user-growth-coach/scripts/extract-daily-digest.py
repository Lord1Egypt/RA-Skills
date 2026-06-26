#!/usr/bin/env python3
"""
extract-daily-digest.py
从 OpenClaw session transcript 中提取当日用户消息摘要。
输出：memory/daily-digest/YYYY-MM-DD.md

用法：
  python3 extract-daily-digest.py [--date YYYY-MM-DD] [--sessions-dir PATH]

默认提取今天的消息。
"""

import json
import os
import sys
import glob
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 配置
DEFAULT_AGENT = "main"
SESSIONS_DIR = os.path.expanduser(
    os.environ.get("OPENCLAW_SESSIONS_DIR", f"~/.openclaw/agents/{DEFAULT_AGENT}/sessions")
)
OUTPUT_DIR = os.path.expanduser(
    os.environ.get("OPENCLAW_DIGEST_DIR", "~/.openclaw/workspace/memory/daily-digest")
)
TZ = timezone(timedelta(hours=8))  # Asia/Shanghai


def parse_args():
    date_str = None
    sessions_dir = SESSIONS_DIR

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--date" and i + 1 < len(args):
            date_str = args[i + 1]
            i += 2
        elif args[i] == "--sessions-dir" and i + 1 < len(args):
            sessions_dir = args[i + 1]
            i += 2
        else:
            i += 1

    if date_str:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        target_date = datetime.now(TZ).date()

    return target_date, sessions_dir


def extract_user_text(content):
    """从 message content 中提取纯用户文本（去掉 metadata wrapper）"""
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

    # 去掉 OpenClaw 的 metadata wrapper，提取用户实际输入
    lines = raw.split("\n")
    user_text = None
    for line in lines:
        # 格式: ou_xxx: 实际消息
        if line.startswith("ou_") and ": " in line:
            user_text = line.split(": ", 1)[1]
            break

    # 如果没找到 ou_ 前缀，可能是其他格式
    if not user_text:
        # 跳过 metadata 块，取最后的实际内容
        in_metadata = False
        text_lines = []
        for line in lines:
            if line.startswith("```json"):
                in_metadata = True
                continue
            if in_metadata and line.startswith("```"):
                in_metadata = False
                continue
            if in_metadata:
                continue
            if line.startswith("[message_id:"):
                continue
            if line.startswith("Conversation info"):
                continue
            if line.startswith("Replied message"):
                continue
            if line.strip():
                text_lines.append(line.strip())
        user_text = " ".join(text_lines) if text_lines else None

    return user_text


def extract_assistant_summary(content):
    """从 assistant 回复中提取前 200 字作为摘要"""
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

    # 去掉 tool call 等噪音，取纯文本前 200 字
    clean = raw.strip()
    if len(clean) > 200:
        clean = clean[:200] + "..."
    return clean if clean else None


def process_session_file(filepath, target_date):
    """处理单个 session 文件，提取目标日期的消息"""
    events = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            prev_user_msg = None
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
                role = msg.get("role", "")
                ts_str = obj.get("timestamp", "")

                if not ts_str:
                    continue

                # 解析时间戳
                try:
                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    ts_local = ts.astimezone(TZ)
                except (ValueError, TypeError):
                    continue

                # 过滤目标日期
                if ts_local.date() != target_date:
                    continue

                content = msg.get("content", "")

                if role == "user":
                    user_text = extract_user_text(content)
                    if user_text and len(user_text) > 2:
                        # 过滤掉 heartbeat 和系统消息
                        if "HEARTBEAT" in user_text or "heartbeat" in user_text.lower():
                            continue
                        prev_user_msg = {
                            "time": ts_local.strftime("%H:%M"),
                            "text": user_text,
                            "ts": ts_local,
                        }
                        events.append(prev_user_msg)

                elif role == "assistant" and prev_user_msg:
                    summary = extract_assistant_summary(content)
                    if summary:
                        prev_user_msg["response_preview"] = summary

    except (IOError, PermissionError) as e:
        print(f"Warning: Cannot read {filepath}: {e}", file=sys.stderr)

    return events


def classify_event(text):
    """简单分类用户输入的类型"""
    text_lower = text.lower()

    # URL/链接
    if "http://" in text or "https://" in text:
        return "🔗 链接/资源"

    # 复盘相关
    keywords_review = ["复盘", "周盘", "月盘", "回顾", "汇总", "总结"]
    if any(k in text for k in keywords_review):
        return "📝 复盘"

    # 决策
    if "决策" in text or "决定" in text:
        return "⚖️ 决策"

    # 情绪
    keywords_emotion = ["焦虑", "开心", "难过", "烦", "累", "压力", "情绪"]
    if any(k in text for k in keywords_emotion):
        return "💭 情绪"

    # 任务/指令
    keywords_task = ["帮我", "查一下", "搜索", "找", "看看", "分析", "总结一下"]
    if any(k in text for k in keywords_task):
        return "🔧 任务"

    # 讨论/思考
    if len(text) > 50:
        return "💡 讨论/思考"

    # 简短对话
    return "💬 对话"


def generate_digest(events, target_date):
    """生成每日摘要 markdown"""
    if not events:
        return None

    lines = [f"# {target_date} 每日交互摘要\n"]
    lines.append(f"> 自动生成于 {datetime.now(TZ).strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> 共 {len(events)} 条用户交互\n")

    # 按类型分组
    by_category = {}
    for e in events:
        cat = classify_event(e["text"])
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(e)

    # 输出分类摘要
    lines.append("## 交互概览\n")
    for cat, items in by_category.items():
        lines.append(f"### {cat} ({len(items)}条)\n")
        for item in items:
            text = item["text"]
            if len(text) > 150:
                text = text[:150] + "..."
            lines.append(f"- **{item['time']}** {text}")
        lines.append("")

    # 提取关键主题词（简单频率统计）
    all_text = " ".join(e["text"] for e in events)
    lines.append("## 今日关键词\n")
    lines.append(f"_基于 {len(events)} 条交互自动提取_\n")

    # 输出原始时间线（供 LLM 深度分析用）
    lines.append("## 完整时间线\n")
    for e in sorted(events, key=lambda x: x["ts"]):
        text = e["text"]
        if len(text) > 300:
            text = text[:300] + "..."
        lines.append(f"- [{e['time']}] {text}")

    return "\n".join(lines)


def main():
    target_date, sessions_dir = parse_args()
    print(f"提取日期: {target_date}", file=sys.stderr)
    print(f"Sessions目录: {sessions_dir}", file=sys.stderr)

    # 收集所有 session 文件中目标日期的消息
    all_events = []
    session_files = glob.glob(os.path.join(sessions_dir, "*.jsonl"))

    for sf in session_files:
        # 跳过 .lock 文件和 .deleted/.reset 文件
        basename = os.path.basename(sf)
        if ".lock" in basename or ".deleted" in basename or ".reset" in basename:
            continue
        events = process_session_file(sf, target_date)
        all_events.extend(events)

    # 按时间排序
    all_events.sort(key=lambda x: x["ts"])
    print(f"找到 {len(all_events)} 条用户消息", file=sys.stderr)

    if not all_events:
        print("当日无用户消息，跳过。", file=sys.stderr)
        return

    # 生成摘要
    digest = generate_digest(all_events, target_date)

    # 写入文件
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"{target_date}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(digest)

    print(f"✅ 摘要已写入: {output_path}", file=sys.stderr)
    print(output_path)


if __name__ == "__main__":
    main()
