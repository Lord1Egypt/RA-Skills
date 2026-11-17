#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能进化（知行环）— Claude Code Stop Hook 提醒脚本（跨平台版）

在 Agent 完成响应时触发，若项目存在 .wiki/ 则输出记录提醒。
只输出提醒文本，不代替 Agent 判断，也不写入任何内容。

为什么需要 .py 版本：
    Claude Code 在 Windows 上执行 hook 命令时默认走 cmd.exe / PowerShell，
    而非 bash，因此 wiki_remind.sh 在 Windows 下会静默失效。本文件是
    Windows 环境的正确入口。

用法（Claude Code settings.json，项目级安装）:
    {"hooks": {"Stop": [{"hooks": [
        {"type": "command", "command": "python \\".wiki/scripts/wiki_remind.py\\""}
    ]}]}}

用户级安装则指向 ~/.claude/scripts/skill-evolution/wiki_remind.py
（不要用 ~/.workbuddy/... —— 那是 WorkBuddy 私有目录，未装 WorkBuddy 时不存在）。

环境变量:
    CLAUDE_PROJECT_DIR  Claude Code 运行时自动注入的项目根目录（可选）
"""

import os
import sys
from datetime import date

# Windows 下 stdout 默认编码是 GBK(cp936)，输出中文会抛 UnicodeEncodeError。
# 必须先切换为 UTF-8，否则 hook 会在 cmd.exe 下崩溃且无提示。
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass


def find_project_dir() -> str:
    """
    定位项目根目录，三级 fallback，缺一不可：

    1. CLAUDE_PROJECT_DIR —— Claude Code 运行时注入，最可靠。
    2. 当前工作目录 —— cron / 手动执行时靠它。
    3. 脚本自身位置 —— 项目级自包含安装时，本文件位于
       <项目>/.wiki/scripts/wiki_remind.py，上溯两级即项目根。
       这一级是关键兜底：某些沙箱化 shell 启动子进程时会强制 cd 回工作区，
       导致 os.getcwd() 与调用者目录不一致，前两级同时失效。

    三级都找不到 .wiki/ 时返回 cwd，由调用方判定为"无 wiki，静默退出"。
    """
    candidates = []

    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        candidates.append(env)
    candidates.append(os.getcwd())

    # 脚本自身位置：<项目>/.wiki/scripts/ -> 上溯两级
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        candidates.append(os.path.dirname(os.path.dirname(here)))
    except NameError:
        pass

    for c in candidates:
        if c and os.path.isdir(os.path.join(c, ".wiki")):
            return c
    return os.getcwd()


def main() -> int:
    project_dir = find_project_dir()

    if not os.path.isdir(os.path.join(project_dir, ".wiki")):
        return 0

    raw_file = os.path.join(project_dir, ".wiki", "raw", "%s.md" % date.today().isoformat())

    sys.stdout.write(
        "[技能进化] 会话结束前检查：本次任务是否有值得记录的经验？\n"
        "\n"
        "若有（踩坑、失败、或有效的解决技巧），追加到：\n"
        "  %s\n"
        "\n"
        "格式（≤10 行，只记关键决策点和异常，不记流水账）：\n"
        "  ### [HH:MM] 任务简述\n"
        "  - **域**：coding | data | research | debug | deploy\n"
        "  - **结果**：成功 / 失败 / 部分成功\n"
        "  - **轨迹**：1. [关键步骤] -> [结果]\n"
        "  - **关键观察**：[意外发现 / 踩坑点 / 有效技巧]\n"
        "\n"
        "若无值得记录的内容，忽略本提醒即可。\n" % raw_file
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
