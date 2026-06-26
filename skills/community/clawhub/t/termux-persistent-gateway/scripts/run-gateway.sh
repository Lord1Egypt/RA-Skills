#!/data/data/com.termux/files/usr/bin/bash
# Keep AI Agent Gateway alive on Termux (background, like WhatsApp/Telegram)
# Usage: bash <skill_dir>/scripts/run-gateway.sh

# === CONFIG ===
GATEWAY_CMD="openclaw gateway run"
SESSION_NAME="agent-gw"
LOG_DIR="$HOME/.agent/logs"
# ===============

mkdir -p "$LOG_DIR"

# Acquire wake lock to prevent CPU sleep
termux-wake-lock 2>/dev/null
echo "🔒 Wake lock acquired (CPU won't sleep)"

# Kill old session if exists
tmux kill-session -t "$SESSION_NAME" 2>/dev/null

# Start gateway in tmux
echo "🚀 Starting gateway in tmux..."
tmux new-session -d -s "$SESSION_NAME" -x 120 -y 40 \
  "$GATEWAY_CMD 2>&1 | tee $LOG_DIR/gateway-termux.log"

echo "✅ Gateway running in tmux session '$SESSION_NAME'"
echo "  Attach:  tmux attach -t $SESSION_NAME"
echo "  Detach:  Ctrl+B, D"
echo "  Logs:    tail -f $LOG_DIR/gateway-termux.log"
