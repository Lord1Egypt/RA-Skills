# -*- coding: utf-8 -*-
"""
定时任务配置 —— 硬件感知、零脚本文件。

关键点（遵守「禁止 .ps1/.sh/.bat 等可执行文件」约束）：
  - Windows：用 Python 直接调用系统自带的 `schtasks` 命令创建计划任务，不生成 .ps1。
  - macOS/Linux：用 Python 调用 `crontab` 写入一行命令，不生成 .sh。
  - 任务内容固定为 `python cli.py autopilot`（每日自动进化 + 沉淀 + 健康巡检）。

并发与执行节奏由 hardware.get_plan() 决定，避免在低配机上加负担。
"""

from __future__ import annotations

import os
import subprocess
import sys

from . import config, hardware

TASK_NAME = "ZwjhMemoryEvolution"


def _cli_command() -> str:
    py = sys.executable or "python3"
    cli = str(config.ZWJH_DIR.parent / "scripts" / "cli.py")
    # 退回：若 cli.py 不在预期位置，用技能目录推导
    if not os.path.exists(cli):
        here = os.path.dirname(os.path.abspath(__file__))
        cli = os.path.join(here, "cli.py")
    return f'"{py}" "{cli}" autopilot'


def setup_daily(hour: int = 23, minute: int = 0) -> dict:
    plan = hardware.get_plan()
    cmd = _cli_command()
    log = str(config.ZWJH_DIR / "autopilot.log")

    if sys.platform.startswith("win"):
        # 用 schtasks 直接注册，不落 .ps1
        # /tr 内部的引号必须转义为 \"，否则路径含空格时任务无法正确注册
        trigger = f"{hour:02d}:{minute:02d}"
        tr_escaped = cmd.replace('"', '\\"')
        schtasks = (
            f'schtasks /create /tn "{TASK_NAME}" /tr "{tr_escaped}" '
            f'/sc daily /st {trigger} /f /rl LIMITED'
        )
        try:
            proc = subprocess.run(schtasks, shell=True, capture_output=True, text=True)
            ok = proc.returncode == 0
            return {"ok": ok, "platform": "windows", "command": schtasks,
                    "output": (proc.stdout or proc.stderr)[:300], "plan": plan["tier"]}
        except Exception as e:
            return {"ok": False, "platform": "windows", "error": str(e)[:200]}
    else:
        # Unix：写 crontab，不落 .sh
        line = f"{minute} {hour} * * * {cmd} >> \"{log}\" 2>&1\n"
        try:
            cur = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
            existing = cur.stdout if cur.returncode == 0 else ""
            if TASK_NAME_MARKER in existing:
                # 已存在，先移除旧行
                existing = _strip_old(existing)
            new_cron = existing + f"# {TASK_NAME_MARKER}\n" + line
            proc = subprocess.run(["crontab", "-"], input=new_cron,
                                  capture_output=True, text=True)
            ok = proc.returncode == 0
            return {"ok": ok, "platform": "unix", "line": line,
                    "output": (proc.stdout or proc.stderr)[:300], "plan": plan["tier"]}
        except Exception as e:
            return {"ok": False, "platform": "unix", "error": str(e)[:200]}


TASK_NAME_MARKER = "zwjh-memory-evolution"


def _strip_old(cron_text: str) -> str:
    out = []
    skip = False
    for line in cron_text.splitlines(keepends=True):
        if TASK_NAME_MARKER in line:
            skip = True
            continue
        if skip and line.strip() == "":
            skip = False
            continue
        if skip:
            continue
        out.append(line)
    return "".join(out)


def remove() -> dict:
    if sys.platform.startswith("win"):
        proc = subprocess.run(f'schtasks /delete /tn "{TASK_NAME}" /f',
                              shell=True, capture_output=True, text=True)
        return {"ok": proc.returncode == 0, "platform": "windows",
                "output": (proc.stdout or proc.stderr)[:200]}
    else:
        try:
            cur = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
            existing = cur.stdout if cur.returncode == 0 else ""
            new_cron = _strip_old(existing)
            proc = subprocess.run(["crontab", "-"], input=new_cron,
                                  capture_output=True, text=True)
            return {"ok": proc.returncode == 0, "platform": "unix"}
        except Exception as e:
            return {"ok": False, "platform": "unix", "error": str(e)[:200]}


def status() -> dict:
    if sys.platform.startswith("win"):
        proc = subprocess.run(f'schtasks /query /tn "{TASK_NAME}"',
                              shell=True, capture_output=True, text=True)
        return {"exists": proc.returncode == 0, "platform": "windows",
                "output": (proc.stdout or proc.stderr)[:200]}
    else:
        cur = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        existing = cur.stdout if cur.returncode == 0 else ""
        return {"exists": TASK_NAME_MARKER in existing, "platform": "unix"}


if __name__ == "__main__":
    import json
    print(json.dumps(setup_daily(), ensure_ascii=False, indent=2))
