#!/bin/bash
# SignaAI listener daemon — works on any machine with signaai-worker.json configured.
# Address is derived automatically from the worker passphrase.

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v launchctl >/dev/null 2>&1 && launchctl list | grep -q "io.signaai.listener"; then
  echo "io.signaai.listener is already managed by launchctl."
  echo "Use launchctl kickstart -k gui/\$(id -u)/io.signaai.listener to restart it."
  echo "Refusing to start a second foreground listener."
  exit 2
fi

exec python3 "$SKILL_DIR/scripts/listener.py" --network mainnet
