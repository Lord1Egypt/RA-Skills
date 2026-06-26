#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[info]${NC} $*"; }
ok()    { echo -e "${GREEN}[ok]${NC} $*"; }
err()   { echo -e "${RED}[error]${NC} $*" >&2; }

NS_NAME=""
BINDING="KV"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --binding) BINDING="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $(basename "$0") <namespace-name> [--binding NAME]"
      exit 0 ;;
    -*) err "Unknown option: $1"; exit 1 ;;
    *) NS_NAME="$1"; shift ;;
  esac
done

if [[ -z "$NS_NAME" ]]; then
  err "Namespace name is required"
  echo "Usage: $(basename "$0") <namespace-name> [--binding NAME]"
  exit 1
fi

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  if wrangler whoami &>/dev/null; then
    info "Using OAuth credentials from wrangler login"
  else
    err "Not authenticated. export CLOUDFLARE_API_TOKEN=<token> or run: wrangler login"
    exit 1
  fi
fi

info "Creating KV namespace: $NS_NAME"
OUTPUT=$(wrangler kv namespace create "$NS_NAME" 2>&1)
echo "$OUTPUT"

# Extract namespace ID — try structured output first, fall back to hex pattern
NS_ID=$(echo "$OUTPUT" | grep -oE 'id = "[^"]*"' | head -1 | cut -d'"' -f2 || true)
if [[ -z "$NS_ID" ]]; then
  NS_ID=$(echo "$OUTPUT" | grep -oE '"id"\s*:\s*"[0-9a-f]+"' | head -1 | grep -oE '[0-9a-f]{32}' || true)
fi
if [[ -z "$NS_ID" ]]; then
  NS_ID=$(echo "$OUTPUT" | grep -oE '[0-9a-f]{32}' | head -1 || true)
fi

if [[ -z "$NS_ID" ]]; then
  err "Namespace may have been created but could not extract ID from wrangler output."
  err "Check manually: wrangler kv namespace list"
  exit 1
fi

ok "KV namespace created: $NS_NAME (ID: $NS_ID)"
echo ""
echo -e "${CYAN}Add to wrangler.toml:${NC}"
echo ""
echo "[[kv_namespaces]]"
echo "binding = \"$BINDING\""
echo "id = \"$NS_ID\""
