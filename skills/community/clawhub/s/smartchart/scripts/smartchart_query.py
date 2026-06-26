#!/usr/bin/env python3
"""
smartchart_query.py - SmartChart 工具调用辅助脚本

用法:
    # 列出所有工具
    python smartchart_query.py list_tool

    # 执行具体工具（JSON 格式输出）
    python smartchart_query.py <tool_name> --format json

等同于:
    smartchart run_tool -n list_tool
    smartchart run_tool -n <tool_name> --format json
"""

import subprocess
import sys
import json
import argparse


def run_smartchart(tool_name: str, fmt: str = "json", extra_args: list = None) -> str:
    """执行 smartchart run_tool 命令并返回输出"""
    cmd = ["smartchart", "run_tool", "-n", tool_name, "--format", fmt]
    if extra_args:
        cmd.extend(extra_args)
    print(f"[执行命令] {' '.join(cmd)}", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[错误] {result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)
    return result.stdout


def try_parse_json(output: str):
    """从输出中提取 JSON 内容（跳过 INFO 日志行）"""
    lines = output.strip().splitlines()
    json_lines = []
    in_json = False
    for line in lines:
        if line.strip().startswith("[") or line.strip().startswith("{"):
            in_json = True
        if in_json:
            json_lines.append(line)
    json_str = "\n".join(json_lines)
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return output


def main():
    parser = argparse.ArgumentParser(
        description="SmartChart 数据查询辅助工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("tool_name", help="工具名称（数据集名），使用 list_tool 获取所有可用工具")
    parser.add_argument("--format", choices=["raw", "json", "array"], default="json", help="输出格式（默认 json）")
    parser.add_argument("--pretty", action="store_true", help="以格式化 JSON 输出结果")

    args, extra = parser.parse_known_args()

    output = run_smartchart(args.tool_name, fmt=args.format, extra_args=extra if extra else None)
    parsed = try_parse_json(output)

    if args.pretty and isinstance(parsed, (dict, list)):
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
    else:
        print(output)


if __name__ == "__main__":
    main()
