#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill-template CLI 入口。

复制为新技能后，请修改注释与常量，但保留当前分层结构：
cli（argv）→ service（业务编排）→ db（持久化）→ util（通用工具）。

jiangchang_skill_core 来自宿主共享 Python runtime 安装的 jiangchang-platform-kit，
不在技能仓库内 vendored。
"""
from __future__ import annotations

import os
import sys

if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

_scripts_dir = os.path.dirname(os.path.abspath(__file__))
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from jiangchang_skill_core.runtime_env import apply_cli_local_defaults

apply_cli_local_defaults()

from util.config_bootstrap import bootstrap_skill_config

bootstrap_skill_config()

from cli.app import main

if __name__ == "__main__":
    raise SystemExit(main())
