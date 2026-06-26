#!/usr/bin/env python3
"""
ultra-memory: n8n 集成节点
作为 n8n "Execute Command" 节点的 Python 脚本后端，
支持 init / log / recall 三种操作。

n8n 配置示例：
  Execute Command 节点
    命令: python3
    参数: /path/to/ultra-memory/integrations/n8n_nodes.py <operation> <args>

Operations:
  init --project <proj>                    → 返回 session_id
  log --session <id> --summary "..." --type <type> --detail '{}'
  recall --session <id> --query "..."
  profile --action read|update --field <field> --value <value>
"""

import json
import os
import sys
import re
from pathlib import Path

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))
_SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


def _run_script(script_name: str, args: list[str]) -> str:
    """运行脚本并返回输出"""
    import subprocess

    script_path = _SCRIPTS_DIR / script_name
    result = subprocess.run(
        [sys.executable, str(script_path)] + args,
        capture_output=True, text=True, timeout=30,
    )
    return result.stdout + result.stderr


def cmd_init(project: str) -> dict:
    """初始化会话"""
    output = _run_script("init.py", ["--project", project, "--resume"])

    session_id = None
    memory_ready = False

    for line in output.split("\n"):
        if "session_id:" in line:
            match = re.search(r"session_id:\s*(sess_\w+)", line)
            if match:
                session_id = match.group(1)
        if "MEMORY_READY" in line:
            memory_ready = True

    return {
        "success": memory_ready,
        "session_id": session_id,
        "output": output,
    }


def cmd_log(session_id: str, summary: str, op_type: str, detail: str = "{}") -> dict:
    """记录操作"""
    output = _run_script("log_op.py", [
        "--session", session_id,
        "--type", op_type,
        "--summary", summary,
        "--detail", detail,
    ])
    return {"success": True, "output": output}


def cmd_recall(session_id: str, query: str, top_k: int = 5) -> dict:
    """检索记忆"""
    output = _run_script("recall.py", [
        "--session", session_id,
        "--query", query,
        "--top-k", str(top_k),
    ])
    return {"success": True, "output": output}


def cmd_profile(action: str, field: str = None, value: str = None) -> dict:
    """读取或更新用户画像"""
    if action == "read":
        output = _run_script("evolve_profile.py", [])
        return {"success": True, "output": output}
    elif action == "update" and field and value:
        output = _run_script("evolve_profile.py", [
            "--field", field, "--value", value,
        ])
        return {"success": True, "output": output}
    return {"success": False, "error": "invalid profile command"}


# ── CLI ─────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: n8n_nodes.py <init|log|recall|profile> [args...]")
        sys.exit(1)

    operation = sys.argv[1].lower()
    args = sys.argv[2:]

    result = {}
    try:
        if operation == "init":
            project = next((a for a in args if a.startswith("--project=")),
                          "--project=default").split("=", 1)[1]
            result = cmd_init(project)

        elif operation == "log":
            session_id = next((a for a in args if a.startswith("--session=")),
                             None).split("=", 1)[1]
            summary = next((a for a in args if a.startswith("--summary=")),
                          "").split("=", 1)[1]
            op_type = next((a for a in args if a.startswith("--type=")),
                          "tool_call").split("=", 1)[1]
            detail = next((a for a in args if a.startswith("--detail=")),
                         "{}").split("=", 1)[1]
            result = cmd_log(session_id, summary, op_type, detail)

        elif operation == "recall":
            session_id = next((a for a in args if a.startswith("--session=")),
                             None).split("=", 1)[1]
            query = next((a for a in args if a.startswith("--query=")),
                        "").split("=", 1)[1]
            result = cmd_recall(session_id, query)

        elif operation == "profile":
            action = next((a for a in args if a.startswith("--action=")),
                         "read").split("=", 1)[1]
            field = next((a for a in args if a.startswith("--field=")),
                        None)
            field = field.split("=", 1)[1] if field else None
            value = next((a for a in args if a.startswith("--value=")),
                        None)
            value = value.split("=", 1)[1] if value else None
            result = cmd_profile(action, field, value)

        else:
            result = {"success": False, "error": f"unknown operation: {operation}"}

    except Exception as e:
        result = {"success": False, "error": str(e)}

    print(json.dumps(result, ensure_ascii=False, indent=2))
