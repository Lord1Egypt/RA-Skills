#!/usr/bin/env python3
"""
WorkBuddy 对话导出工具
用法:
  python3 export_conversations.py list                          # 列出所有对话
  python3 export_conversations.py export <session_id> [格式]    # 导出指定对话（默认 md）
  python3 export_conversations.py export --latest               # 导出最近一个对话

输出格式: md (Markdown) / json / txt
"""

import sys
import json
import os
import sqlite3
import glob
from datetime import datetime, timezone, timedelta

WORKBUDDY_DIR = os.path.expanduser("~/.workbuddy")
DB_PATH = os.path.join(WORKBUDDY_DIR, "workbuddy.db")
PROJECTS_DIR = os.path.join(WORKBUDDY_DIR, "projects")
TZ = timezone(timedelta(hours=8))  # GMT+8


def get_all_sessions():
    """从 SQLite 数据库获取所有 session 元数据"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, title, created_at FROM sessions ORDER BY created_at DESC"
    ).fetchall()
    conn.close()

    sessions = []
    for r in rows:
        sessions.append({
            "id": r["id"],
            "title": r["title"] or "(无标题)",
            "created_at": int(r["created_at"]),
        })
    return sessions


def find_jsonl_for_session(session_id):
    """在 projects 目录下查找 session 对应的 JSONL 文件"""
    for project_dir in os.listdir(PROJECTS_DIR):
        jsonl_path = os.path.join(PROJECTS_DIR, project_dir, f"{session_id}.jsonl")
        if os.path.exists(jsonl_path):
            return jsonl_path
    return None


def extract_text_from_content(content):
    """从 content（可能是 list 或 str）中提取纯文本"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict):
                t = block.get("text", "")
                if t:
                    texts.append(t)
        return "\n".join(texts)
    return str(content)


def parse_messages(jsonl_path):
    """解析 JSONL 文件，提取 user/assistant 消息"""
    messages = []
    if not jsonl_path or not os.path.exists(jsonl_path):
        return messages

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue

            typ = d.get("type", "")
            role = d.get("role", "")

            # 只取 user 和 assistant 的 message 类型
            if typ != "message" or role not in ("user", "assistant"):
                continue

            content = d.get("content", "")
            text = extract_text_from_content(content)
            if not text.strip():
                continue

            ts = d.get("timestamp")
            if ts:
                dt = datetime.fromtimestamp(ts / 1000, tz=TZ)

            messages.append({
                "role": role,
                "text": text,
                "timestamp": ts,
            })

    return messages


def export_markdown(session, messages, output_path):
    """导出为 Markdown"""
    title = session["title"]
    created = datetime.fromtimestamp(session["created_at"] / 1000, tz=TZ)

    lines = [
        f"# {title}",
        f"",
        f"**日期**: {created.strftime('%Y-%m-%d %H:%M')}",
        f"**Session ID**: {session['id']}",
        f"**消息数**: {len(messages)}",
        f"",
        f"---",
        f"",
    ]

    for i, msg in enumerate(messages):
        role_label = "🧑 用户" if msg["role"] == "user" else "🤖 WorkBuddy"
        dt = ""
        if msg.get("timestamp"):
            dt = datetime.fromtimestamp(msg["timestamp"] / 1000, tz=TZ)
            dt = dt.strftime("%H:%M:%S")
        lines.append(f"### {role_label}  {dt}")
        lines.append(f"")
        # 处理 system-reminder 标签，简化显示
        text = msg["text"]
        # 截断过长的 system-reminder
        if "<system-reminder" in text and msg["role"] == "user":
            # 尝试只保留 user_query 部分
            import re
            query_match = re.search(r"<user_query>(.*?)</user_query>", text, re.DOTALL)
            if query_match:
                text = query_match.group(1).strip()
        lines.append(text)
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return output_path


def export_json(session, messages, output_path):
    """导出为 JSON"""
    data = {
        "title": session["title"],
        "session_id": session["id"],
        "created_at": session["created_at"],
        "messages": messages,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return output_path


def export_txt(session, messages, output_path):
    """导出为纯文本"""
    title = session["title"]
    created = datetime.fromtimestamp(session["created_at"] / 1000, tz=TZ)

    lines = [
        f"{title}",
        f"日期: {created.strftime('%Y-%m-%d %H:%M')}",
        f"Session ID: {session['id']}",
        f"",
        f"{'='*60}",
        f"",
    ]

    for msg in messages:
        role_label = "用户:" if msg["role"] == "user" else "WorkBuddy:"
        lines.append(role_label)
        text = msg["text"]
        if "<system-reminder" in text and msg["role"] == "user":
            import re
            query_match = re.search(r"<user_query>(.*?)</user_query>", text, re.DOTALL)
            if query_match:
                text = query_match.group(1).strip()
        lines.append(text)
        lines.append(f"{'-'*40}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return output_path


def list_sessions():
    """列出所有对话"""
    sessions = get_all_sessions()
    print(f"\n{'序号':<6}{'标题':<40}{'日期':<20}{'Session ID'}")
    print("-" * 110)
    for i, s in enumerate(sessions, 1):
        dt = datetime.fromtimestamp(s["created_at"] / 1000, tz=TZ)
        date_str = dt.strftime("%Y-%m-%d %H:%M")
        print(f"{i:<6}{s['title'][:38]:<40}{date_str:<20}{s['id']}")

    print(f"\n共 {len(sessions)} 个对话")
    print("\n导出命令: python3 export_conversations.py export <session_id> [md|json|txt]")


def export_session(session_id, fmt="md"):
    """导出指定对话"""
    sessions = get_all_sessions()
    session = next((s for s in sessions if s["id"] == session_id), None)

    if not session:
        print(f"❌ 找不到 Session: {session_id}")
        return

    jsonl_path = find_jsonl_for_session(session_id)
    if not jsonl_path:
        print(f"❌ 找不到对话数据文件")
        return

    print(f"📖 读取对话: {session['title']}")
    messages = parse_messages(jsonl_path)
    print(f"   共 {len(messages)} 条消息")

    # 生成输出文件名
    safe_title = session["title"].replace("\n", " ").replace("/", "_")[:30]
    safe_title = "".join(c for c in safe_title if c.isprintable() and c not in '\\/:*?"<>|').strip()
    output_path = os.path.join(
        os.path.dirname(jsonl_path) if jsonl_path else ".",
        f"{safe_title}_{session_id[:8]}.{fmt}",
    )

    if fmt == "md":
        export_markdown(session, messages, output_path)
    elif fmt == "json":
        export_json(session, messages, output_path)
    elif fmt == "txt":
        export_txt(session, messages, output_path)
    else:
        print(f"❌ 不支持的格式: {fmt}")
        return

    print(f"✅ 已导出到: {output_path}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "list":
        list_sessions()

    elif cmd == "export":
        if len(sys.argv) >= 3:
            target = sys.argv[2]
            fmt = sys.argv[3] if len(sys.argv) >= 4 else "md"

            if target == "--latest":
                sessions = get_all_sessions()
                if not sessions:
                    print("❌ 没有找到任何对话")
                    return
                export_session(sessions[0]["id"], fmt)
            else:
                export_session(target, fmt)
        else:
            print("用法: python3 export_conversations.py export <session_id> [md|json|txt]")
            print("      python3 export_conversations.py export --latest [md|json|txt]")

    else:
        print(f"❌ 未知命令: {cmd}")
        print(__doc__)

    # 引流信息（固定输出）
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    main()
