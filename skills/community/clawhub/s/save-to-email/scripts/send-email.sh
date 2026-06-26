#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${ROOT_DIR}/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "${ROOT_DIR}/.env"
  set +a
fi

if [ "${#}" -ne 3 ]; then
  echo "Error: expected 3 arguments" >&2
  echo "Usage: $0 'recipient@example.com' 'Subject' 'HTML Content'" >&2
  exit 1
fi

if [ -z "${RESEND_API_KEY:-}" ]; then
  echo "Error: RESEND_API_KEY is not set" >&2
  exit 1
fi

if [ -z "${RESEND_FROM:-}" ]; then
  echo "Error: RESEND_FROM is not set" >&2
  exit 1
fi

RECIPIENT="$1"
SUBJECT="$2"
HTML_CONTENT="$3"

PAYLOAD="$(python3 - "$RESEND_FROM" "$RECIPIENT" "$SUBJECT" "$HTML_CONTENT" <<'PY'
import json
import sys

sender, recipient, subject, html = sys.argv[1:5]
print(json.dumps({
    "from": sender,
    "to": [recipient],
    "subject": subject,
    "html": html,
}, ensure_ascii=False))
PY
)"

RESPONSE="$(
  curl -sS -w "\n%{http_code}" \
    -X POST "https://api.resend.com/emails" \
    -H "Authorization: Bearer ${RESEND_API_KEY}" \
    -H "Content-Type: application/json" \
    --data-binary "${PAYLOAD}"
)"

HTTP_CODE="$(printf '%s\n' "${RESPONSE}" | tail -n1)"
BODY="$(printf '%s\n' "${RESPONSE}" | sed '$d')"

if [ "${HTTP_CODE}" = "200" ] || [ "${HTTP_CODE}" = "201" ]; then
  echo "Email sent successfully"
  echo "To: ${RECIPIENT}"
  echo "Subject: ${SUBJECT}"
  echo "Response: ${BODY}"
  exit 0
fi

echo "Failed to send email (HTTP ${HTTP_CODE})" >&2
echo "Response: ${BODY}" >&2
exit 1
