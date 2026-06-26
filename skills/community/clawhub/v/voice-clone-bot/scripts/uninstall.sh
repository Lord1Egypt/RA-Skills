#!/bin/bash
# 卸载与环境清理脚本 (全引擎版)
# 使用: bash scripts/uninstall.sh [选项]
#
# 选项:
#   --all           卸载全部引擎与环境（默认行为）
#   --engine NAME   仅卸载指定引擎的源码（保留 venv 和基础环境）
#   --purge         彻底删除，包括全局模型权重（数 GB）

set -e

CDIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$CDIR"

# 读取可选配置，保证清理的端口与运行时一致
CONFIG_FILE="${TTS_CONFIG_FILE:-$CDIR/.env}"
if [ -f "$CONFIG_FILE" ]; then
    set -a
    # shellcheck disable=SC1090
    source "$CONFIG_FILE"
    set +a
fi
TTS_SERVER_PORT="${TTS_SERVER_PORT:-8000}"

MODE="all"
PURGE_MODELS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --engine) MODE="engine"; ENGINE_NAME="$2"; shift 2 ;;
        --purge)  PURGE_MODELS=true; shift ;;
        --all)    MODE="all"; shift ;;
        *)        echo "未知选项: $1"; exit 1 ;;
    esac
done

echo "=== voice-clone-bot 卸载与清理 ==="

# -----------------------------------------------
# 1. 杀死所有后台守护进程
# -----------------------------------------------
echo ""
echo "[1/5] 终止后台服务进程..."

PIDS=$(lsof -t -i:"$TTS_SERVER_PORT" 2>/dev/null || echo "")
if [ -n "$PIDS" ]; then
    kill -9 $PIDS 2>/dev/null || true
    echo "    ✓ 已关闭端口 $TTS_SERVER_PORT 的进程 (PID: $PIDS)"
else
    echo "    - 端口 $TTS_SERVER_PORT 未被占用"
fi
pkill -f "python app.py" 2>/dev/null && echo "    ✓ 已清理残留 app.py 进程" || true

# 清理守护日志
rm -f server/daemon_server.log
# 清理生成的临时音频
rm -rf server/generated_audio

# -----------------------------------------------
# 2. 按模式清理引擎源码
# -----------------------------------------------
echo ""
echo "[2/5] 清理引擎源码..."

remove_engine_source() {
    local name="$1"
    local dir=""
    case "$name" in
        cosyvoice) dir="venv/CosyVoice" ;;
        chattts)   dir="venv/ChatTTS" ;;
        openvoice) dir="venv/OpenVoice" ;;
        f5)        echo "    - F5-TTS 通过 pip 安装，将随 venv 一起清除"; return ;;
        *)         echo "    ! 未知引擎: $name"; return ;;
    esac
    if [ -d "$dir" ]; then
        rm -rf "$dir"
        echo "    ✓ 已删除 $name 源码: $dir"
    else
        echo "    - $name 源码不存在，跳过"
    fi
}

if [ "$MODE" = "engine" ]; then
    remove_engine_source "$ENGINE_NAME"
elif [ "$MODE" = "all" ]; then
    # 删除整个 venv（包含所有引擎源码）
    echo "[3/5] 删除 Python 虚拟环境 (venv)..."
    if [ -d "venv" ]; then
        rm -rf venv
        echo "    ✓ 已删除 venv（释放数 GB 空间）"
    else
        echo "    - venv 不存在"
    fi
fi

# -----------------------------------------------
# 3. 卸除 OpenClaw 技能注册
# -----------------------------------------------
echo ""
echo "[4/5] 卸除 OpenClaw 技能注册..."
SKILL_LINK="$HOME/.openclaw/skills/voice-clone-bot"
if [ -L "$SKILL_LINK" ] || [ -d "$SKILL_LINK" ]; then
    rm -rf "$SKILL_LINK"
    echo "    ✓ 已拔除技能注册: $SKILL_LINK"
else
    echo "    - 未找到技能注册"
fi

# -----------------------------------------------
# 4. 可选：清除全局模型权重
# -----------------------------------------------
echo ""
echo "[5/5] 全局模型权重..."
MODEL_DIR="$HOME/.openclaw/models/voice-clone"
if [ "$PURGE_MODELS" = true ]; then
    if [ -d "$MODEL_DIR" ]; then
        rm -rf "$MODEL_DIR"
        echo "    ✓ 已彻底删除全局模型权重: $MODEL_DIR"
    fi
else
    if [ -d "$MODEL_DIR" ]; then
        echo "    - 保留全局模型权重（数 GB，避免重复下载）"
        echo "      如需彻底清理，请使用: bash scripts/uninstall.sh --purge"
    fi
fi

echo ""
echo "=== 清理完毕！==="
if [ "$MODE" = "engine" ]; then
    echo "已卸载引擎: $ENGINE_NAME"
    echo "venv 基础环境保留，可直接安装其他引擎。"
else
    echo "所有环境已还原。重新安装请运行: bash scripts/auto_installer.sh"
fi
