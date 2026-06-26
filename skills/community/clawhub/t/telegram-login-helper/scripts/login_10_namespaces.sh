#!/usr/bin/env bash
set -euo pipefail

namespaces=(tg1 tg2 tg3 tg4 tg5 tg6 tg7 tg8 tg9 tg10)

echo "Telegram 10-account namespace login helper"
echo "This is interactive. Scan QR for each namespace in order."
echo

for ns in "${namespaces[@]}"; do
  echo "=================================================="
  echo "Namespace: $ns"
  if tdl chat ls -n "$ns" --limit 1 >/dev/null 2>&1; then
    echo "Status: already logged in"
    continue
  fi

  echo "Status: login required"
  echo "Running: tdl login -n $ns -T qr"
  tdl login -n "$ns" -T qr

  if tdl chat ls -n "$ns" --limit 1 >/dev/null 2>&1; then
    echo "Login OK: $ns"
  else
    echo "Login still not usable: $ns"
    echo "Stop here and retry this namespace before continuing."
    exit 1
  fi
  echo
  sleep 1
done

echo "All namespaces processed."
echo "Next step:"
echo "python3 /home/stevewu/.openclaw/workspace/skills/telegram-multi-account-monitor/scripts/tg_multi_account_monitor.py --list-namespaces"
