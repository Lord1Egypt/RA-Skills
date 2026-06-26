#!/usr/bin/env bash
# Restart TTS server (Qwen3-TTS MLX)
# Usage: bash scripts/restart_tts.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_DIR/tts_server.log"
PORT=8100
MAX_WAIT=15
CONDA_ENV="d2l_3.13"
PYTHON="/opt/homebrew/Caskroom/miniconda/base/envs/${CONDA_ENV}/bin/python"

echo "============================================"
echo "  TTS Server Restart"
echo "============================================"

# Step 1: Kill existing tts_server.py processes
PIDS=$(pgrep -f "tts_server.py" 2>/dev/null || true)
if [ -n "$PIDS" ]; then
    echo "[1/4] Stopping existing TTS server (PID: $PIDS)..."
    kill $PIDS 2>/dev/null || true
    sleep 2
    # Force kill if still alive
    PIDS_REMAINING=$(pgrep -f "tts_server.py" 2>/dev/null || true)
    if [ -n "$PIDS_REMAINING" ]; then
        echo "  ⚠️  Force killing remaining processes..."
        kill -9 $PIDS_REMAINING 2>/dev/null || true
        sleep 1
    fi
    echo "  ✅ Old processes stopped."
else
    echo "[1/4] No existing TTS server found."
fi

# Step 2: Wait for port to be released
echo "[2/4] Waiting for port $PORT to be released..."
WAITED=0
while lsof -i :$PORT -sTCP:LISTEN >/dev/null 2>&1; do
    if [ $WAITED -ge $MAX_WAIT ]; then
        echo "  ❌ Port $PORT still in use after ${MAX_WAIT}s. Aborting."
        exit 1
    fi
    sleep 1
    WAITED=$((WAITED + 1))
done
echo "  ✅ Port $PORT is free."

# Step 3: Start TTS server in background
echo "[3/4] Starting TTS server (conda env: $CONDA_ENV)..."
cd "$PROJECT_DIR"
nohup $PYTHON scripts/tts_server.py > "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo "  PID: $NEW_PID"
echo "  Log: $LOG_FILE"

# Step 4: Wait for model to load and health check to pass
echo "[4/4] Waiting for model to load + warmup (this may take 60-120s)..."
WAITED=0
HEALTH_TIMEOUT=180
while [ $WAITED -lt $HEALTH_TIMEOUT ]; do
    RESP=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/health" 2>/dev/null || echo "000")
    if [ "$RESP" = "200" ]; then
        MODEL_LOADED=$(curl -s "http://localhost:$PORT/health" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('model_loaded', False))" 2>/dev/null || echo "False")
        if [ "$MODEL_LOADED" = "True" ]; then
            echo "  ✅ TTS server is ready!"
            echo ""
            echo "============================================"
            echo "  ✅ Restart complete!"
            echo "  URL:  http://localhost:$PORT"
            echo "  PID:  $NEW_PID"
            echo "  Log:  $LOG_FILE"
            echo "============================================"
            exit 0
        fi
    fi
    # Check if process is still alive
    if ! kill -0 $NEW_PID 2>/dev/null; then
        echo "  ❌ TTS server process died. Check log:"
        tail -20 "$LOG_FILE"
        exit 1
    fi
    printf "  ⏳ %ds...\r" $WAITED
    sleep 3
    WAITED=$((WAITED + 3))
done

echo "  ⚠️  Health check timed out after ${HEALTH_TIMEOUT}s."
echo "  Server may still be loading. Check: curl http://localhost:$PORT/health"
echo "  Tail log: tail -f $LOG_FILE"