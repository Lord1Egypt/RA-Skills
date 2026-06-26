#!/data/data/com.termux/files/usr/bin/bash
# Health check: auto-restart gateway if down
# Usage: bash <skill_dir>/scripts/healthcheck.sh

# === CONFIG ===
SESSION_NAME="agent-gw"
LOG_DIR="$HOME/.agent/logs"
SCRIPT_PATH="$HOME/.agent/scripts/run-gateway.sh"
# ===============

mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/healthcheck.log"

if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "[$(date)] ⚠️ Gateway down! Restarting..." >> "$LOG"
  bash "$SCRIPT_PATH" >> "$LOG" 2>&1
  echo "[$(date)] ✅ Restart done." >> "$LOG"
else
  echo "[$(date)] ✅ Gateway is alive." >> "$LOG"
fi
