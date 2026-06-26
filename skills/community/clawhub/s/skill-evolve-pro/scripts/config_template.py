# -*- coding: utf-8 -*-
"""
config_template.py — 配置模板
复制此文件为 config.py 并填写你的配置

所有脚本优先读取 config.py 中的配置，
若无 config.py 则读取环境变量，
若环境变量也没有则使用占位符（会导致运行失败，需配置后使用）。
"""

from __future__ import annotations

import os
from pathlib import Path

# ── DeepSeek API 配置 ──────────────────────────────────────────────────────
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
if not DEEPSEEK_API_KEY:
    raise RuntimeError(
        "DEEPSEEK_API_KEY 未设置！\n"
        "方法1: 设置环境变量 DEEPSEEK_API_KEY\n"
        "方法2: 编辑本文件，填写上方的 DEEPSEEK_API_KEY"
    )

DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")

# ── Python 路径 ──────────────────────────────────────────────────────────
PYTHON_PATH = os.environ.get("PYTHON_PATH", "{{PYTHON_PATH}}")
# 示例（Windows）: C:\Users\YourName\AppData\Local\Programs\Python\Python310\python.exe
# 示例（Linux/Mac）: /usr/bin/python3

# ── 工作区路径 ───────────────────────────────────────────────────────────
# OpenClaw 工作区根目录（skill-evolve-pro 的父目录的父目录）
WORKSPACE = Path(os.environ.get(
    "OPENCLAW_WORKSPACE",
    os.path.join(os.path.expanduser("~"), ".jvs", "workspace")
))

# ── 技能目录 ─────────────────────────────────────────────────────────────
# skill-evolve-pro 安装目录
SKILL_DIR = Path(__file__).parent.parent.resolve()

# ── 内部路径 ─────────────────────────────────────────────────────────────
STATE_DIR = SKILL_DIR / "state"
SCRIPTS_DIR = Path(__file__).parent.resolve()

# 默认 SESSION-STATE.md 路径
DEFAULT_SESSION = WORKSPACE / "SESSION-STATE.md"

# 默认轨迹目录
DEFAULT_TEMP = WORKSPACE / "temp"
DEFAULT_ROLLOUT = WORKSPACE / "temp" / "rollouts"

# 默认目标技能目录（robot-evolve）
DEFAULT_TARGET_SKILL_DIR = WORKSPACE / "skills" / "robot-evolve"

# ── 调度器配置 ────────────────────────────────────────────────────────────
DEFAULT_MAX_EDITS = 8
DEFAULT_AUTO_GATE = True
