#!/data/data/com.termux/files/usr/bin/bash
# Auto-start AI Agent Gateway on device boot
# Install: copy to ~/.termux/boot/agent-gateway and chmod +x
# Adjust SCRIPT path below to match your setup

# Wait for Wi-Fi to connect
sleep 15

# Source profile for PATH + venv
source /data/data/com.termux/files/home/.profile 2>/dev/null || true

# === CONFIG: point this to your run-gateway.sh ===
SCRIPT="/data/data/com.termux/files/home/.agent/scripts/run-gateway.sh"
# =================================================

bash "$SCRIPT"
