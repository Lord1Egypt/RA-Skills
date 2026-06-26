#!/usr/bin/env bash
set -euo pipefail

VOICE_HTTPS_PORT="${VOICE_HTTPS_PORT:-8443}"

# Input validation
if ! [[ "$VOICE_HTTPS_PORT" =~ ^[0-9]+$ ]] || (( VOICE_HTTPS_PORT < 1 || VOICE_HTTPS_PORT > 65535 )); then
  echo "ERROR: VOICE_HTTPS_PORT must be a valid port (1-65535)" >&2
  exit 1
fi

systemctl --user is-active openclaw-voice-https.service
curl -sk "https://127.0.0.1:${VOICE_HTTPS_PORT}/chat?session=main" -o /dev/null -w 'https:%{http_code}\n'
echo 'status:done'
