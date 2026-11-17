"""_paths.py — 持久化路径统一收口（K8s Pod 容器友好）

所有 skill-to-http 自身的持久化数据（config.json/server.log/server.pid/history.db/data/）
默认放在 workspace 内的隐藏目录，跟 PVC 持久化，容器重启不丢。

证书 / API Key 共享目录见 tls_auth.HTTP_ROOT（同样在 workspace 内）。

优先级：
  1. OPENCLAW_S2H_DATA_DIR 环境变量
  2. <workspace>/.skill-to-http/
  3. ~/.skill-to-http/（兜底，非 OpenClaw 环境）
"""

from __future__ import annotations

import os
from pathlib import Path


def detect_skill_to_http_root() -> Path:
    """探测 skill-to-http 持久化根目录。"""
    if env := os.environ.get("OPENCLAW_S2H_DATA_DIR"):
        return Path(env).expanduser()
    workspace = os.environ.get(
        "OPENCLAW_WORKSPACE",
        str(Path.home() / ".openclaw" / "workspace"),
    )
    ws_path = Path(workspace)
    if ws_path.exists() and (ws_path / "skills").exists():
        return ws_path / ".skill-to-http"
    return Path.home() / ".skill-to-http"


S2H_ROOT = detect_skill_to_http_root()

# 派生路径（所有脚本统一从这里取）
CONFIG_PATH = S2H_ROOT / "config.json"
DATA_DIR = S2H_ROOT / "data"
LOG_FILE = S2H_ROOT / "server.log"
PID_FILE = S2H_ROOT / "server.pid"
PORT_FILE = S2H_ROOT / "server.port"
HISTORY_DB = S2H_ROOT / "history.db"
DEPS_FILE = S2H_ROOT / "skill_deps.json"
CONSOLE_PID_FILE = S2H_ROOT / "console.pid"
CONSOLE_PORT_FILE = S2H_ROOT / "console.port"
SPEED_MODE_FILE = S2H_ROOT / "speed_mode.json"

SKILL_META_DIR = S2H_ROOT / 'skill_meta'
PARAMS_TEMPLATE_DIR = S2H_ROOT / 'params-template'
