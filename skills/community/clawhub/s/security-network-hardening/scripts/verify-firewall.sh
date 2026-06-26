#!/usr/bin/env bash
set -euo pipefail

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

need_cmd ufw
need_cmd ss

echo '== UFW status =='
sudo ufw status verbose || true

echo
echo '== Listening ports =='
ss -ltnp || true

echo
echo '== OpenClaw audit =='
openclaw security audit --deep || true

echo
echo '== OpenClaw gateway status =='
openclaw gateway status || true
