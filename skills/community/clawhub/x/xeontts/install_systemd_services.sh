#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEMD_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
TTS_UNIT_NAME="xeontts-tts.service"
NODE_UNIT_NAME="xeontts-node.service"
TTS_UNIT_PATH="$SYSTEMD_USER_DIR/$TTS_UNIT_NAME"
NODE_UNIT_PATH="$SYSTEMD_USER_DIR/$NODE_UNIT_NAME"
NODE_BIN="$(command -v node || true)"
TTS_BIN="$SKILL_DIR/venv/bin/xdp-tts-service"

[[ -n "$NODE_BIN" ]] || { echo "未找到 node" >&2; exit 1; }
[[ -x "$TTS_BIN" ]] || { echo "未找到 $TTS_BIN" >&2; exit 1; }
[[ -f "$SKILL_DIR/tts_config.json" ]] || { echo "未找到 tts_config.json" >&2; exit 1; }
[[ -f "$SKILL_DIR/config.json" ]] || { echo "未找到 config.json" >&2; exit 1; }

mkdir -p "$SYSTEMD_USER_DIR"

cat > "$TTS_UNIT_PATH" <<EOF
[Unit]
Description=Xeon TTS Flask Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$SKILL_DIR
ExecStart=$TTS_BIN --host 127.0.0.1 --port 5002 --config $SKILL_DIR/tts_config.json
Restart=always
RestartSec=3
Environment=HOME=$HOME
Environment=PATH=$HOME/.local/bin:$HOME/.npm-global/bin:$HOME/bin:/usr/local/bin:/usr/bin:/bin
Environment=XDP_TTS_CONFIG=$SKILL_DIR/tts_config.json

[Install]
WantedBy=default.target
EOF

cat > "$NODE_UNIT_PATH" <<EOF
[Unit]
Description=Xeon TTS Workflow Gateway
After=network-online.target $TTS_UNIT_NAME
Wants=network-online.target $TTS_UNIT_NAME

[Service]
Type=simple
WorkingDirectory=$SKILL_DIR
ExecStart=$NODE_BIN $SKILL_DIR/server.js
Restart=always
RestartSec=3
Environment=HOME=$HOME
Environment=PATH=$HOME/.local/bin:$HOME/.npm-global/bin:$HOME/bin:/usr/local/bin:/usr/bin:/bin

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now "$TTS_UNIT_NAME"
systemctl --user enable --now "$NODE_UNIT_NAME"
echo "xeontts 开机自启已启用"
