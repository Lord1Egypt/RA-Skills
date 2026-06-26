#!/bin/bash
# ChromaDB 服务启动脚本 — Semantic Memory 技能配套
# 用法：bash scripts/start_chroma.sh
# 或直接运行：chroma run --path ./vector_db --host 0.0.0.0 --port 8000 &

CHROMA_PATH="${CHROMA_PATH:-./vector_db}"
CHROMA_HOST="${CHROMA_HOST:-0.0.0.0}"
CHROMA_PORT="${CHROMA_PORT:-8000}"

# 检查是否已有进程在运行
if curl -s "http://localhost:${CHROMA_PORT}/api/v2/heartbeat" > /dev/null 2>&1; then
    echo "✅ ChromaDB 已在运行 (http://localhost:${CHROMA_PORT})"
else
    echo "🚀 启动 ChromaDB..."
    echo "   路径: $CHROMA_PATH"
    echo "   监听: $CHROMA_HOST:$CHROMA_PORT"

    # 优先用全局安装的 chroma
    if command -v chroma &> /dev/null; then
        CMD="chroma"
    elif [ -x "$HOME/.local/bin/chroma" ]; then
        CMD="$HOME/.local/bin/chroma"
    else
        CMD="python3 -m chromadb"
    fi

    nohup $CMD run \
        --path "$CHROMA_PATH" \
        --host "$CHROMA_HOST" \
        --port "$CHROMA_PORT" \
        > chroma_server.log 2>&1 &

    echo "   PID: $!"
    echo "   日志: ./chroma_server.log"
    sleep 2

    if curl -s "http://localhost:${CHROMA_PORT}/api/v2/heartbeat" > /dev/null 2>&1; then
        echo "✅ ChromaDB 启动成功！"
    else
        echo "❌ ChromaDB 启动失败，查看日志：tail chroma_server.log"
    fi
fi
