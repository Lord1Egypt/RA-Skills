#!/usr/bin/env bash
# 一次性准备：创建本地虚拟环境并安装依赖（幂等）
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$SKILL_DIR/.venv"
MIRROR="${ZHIQI_PIP_MIRROR:-https://pypi.tuna.tsinghua.edu.cn/simple}"
MIN_MINOR=9

# 挑出【版本最高且 >= 3.9】的解释器
find_python() {
  local best="" best_score=-1
  for c in python3.13 python3.12 python3.11 python3.10 python3.9 python3 python "${ZHIQI_PYTHON:-}"; do
    [ -n "$c" ] || continue
    command -v "$c" >/dev/null 2>&1 || continue
    local mm maj min score
    mm="$("$c" -c 'import sys;print("%d %d"%sys.version_info[:2])' 2>/dev/null || echo "")"
    [ -n "$mm" ] || continue
    maj="$(echo "$mm" | awk '{print $1}')"; min="$(echo "$mm" | awk '{print $2}')"
    [ "$maj" = "3" ] || continue
    [ "$min" -ge "$MIN_MINOR" ] || continue
    score=$((maj * 1000 + min))
    if [ "$score" -gt "$best_score" ]; then best="$c"; best_score="$score"; fi
  done
  [ -n "$best" ] && { echo "$best"; return 0; }
  return 1
}

PY="$(find_python)" || { echo "未找到 Python 3.9+，请安装后重试" >&2; exit 3; }
echo "[bootstrap] 使用解释器: $PY ($("$PY" -c 'import sys;print("%d.%d"%sys.version_info[:2])'))"

VENV_PY="$VENV_DIR/bin/python"
if [ -x "$VENV_PY" ]; then
  VV="$("$VENV_PY" -c 'import sys;print("%d %d"%sys.version_info[:2])' 2>/dev/null || echo "0 0")"
  VMaj="$(echo "$VV" | awk '{print $1}')"; VMin="$(echo "$VV" | awk '{print $2}')"
  if [ "$VMaj" != "3" ] || [ "$VMin" -lt "$MIN_MINOR" ]; then
    echo "[bootstrap] 现有虚拟环境 Python 版本过低，重建"
    rm -rf "$VENV_DIR"
  fi
fi

if [ ! -x "$VENV_DIR/bin/python" ]; then
  echo "[bootstrap] 创建虚拟环境 $VENV_DIR"
  "$PY" -m venv "$VENV_DIR"
fi
VENV_PY="$VENV_DIR/bin/python"

echo "[bootstrap] 安装依赖 cryptography / requests"
"$VENV_PY" -m pip install -q --disable-pip-version-check -i "$MIRROR" --upgrade pip 2>/dev/null || true
"$VENV_PY" -m pip install -q --disable-pip-version-check -i "$MIRROR" cryptography requests

VENDOR="$SKILL_DIR/vendor"
if [ ! -d "$VENDOR/zhiqi_agent" ] || [ ! -d "$VENDOR/zhiqi_mcp" ]; then
  SRC="${ZHIQI_AGENT_SRC:-}"
  if [ -z "$SRC" ] && [ -f "$SKILL_DIR/.source" ]; then SRC="$(cat "$SKILL_DIR/.source")"; fi
  if [ -n "$SRC" ] && [ -d "$SRC/zhiqi_agent" ]; then
    mkdir -p "$VENDOR"
    cp -R "$SRC/zhiqi_agent" "$VENDOR/" 2>/dev/null || true
    cp -R "$SRC/zhiqi_mcp" "$VENDOR/" 2>/dev/null || true
    echo "[bootstrap] 已内置 Python 包 -> $VENDOR"
  else
    # 正常发布的技能包**自带** vendor/，不会走到这里。
    # 走到这里说明安装不完整（例如手动只拷贝了 SKILL.md 与 scripts/），
    # 因此给出面向用户的重装建议，而不是把我们内部的开发脚本名甩给用户。
    echo "安装不完整：缺少内置包目录 $VENDOR。" >&2
    echo "请重新安装本技能（应为自包含包）：" >&2
    echo "  openclaw skills install zhiqi-agent      # 或重新执行你使用的安装方式" >&2
    exit 3
  fi
fi

"$VENV_PY" -c "import sys, cryptography, requests; print('[bootstrap] 就绪 Python', sys.version.split()[0], '| cryptography', cryptography.__version__)"
