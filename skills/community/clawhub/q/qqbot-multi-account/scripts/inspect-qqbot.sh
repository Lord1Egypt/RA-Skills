#!/usr/bin/env bash
set -euo pipefail

CONFIG="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
KNOWN="${QQBOT_KNOWN_USERS:-$HOME/.openclaw/qqbot/data/known-users.json}"

echo '== openclaw.service =='
if systemctl status openclaw.service --no-pager --lines=20 2>/dev/null; then
  :
else
  echo 'systemd status unavailable in current shell environment'
fi

echo
echo '== gateway port =='
python3 - <<'PY'
import json, os
p = os.environ.get('OPENCLAW_CONFIG_PATH') or os.path.expanduser('~/.openclaw/openclaw.json')
obj = json.load(open(p))
print(obj.get('gateway', {}).get('port'))
PY

echo
echo '== bindings/accounts =='
python3 - <<'PY'
import json, os
p = os.environ.get('OPENCLAW_CONFIG_PATH') or os.path.expanduser('~/.openclaw/openclaw.json')
obj = json.load(open(p))
print('bindings:')
for item in obj.get('bindings', []):
    print(' ', item)
print('accounts:')
for key, value in (obj.get('channels', {}).get('qqbot', {}).get('accounts', {}) or {}).items():
    print(f'  {key}: appId={value.get("appId")} secretFile={value.get("clientSecretFile")}')
PY

echo
if [ -f "$KNOWN" ]; then
  echo '== known users =='
  cat "$KNOWN"
else
  echo "known-users.json missing: $KNOWN"
fi
