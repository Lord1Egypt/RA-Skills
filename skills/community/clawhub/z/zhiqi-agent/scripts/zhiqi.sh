#!/usr/bin/env bash
# 智契接入端运行器（Linux / macOS / Git Bash）
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR="$SKILL_DIR/vendor"
VENV_PY="$SKILL_DIR/.venv/bin/python"

# 0) 默认把 --home 指向技能自身的 .zhiqi：技能应当自包含。
#    不默认的话 CLI 会退到 ./.zhiqi（当前工作目录），于是"给这个技能配的模型"
#    可能和"实际调用读的配置"不是同一个 —— 症状是"明明配了模型，还报未申报"。
#    必须放在"复用全局 zhiqi"之前，否则装了全局命令时仍会用错 home。
HAS_HOME=0
for _a in "$@"; do [ "$_a" = "--home" ] && HAS_HOME=1; done
if [ "$HAS_HOME" = "0" ]; then
  set -- --home "$SKILL_DIR/.zhiqi" "$@"
fi

# 1) 已全局安装则直接复用
if command -v zhiqi >/dev/null 2>&1 && [ -z "${ZHIQI_FORCE_LOCAL:-}" ]; then
  exec zhiqi "$@"
fi

# 2) 确保本地环境就绪
NEED=1
if [ -x "$VENV_PY" ] && "$VENV_PY" -c 'import cryptography, requests' 2>/dev/null && [ -d "$VENDOR/zhiqi_agent" ]; then
  NEED=0
fi
if [ "$NEED" = "1" ]; then
  echo "[zhiqi] 首次运行，正在准备本地环境（约 10~30 秒）..." >&2
  bash "$SKILL_DIR/scripts/bootstrap.sh" >&2
fi

export PYTHONPATH="$VENDOR"
export PYTHONIOENCODING=utf-8
export PYTHONUTF8=1
exec "$VENV_PY" -m zhiqi_agent.cli "$@"
