#!/bin/bash
# run_tts.sh - The universal automated entry point for Voice Clone processing

# Navigate to the root of the skill repository safely
CDIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$CDIR"

# 0. Load optional runtime config from .env
CONFIG_FILE="${TTS_CONFIG_FILE:-$CDIR/.env}"
if [ -f "$CONFIG_FILE" ]; then
    set -a
    # shellcheck disable=SC1090
    source "$CONFIG_FILE"
    set +a
fi

TTS_SERVER_HOST="${TTS_SERVER_HOST:-127.0.0.1}"
TTS_SERVER_PORT="${TTS_SERVER_PORT:-8000}"
export TTS_SERVER_HOST
export TTS_SERVER_PORT
SERVER_BASE_URL="http://${TTS_SERVER_HOST}:${TTS_SERVER_PORT}"

# 1. Self-healing environment check
if [ ! -d "venv" ]; then
    echo "[!] 推理沙箱环境不存在。正在为您（Agent）自主安装依赖并配置 OpenClaw 全局环境变量..." >&2
    bash scripts/auto_installer.sh
fi

source venv/bin/activate

# 2. Daemon monitoring and self-ignition (Lazy Load)
# Check if the FastAPI endpoint is alive
if ! curl -m 2 -s "${SERVER_BASE_URL}/openapi.json" > /dev/null; then
    echo "[!] 推理后台引擎离线或初次启动，正在脱壳（nohup）为您点燃 PyTorch 大端..." >&2
    
    export HF_HOME="$HOME/.openclaw/models/voice-clone"
    
    cd server
    nohup $CDIR/venv/bin/python app.py > daemon_server.log 2>&1 &
    DAEMON_PID=$!
    cd ..
    
    echo "[*] 后台 PID $DAEMON_PID 已托管。等待模型从磁盘/HuggingFace完全载入显存 (请耐心等待大约20-40秒)..." >&2
    
    # Block until the server breathes
    READY=false
    for i in {1..120}; do
        if curl -m 2 -s "${SERVER_BASE_URL}/openapi.json" > /dev/null; then
            READY=true
            echo "[*] 端口监测：微服务就绪 (${TTS_SERVER_HOST}:${TTS_SERVER_PORT})，大模型已成功挂载。" >&2
            break
        fi
        sleep 1
    done
    
    if [ "$READY" = false ]; then
        echo "Error: 模型自激失败或拉取超时，请检查 server/daemon_server.log 并提示用户！" >&2
        exit 1
    fi
fi

# 3. Transparently pass all arguments to the actual communication client securely
#    This script expects: --text "..." --ref_audio "..."
$CDIR/venv/bin/python scripts/tts_client.py "$@"
