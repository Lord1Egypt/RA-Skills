#!/usr/bin/env python3
"""Novel Writer 统一 CLI 入口"""

import argparse
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent


def run_script(name: str, args: list[str]):
    script = SCRIPTS_DIR / f"{name}.py"
    if not script.exists():
        print(f"❌ 未知命令: {name}")
        available = sorted(p.stem for p in SCRIPTS_DIR.glob("*.py") if p.stem not in ("cli", "__init__"))
        print(f"   可用命令: {', '.join(available)}")
        sys.exit(1)
    import subprocess
    result = subprocess.run([sys.executable, str(script)] + args)
    sys.exit(result.returncode)


def main():
    p = argparse.ArgumentParser(
        prog="novel-writer",
        description="📖 长篇网络小说创作引擎 — 企业级 CLI",
    )
    p.add_argument("command", help="子命令")
    p.add_argument("args", nargs="*", help="子命令参数")

    aliases = {
        "check": "consistency_check",
        "drift": "outline_drift",
        "rhythm": "rhythm_check",
        "dialogue": "dialogue_tag_check",
        "hook": "chapter_hook_check",
        "title": "chapter_title_check",
        "opening": "opening_score",
        "paragraph": "paragraph_check",
        "foreshadow": "foreshadow_scan",
        "tension": "tension_forecast",
        "repeat": "repetition_check",
        "all": "run_all_checks",
        "config": "config_manager",
        "changelog": "changelog",
        "backup": "backup",
        "parallel": "run_parallel",
        "semantic": "semantic_check",
        "diff": "diff_check",
        "report": "html_report",
        "bench": "benchmark",
    }

    args = p.parse_args()
    cmd = aliases.get(args.command, args.command)
    run_script(cmd, args.args)


if __name__ == "__main__":
    main()
