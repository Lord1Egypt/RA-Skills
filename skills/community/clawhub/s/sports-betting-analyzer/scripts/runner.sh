#!/bin/bash
# 体育彩票分析助手 - OpenClaw 集成脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 检查虚拟环境
if [ ! -d "$SKILL_DIR/venv" ]; then
    python3 -m venv "$SKILL_DIR/venv"
    source "$SKILL_DIR/venv/bin/activate"
    pip install numpy -q
else
    source "$SKILL_DIR/venv/bin/activate"
fi

# 运行分析脚本
cd "$SKILL_DIR"
python3 scripts/analyze.py "$@"