#!/usr/bin/env python3
"""
ultra-memory: Claude Code PostToolUse 自动捕获钩子
从 stdin 读取 Claude Code 传入的 hook payload（JSON），
自动调用 log_op.py 记录工具调用，无需手动触发。

配置方式（.claude/settings.json）:
  {
    "hooks": {
      "PostToolUse": [
        {
          "matcher": "Write|Edit|Bash|NotebookEdit",
          "hooks": [
            {
              "type": "command",
              "command": "python3 scripts/hook_capture.py"
            }
          ]
        }
      ]
    }
  }

环境变量:
  ULTRA_MEMORY_SESSION  — 当前会话 ID（必填）
  ULTRA_MEMORY_HOME     — 存储根目录（可选，默认 ~/.ultra-memory）
"""

import os
import sys
import json
import subprocess
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPTS_DIR = Path(__file__).parent
SESSION_ID = os.environ.get("ULTRA_MEMORY_SESSION", "")


def main():
    if not SESSION_ID:
        # 未配置会话 ID，静默退出（不阻塞 Claude Code 工具调用）
        sys.exit(0)

    # 读取 Claude Code 传入的 hook payload
    payload: dict = {}
    try:
        raw = sys.stdin.read()
        if raw.strip():
            payload = json.loads(raw)
    except Exception:
        pass

    tool_name = payload.get("tool_name", payload.get("tool", "unknown"))
    tool_input = payload.get("tool_input", payload.get("input", {}))

    # 根据工具类型推断 op_type 和摘要
    op_type = "tool_call"
    summary_parts = [f"[auto] {tool_name}"]

    if tool_name in ("Write", "NotebookEdit"):
        op_type = "file_write"
        path = tool_input.get("file_path", tool_input.get("notebook_path", ""))
        if path:
            summary_parts.append(path)
    elif tool_name == "Edit":
        op_type = "file_write"
        path = tool_input.get("file_path", "")
        if path:
            summary_parts.append(path)
    elif tool_name == "Bash":
        op_type = "bash_exec"
        cmd = tool_input.get("command", "")
        if cmd:
            summary_parts.append(cmd[:120])
    elif tool_name == "Read":
        op_type = "file_read"
        path = tool_input.get("file_path", "")
        if path:
            summary_parts.append(path)

    summary = " ".join(summary_parts)

    # 构建 detail（只保留关键字段，截断长值）
    detail = {}
    if tool_name in ("Write", "Edit", "NotebookEdit"):
        path = tool_input.get("file_path", tool_input.get("notebook_path", ""))
        if path:
            detail["path"] = path
    elif tool_name == "Bash":
        cmd = tool_input.get("command", "")
        if cmd:
            detail["cmd"] = cmd[:200]

    detail_json = json.dumps(detail, ensure_ascii=False)

    # 调用 log_op.py（子进程，失败静默忽略）
    python = sys.executable
    try:
        subprocess.run(
            [
                python,
                str(SCRIPTS_DIR / "log_op.py"),
                "--session", SESSION_ID,
                "--type", op_type,
                "--summary", summary[:200],
                "--detail", detail_json,
            ],
            timeout=5,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
