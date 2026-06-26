#!/usr/bin/env python3
"""
save_test_script.py — 将录制的 session 保存为可重放的测试脚本

生成两种格式：
  1. Shell 脚本 (.sh / .bat)：直接调用 agent-browser 命令
  2. JSON 脚本（.test.json）：结构化测试用例，可被其他工具解析

用法:
    python save_test_script.py \
        --session <session_file.json> \
        --output-dir <输出目录> \
        --test-name "测试用例名称" \
        [--format shell|json|both]
"""

import argparse
import json
import os
import sys
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="将 session 保存为测试脚本")
    parser.add_argument("--session",    required=True, help="session JSON 文件路径")
    parser.add_argument("--output-dir", required=True, help="脚本输出目录")
    parser.add_argument("--test-name",  required=True, help="测试用例名称")
    parser.add_argument("--format",     default="both", choices=["shell", "json", "both"],
                        help="输出格式：shell / json / both（默认 both）")
    parser.add_argument("--description", default="", help="测试用例描述")
    return parser.parse_args()


def load_session(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sanitize_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in "._- " else "_" for c in name).strip().replace(" ", "_")


def generate_shell_script(session: dict, test_name: str, description: str) -> str:
    lines = [
        "#!/usr/bin/env bash",
        "# =========================================",
        f"# 测试脚本: {test_name}",
        f"# 描述: {description}",
        f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"# 原始 session: {session.get('session_id', 'unknown')}",
        "# =========================================",
        "",
        'set -e  # 任意步骤失败则退出',
        "",
        'echo "🚀 开始执行测试: ' + test_name + '"',
        "",
    ]

    for step in session.get("steps", []):
        num  = step["step_num"]
        desc = step["description"]
        cmd  = step["command"]
        lines.append(f'echo "▶ Step {num}: {desc}"')
        lines.append(cmd)
        lines.append("")

    lines += [
        'echo "✅ 测试执行完成: ' + test_name + '"',
        "",
    ]
    return "\n".join(lines)


def generate_bat_script(session: dict, test_name: str, description: str) -> str:
    lines = [
        "@echo off",
        "REM =========================================",
        f"REM 测试脚本: {test_name}",
        f"REM 描述: {description}",
        f"REM 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "REM =========================================",
        "",
        f'echo 开始执行测试: {test_name}',
        "",
    ]

    for step in session.get("steps", []):
        num  = step["step_num"]
        desc = step["description"]
        cmd  = step["command"]
        lines.append(f'echo Step {num}: {desc}')
        lines.append(cmd)
        lines.append("if errorlevel 1 goto :error")
        lines.append("")

    lines += [
        f'echo 测试执行完成: {test_name}',
        "exit /b 0",
        "",
        ":error",
        "echo 测试执行失败，请检查上述步骤",
        "exit /b 1",
    ]
    return "\n".join(lines)


def generate_json_script(session: dict, test_name: str, description: str) -> dict:
    steps = []
    for step in session.get("steps", []):
        steps.append({
            "step":        step["step_num"],
            "description": step["description"],
            "action":      _parse_action(step["command"]),
            "command":     step["command"],
            "selector":    step.get("selector", ""),
            "input_value": step.get("input_value", ""),
            "url":         step.get("url", ""),
            "expected":    "页面正常展示",
            "status":      step.get("status", "passed"),
        })

    return {
        "test_name":   test_name,
        "description": description,
        "generated_at": datetime.now().isoformat(),
        "session_id":  session.get("session_id", ""),
        "total_steps": len(steps),
        "steps":       steps,
    }


def _parse_action(command: str) -> str:
    """从 agent-browser 命令中提取动作类型。"""
    cmd = command.lower()
    if "navigate" in cmd or "open" in cmd or "goto" in cmd:
        return "navigate"
    if "click" in cmd:
        return "click"
    if "type" in cmd or "fill" in cmd or "input" in cmd:
        return "type"
    if "select" in cmd:
        return "select"
    if "scroll" in cmd:
        return "scroll"
    if "wait" in cmd:
        return "wait"
    if "assert" in cmd or "expect" in cmd or "check" in cmd:
        return "assert"
    return "action"


def main():
    args = parse_args()

    if not os.path.exists(args.session):
        print(f"❌ Session 文件不存在: {args.session}", file=sys.stderr)
        sys.exit(1)

    session  = load_session(args.session)
    os.makedirs(args.output_dir, exist_ok=True)
    safe_name = sanitize_filename(args.test_name)
    outputs   = []

    if args.format in ("shell", "both"):
        # 生成 .sh 脚本
        sh_content  = generate_shell_script(session, args.test_name, args.description)
        sh_path = os.path.join(args.output_dir, f"{safe_name}.sh")
        with open(sh_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(sh_content)
        outputs.append(sh_path)

        # 生成 Windows .bat 脚本
        bat_content = generate_bat_script(session, args.test_name, args.description)
        bat_path = os.path.join(args.output_dir, f"{safe_name}.bat")
        with open(bat_path, "w", encoding="utf-8", newline="\r\n") as f:
            f.write(bat_content)
        outputs.append(bat_path)

    if args.format in ("json", "both"):
        json_data = generate_json_script(session, args.test_name, args.description)
        json_path = os.path.join(args.output_dir, f"{safe_name}.test.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        outputs.append(json_path)

    print(f"✅ 测试脚本已保存:")
    for p in outputs:
        print(f"   📄 {p}")


if __name__ == "__main__":
    main()
