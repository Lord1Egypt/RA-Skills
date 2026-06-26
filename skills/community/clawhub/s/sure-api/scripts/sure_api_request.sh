#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   sure_api_request.sh GET /api/v1/accounts
#   sure_api_request.sh POST /api/v1/transactions -d '{...}'
#
# Requires env vars (in secure/api-fillin.env):
#   SURE_BASE_URL
#   SURE_API_KEY

METHOD=${1:-}
PATH_=${2:-}
shift 2 || true

if [[ -z "${METHOD}" || -z "${PATH_}" ]]; then
  echo "Usage: $0 <METHOD> <PATH> [curl-args...]" >&2
  exit 2
fi

# Load env if available
ENV_FILE="/root/.openclaw/workspace/secure/api-fillin.env"
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

: "${SURE_BASE_URL:?Missing SURE_BASE_URL}"
: "${SURE_API_KEY:?Missing SURE_API_KEY}"

BASE="${SURE_BASE_URL%/}"
URL="$BASE$PATH_"

curl -sS \
  -H "X-Api-Key: $SURE_API_KEY" \
  -H 'Accept: application/json' \
  -X "$METHOD" \
  "$URL" \
  "$@"
