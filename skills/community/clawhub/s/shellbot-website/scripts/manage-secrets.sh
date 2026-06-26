#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[info]${NC} $*"; }
ok()    { echo -e "${GREEN}[ok]${NC} $*"; }
err()   { echo -e "${RED}[error]${NC} $*" >&2; }

usage() {
  echo "Usage: $(basename "$0") <action> [args] [--env <environment>]"
  echo ""
  echo "Actions:"
  echo "  put <key> <value>     Add or update a secret"
  echo "  list                  List all secrets"
  echo "  delete <key>          Delete a secret"
  echo "  bulk <file.json>      Bulk upload secrets from JSON file"
  echo ""
  echo "Options:"
  echo "  --env, -e <env>       Target environment (staging, production)"
}

ACTION=""
KEY=""
VALUE=""
BULK_FILE=""
ENV=""

# Parse action first
if [[ $# -gt 0 ]]; then
  ACTION="$1"; shift
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env|-e) ENV="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    -*)
      err "Unknown option: $1"; usage; exit 1 ;;
    *)
      if [[ -z "$KEY" ]]; then
        KEY="$1"
      elif [[ -z "$VALUE" ]]; then
        VALUE="$1"
      fi
      shift ;;
  esac
done

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  if wrangler whoami &>/dev/null; then
    info "Using OAuth credentials from wrangler login"
  else
    err "Not authenticated. export CLOUDFLARE_API_TOKEN=<token> or run: wrangler login"
    exit 1
  fi
fi

ENV_FLAG=""
if [[ -n "$ENV" ]]; then
  ENV_FLAG="-e $ENV"
fi

case "$ACTION" in
  put)
    if [[ -z "$KEY" ]]; then
      err "Key is required: $(basename "$0") put <key> <value>"
      exit 1
    fi
    if [[ -z "$VALUE" ]]; then
      err "Value is required: $(basename "$0") put <key> <value>"
      err "Non-interactive mode only. Provide the value as an argument."
      exit 1
    fi
    echo "$VALUE" | wrangler secret put "$KEY" $ENV_FLAG
    ok "Secret '$KEY' set"
    ;;
  list)
    wrangler secret list $ENV_FLAG
    ;;
  delete)
    if [[ -z "$KEY" ]]; then
      err "Key is required: $(basename "$0") delete <key>"
      exit 1
    fi
    echo "y" | wrangler secret delete "$KEY" $ENV_FLAG
    ok "Secret '$KEY' deleted"
    ;;
  bulk)
    BULK_FILE="$KEY"  # First positional arg after "bulk" is the file path
    if [[ -z "$BULK_FILE" ]]; then
      err "File path is required: $(basename "$0") bulk <file.json>"
      exit 1
    fi
    if [[ ! -f "$BULK_FILE" ]]; then
      err "File not found: $BULK_FILE"
      exit 1
    fi
    # Validate JSON before uploading
    if command -v jq &>/dev/null; then
      if ! jq empty "$BULK_FILE" 2>/dev/null; then
        err "Invalid JSON in $BULK_FILE"
        exit 1
      fi
    elif command -v python3 &>/dev/null; then
      if ! python3 -c "import json; json.load(open('$BULK_FILE'))" 2>/dev/null; then
        err "Invalid JSON in $BULK_FILE"
        exit 1
      fi
    fi
    wrangler secret bulk "$BULK_FILE" $ENV_FLAG
    ok "Secrets uploaded from $BULK_FILE"
    ;;
  *)
    err "Unknown action: $ACTION"
    usage
    exit 1
    ;;
esac
