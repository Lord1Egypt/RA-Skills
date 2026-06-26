#!/usr/bin/env python3
"""
parse_session.py — Session JSONL 文件解析器

用途：从 OpenClaw session 存档文件中提取对话内容。
能处理被截断的文件（session reset 时正在写入的行不完整）。

用法：
  python3 parse_session.py <session.jsonl> [limit]
  python3 parse_session.py <session.jsonl> --tail 20
  python3 parse_session.py <session.jsonl> --keyword "未完成" --context 2
"""

import json
import sys
import os
from pathlib import Path


def is_message_entry(obj):
    """判断是否是消息条目（跳过头部 metadata 行）"""
    if not isinstance(obj, dict):
        return False
    if obj.get("type") != "message":
        return False
    msg = obj.get("message", {})
    return isinstance(msg, dict) and msg.get("role") in ("user", "assistant")


def extract_text_content(content):
    """从 content 数组中提取纯文本，处理多种类型"""
    if not isinstance(content, list):
        return ""
    texts = []
    for c in content:
        if not isinstance(c, dict):
            continue
        t = c.get("type")
        if t == "text":
            texts.append(c.get("text", ""))
        elif t == "thinking":
            texts.append(f"[思考] {c.get('thinking', '')}")
        elif t == "toolCall":
            texts.append(f"[工具调用] {c.get('name', 'unknown')}")
        elif t == "toolResult":
            # toolResult 内容可能很大，只取前200字
            result = str(c.get("content", ""))[:200]
            texts.append(f"[工具结果] {result}")
    return " ".join(texts)


def parse_session_file(path, limit=None, keyword=None, context_lines=0):
    """
    解析 session JSONL 文件。
    
    Args:
        path: JSONL 文件路径
        limit: 只返回最近 N 条消息
        keyword: 只返回包含关键词的消息
        context_lines: 关键词匹配的上下文行数
    
    Returns:
        [(timestamp, role, content), ...]
    """
    path = Path(path)
    if not path.exists():
        print(f"文件不存在: {path}", file=sys.stderr)
        return []

    # 策略1：文件完整，直接按行解析
    records = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if is_message_entry(obj):
                    msg = obj["message"]
                    ts = obj.get("timestamp", "")
                    role = msg.get("role")
                    content = extract_text_content(msg.get("content", []))
                    if content:
                        records.append((ts, role, content))
    except Exception as e:
        pass

    # 如果解析成功且文件完整，直接返回
    if records:
        return apply_filters(records, limit, keyword, context_lines)

    # 策略2：文件被截断，从尾部反向读取
    return parse_truncated_tail(path, limit, keyword, context_lines)


def parse_truncated_tail(path, limit=None, keyword=None, context_lines=0):
    """
    从文件尾部反向解析，处理截断的 JSON 行。
    每次从文件尾部往前读一批数据，找到完整的 JSON 对象。
    """
    records = []
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            
            # 从尾部开始，每次读 4KB
            chunk_size = 4096
            leftover = b""
            
            while f.tell() > 0:
                read_start = max(0, f.tell() - chunk_size)
                read_len = f.tell() - read_start
                f.seek(read_start)
                chunk = f.read(read_len)
                f.seek(read_start)
                
                if leftover:
                    chunk = chunk + leftover
                
                # 按行分割（从后往前）
                lines = chunk.split(b"\n")
                leftover = lines[0] if len(lines) > 1 else b""
                
                # 解析除了最后一行（可能不完整）之外的所有行
                for line in reversed(lines[1:]):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line.decode("utf-8"))
                        if is_message_entry(obj):
                            msg = obj["message"]
                            ts = obj.get("timestamp", "")
                            role = msg.get("role")
                            content = extract_text_content(msg.get("content", []))
                            if content:
                                records.append((ts, role, content))
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        continue
                
                if read_start == 0:
                    break
    except Exception as e:
        print(f"反向解析失败: {e}", file=sys.stderr)

    # 反转（从旧到新）
    records.reverse()
    return apply_filters(records, limit, keyword, context_lines)


def apply_filters(records, limit, keyword, context_lines):
    """应用 limit 和 keyword 过滤"""
    if keyword:
        filtered = []
        for i, (ts, role, content) in enumerate(records):
            if keyword.lower() in content.lower():
                # 包含上下文行
                start = max(0, i - context_lines)
                end = min(len(records), i + context_lines + 1)
                for j in range(start, end):
                    if records[j] not in filtered:
                        filtered.append(records[j])
        records = filtered
    elif limit:
        records = records[-limit:]
    
    return records


def format_records(records):
    """格式化输出"""
    if not records:
        return "（无内容）"
    
    lines = []
    for ts, role, content in records:
        role_label = "👤" if role == "user" else "🤖"
        # 截断过长内容
        if len(content) > 500:
            content = content[:500] + "..."
        lines.append(f"[{ts}] {role_label} {content}")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    path = sys.argv[1]
    limit = None
    keyword = None
    context = 0
    
    # 简单参数解析
    for arg in sys.argv[2:]:
        if arg == "--tail" and sys.argv[sys.argv.index(arg) + 1:]:
            limit = int(sys.argv[sys.argv.index(arg) + 1])
        elif arg == "--keyword" and sys.argv[sys.argv.index(arg) + 1:]:
            keyword = sys.argv[sys.argv.index(arg) + 1]
        elif arg == "--context" and sys.argv[sys.argv.index(arg) + 1:]:
            context = int(sys.argv[sys.argv.index(arg) + 1])
    
    records = parse_session_file(path, limit=limit, keyword=keyword, context_lines=context)
    print(format_records(records))


if __name__ == "__main__":
    main()
