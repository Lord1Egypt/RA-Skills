#!/bin/bash
# Stable Feishu image send wrapper
# Usage: bash send_to_feishu.sh <image_path> <open_id>

set -euo pipefail

IMAGE_PATH="$1"
OPEN_ID="${2:-ou_22f2eefd5abe63e0cd67f4882cec06d4}"

if [ -z "$IMAGE_PATH" ]; then
  echo "Usage: $0 <image_path> [open_id]"
  exit 1
fi

APP_ID=$(python3 - <<'PY'
import json, pathlib
cfg=json.loads(pathlib.Path('/root/.openclaw/openclaw.json').read_text())
fei=cfg['channels']['feishu']
print(fei.get('appId') or fei.get('accounts',{}).get('default',{}).get('appId'))
PY
)

APP_SECRET=$(python3 - <<'PY'
import json, pathlib
cfg=json.loads(pathlib.Path('/root/.openclaw/openclaw.json').read_text())
fei=cfg['channels']['feishu']
print(fei.get('appSecret') or fei.get('accounts',{}).get('default',{}).get('appSecret'))
PY
)

DOMAIN=$(python3 - <<'PY'
import json, pathlib
cfg=json.loads(pathlib.Path('/root/.openclaw/openclaw.json').read_text())
fei=cfg['channels']['feishu']
print(fei.get('domain') or fei.get('accounts',{}).get('default',{}).get('domain') or 'feishu')
PY
)

python3 /root/.openclaw/workspace/skills/feishu-send-file/scripts/send_image.py \
  "$IMAGE_PATH" \
  "$OPEN_ID" \
  "$APP_ID" \
  "$APP_SECRET" \
  "$DOMAIN"
