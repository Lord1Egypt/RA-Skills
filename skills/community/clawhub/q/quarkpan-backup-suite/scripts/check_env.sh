#!/usr/bin/env bash
set -euo pipefail

need() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "[OK] $1"
  else
    echo "[ERR] missing: $1"
    return 1
  fi
}

need bash
need tar
need sha256sum
need jq
need python3

if python3 - <<'PY' >/dev/null 2>&1
import httpx
PY
then
  echo "[OK] python httpx"
else
  echo "[ERR] missing python module: httpx"
fi

if [[ -x /root/.openclaw/workspace/scripts/backup/quark-openlist-upload.py ]]; then
  echo "[OK] quark-openlist-upload.py"
else
  echo "[WARN] quark-openlist-upload.py not found at expected path"
fi

if [[ -x /root/.openclaw/workspace/scripts/backup/.venv-quark/bin/quarkpan ]]; then
  echo "[OK] quarkpan auth/guard helper"
else
  echo "[WARN] quarkpan not found at expected path"
fi

if [[ -x /root/.openclaw/workspace/scripts/backup/.venv-tccli/bin/tccli ]]; then
  echo "[OK] tccli"
else
  echo "[WARN] tccli not found at expected path"
fi

if [[ -f /root/.openclaw/workspace/scripts/backup/backup.conf ]]; then
  if grep -q '^CLOUD_SPLIT_FALLBACK=0' /root/.openclaw/workspace/scripts/backup/backup.conf; then
    echo "[OK] split fallback disabled"
  else
    echo "[WARN] CLOUD_SPLIT_FALLBACK is not 0"
  fi
fi

echo "[DONE] env check finished"
