#!/usr/bin/env python3
"""
Token Optimizer CLI — 统一命令行入口

实例侧命令 (纯本地):
  route <prompt>          — 模型分级路由
  context <prompt>        — Context Lazy Loading 推荐
  generate-agents         — 生成优化的 AGENTS.md
  heartbeat               — 心跳优化配置

平台侧命令 (需要 DB):
  overview [days]         — 全平台用量概览
  report <instance> [days]— 单实例用量报告
  advisor                 — 套餐匹配建议
"""

import json
import sys
import os

# 确保可以导入同目录下的模块
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)


def cmd_route(args):
    from model_router import route
    if not args:
        print("用法: cli.py route <prompt> [provider]")
        return
    prompt = args[0]
    provider = args[1] if len(args) > 1 else "zai-proxy"
    result = route(prompt, provider)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_context(args):
    from context_optimizer import recommend
    if not args:
        print("用法: cli.py context <prompt>")
        return
    result = recommend(args[0])
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_generate_agents(args):
    from context_optimizer import generate_agents_md
    from pathlib import Path
    content = generate_agents_md()
    output = Path("AGENTS.md.optimized")
    output.write_text(content, encoding="utf-8")
    print(f"已生成 → {output}")


def cmd_heartbeat(args):
    from heartbeat_config import show_recommendation
    ttl = int(args[0]) if args else 60
    result = show_recommendation(ttl)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_overview(args):
    from usage_report import overview
    days = int(args[0]) if args else 30
    result = overview(days)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_report(args):
    from usage_report import instance_report
    if not args:
        print("用法: cli.py report <instance_name> [days]")
        return
    name = args[0]
    days = int(args[1]) if len(args) > 1 else 30
    result = instance_report(name, days)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_advisor(args):
    from quota_advisor import analyze_all
    result = analyze_all()
    print(json.dumps(result, indent=2, ensure_ascii=False))


COMMANDS = {
    # 实例侧 (纯本地)
    "route": ("模型分级路由", cmd_route),
    "context": ("Context Lazy Loading 推荐", cmd_context),
    "generate-agents": ("生成优化的 AGENTS.md", cmd_generate_agents),
    "heartbeat": ("心跳优化配置", cmd_heartbeat),
    # 平台侧 (需要 DB)
    "overview": ("全平台用量概览 [需要 DB]", cmd_overview),
    "report": ("单实例用量报告 [需要 DB]", cmd_report),
    "advisor": ("套餐匹配建议 [需要 DB]", cmd_advisor),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print("OpenClaw Token Optimizer CLI")
        print()
        print("实例侧命令 (纯本地):")
        for name, (desc, _) in list(COMMANDS.items())[:4]:
            print(f"  {name:20s} {desc}")
        print()
        print("平台侧命令 (需要 DB 连接):")
        for name, (desc, _) in list(COMMANDS.items())[4:]:
            print(f"  {name:20s} {desc}")
        print()
        print("示例:")
        print('  cli.py route "thanks!"')
        print('  cli.py context "设计一个架构"')
        print("  cli.py overview 7")
        print("  cli.py advisor")
        sys.exit(0)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command not in COMMANDS:
        print(f"未知命令: {command}")
        print(f"可用命令: {', '.join(COMMANDS.keys())}")
        sys.exit(1)

    _, handler = COMMANDS[command]
    handler(args)


if __name__ == "__main__":
    main()
