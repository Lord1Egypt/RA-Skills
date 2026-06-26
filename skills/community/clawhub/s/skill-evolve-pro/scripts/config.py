# -*- coding: utf-8 -*-
"""
config.py — 用户配置（从此文件读取配置，不上传到 ClawHub）
"""

from __future__ import annotations

import os
from pathlib import Path

# ── DeepSeek API 配置 ──────────────────────────────────────────────────────
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-bcf804f871284c66a1ecef3dffe665f3")

DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")

# ── Python 路径 ──────────────────────────────────────────────────────────
PYTHON_PATH = os.environ.get("PYTHON_PATH", "{{PYTHON_PATH}}")

# ── 工作区路径 ───────────────────────────────────────────────────────────
WORKSPACE = Path(os.environ.get(
    "OPENCLAW_WORKSPACE",
    os.path.join(os.path.expanduser("~"), ".jvs", "workspace")
))

# ── 技能目录 ─────────────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent.parent.resolve()

# ── 内部路径 ─────────────────────────────────────────────────────────────
STATE_DIR = SKILL_DIR / "state"
SCRIPTS_DIR = Path(__file__).parent.resolve()

DEFAULT_SESSION = WORKSPACE / "SESSION-STATE.md"
DEFAULT_TEMP = WORKSPACE / "temp"
DEFAULT_ROLLOUT = WORKSPACE / "temp" / "rollouts"
DEFAULT_TARGET_SKILL_DIR = WORKSPACE / "skills" / "robot-evolve"

DEFAULT_MAX_EDITS = 8
DEFAULT_AUTO_GATE = True
