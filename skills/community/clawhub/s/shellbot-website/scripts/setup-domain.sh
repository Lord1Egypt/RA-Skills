#!/usr/bin/env bash
set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[info]${NC} $*"; }
ok()    { echo -e "${GREEN}[ok]${NC} $*"; }
warn()  { echo -e "${YELLOW}[warn]${NC} $*"; }
err()   { echo -e "${RED}[error]${NC} $*" >&2; }

usage() {
  echo "Usage: $(basename "$0") <worker-name> <custom-domain> [options]"
  echo ""
  echo "Options:"
  echo "  --zone-id <id>     Zone ID (skips automatic lookup)"
  echo "  --account-id <id>  Account ID (overrides CLOUDFLARE_ACCOUNT_ID)"
  echo ""
  echo "Examples:"
  echo "  $(basename "$0") my-worker example.com"
  echo "  $(basename "$0") my-worker app.example.com"
  echo "  $(basename "$0") my-worker example.com --zone-id abc123"
}

# Parse args
WORKER_NAME=""
CUSTOM_DOMAIN=""
ZONE_ID=""
ACCOUNT_ID="${CLOUDFLARE_ACCOUNT_ID:-}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --zone-id) ZONE_ID="$2"; shift 2 ;;
    --account-id) ACCOUNT_ID="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    -*) err "Unknown option: $1"; usage; exit 1 ;;
    *)
      if [[ -z "$WORKER_NAME" ]]; then
        WORKER_NAME="$1"
      elif [[ -z "$CUSTOM_DOMAIN" ]]; then
        CUSTOM_DOMAIN="$1"
      else
        err "Too many arguments"; usage; exit 1
      fi
      shift ;;
  esac
done

if [[ -z "$WORKER_NAME" || -z "$CUSTOM_DOMAIN" ]]; then
  err "Worker name and custom domain are required"
  usage
  exit 1
fi

# Auth check: this script uses the CF API directly, so it needs a token.
# Try to extract OAuth token from wrangler config if API token is not set.
if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  WRANGLER_CONFIG="$HOME/.wrangler/config/default.toml"
  if [[ -f "$WRANGLER_CONFIG" ]]; then
    OAUTH_TOKEN=$(grep -o 'oauth_token\s*=\s*"[^"]*"' "$WRANGLER_CONFIG" 2>/dev/null | head -1 | sed 's/.*"\(.*\)"/\1/' || true)
    if [[ -n "$OAUTH_TOKEN" ]]; then
      info "Using OAuth token from wrangler login (~/.wrangler/config/default.toml)"
      CLOUDFLARE_API_TOKEN="$OAUTH_TOKEN"
    fi
  fi
fi

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  err "This command requires CLOUDFLARE_API_TOKEN (uses CF API directly)."
  echo "  1. export CLOUDFLARE_API_TOKEN=<token>  (get from https://dash.cloudflare.com/profile/api-tokens)"
  echo "  2. wrangler login                       (OAuth via browser, token reused from ~/.wrangler/config/)"
  exit 1
fi

API_BASE="https://api.cloudflare.com/client/v4"
AUTH_HEADER="Authorization: Bearer $CLOUDFLARE_API_TOKEN"

# Get account ID if not set
if [[ -z "$ACCOUNT_ID" ]]; then
  info "Looking up account ID..."
  ACCOUNT_RESPONSE=$(curl -s -H "$AUTH_HEADER" "$API_BASE/accounts?page=1&per_page=5")
  # Use jq if available, fall back to python3, then grep
  if command -v jq &>/dev/null; then
    ACCOUNT_ID=$(echo "$ACCOUNT_RESPONSE" | jq -r '.result[0].id // empty' 2>/dev/null || true)
  elif command -v python3 &>/dev/null; then
    ACCOUNT_ID=$(echo "$ACCOUNT_RESPONSE" | python3 -c "import sys,json; r=json.load(sys.stdin); print(r['result'][0]['id'])" 2>/dev/null || true)
  else
    ACCOUNT_ID=$(echo "$ACCOUNT_RESPONSE" | grep -oE '"id"\s*:\s*"[0-9a-f]+"' | head -1 | grep -oE '[0-9a-f]{20,}' || true)
  fi
  if [[ -z "$ACCOUNT_ID" ]]; then
    err "Could not determine account ID. Set CLOUDFLARE_ACCOUNT_ID or pass --account-id"
    exit 1
  fi
  info "Using account: $ACCOUNT_ID"
fi

# Extract root domain for zone lookup (handles multi-level subdomains correctly)
DOMAIN_PARTS=(${CUSTOM_DOMAIN//./ })
NUM_PARTS=${#DOMAIN_PARTS[@]}
if [[ $NUM_PARTS -lt 2 ]]; then
  err "Invalid domain: $CUSTOM_DOMAIN"
  exit 1
fi
ROOT_DOMAIN="${DOMAIN_PARTS[$((NUM_PARTS-2))]}.${DOMAIN_PARTS[$((NUM_PARTS-1))]}"

# Get zone ID if not provided
if [[ -z "$ZONE_ID" ]]; then
  info "Looking up zone for $ROOT_DOMAIN..."
  ZONE_RESPONSE=$(curl -s -H "$AUTH_HEADER" "$API_BASE/zones?name=$ROOT_DOMAIN&account.id=$ACCOUNT_ID")
  if command -v jq &>/dev/null; then
    ZONE_ID=$(echo "$ZONE_RESPONSE" | jq -r '.result[0].id // empty' 2>/dev/null || true)
  elif command -v python3 &>/dev/null; then
    ZONE_ID=$(echo "$ZONE_RESPONSE" | python3 -c "import sys,json; r=json.load(sys.stdin); print(r['result'][0]['id'] if r['result'] else '')" 2>/dev/null || true)
  else
    ZONE_ID=$(echo "$ZONE_RESPONSE" | grep -oE '"id"\s*:\s*"[0-9a-f]+"' | head -1 | grep -oE '[0-9a-f]{20,}' || true)
  fi
  if [[ -z "$ZONE_ID" ]]; then
    err "Zone not found for $ROOT_DOMAIN"
    echo "  Make sure the domain is added to your Cloudflare account"
    echo "  Dashboard: https://dash.cloudflare.com/$ACCOUNT_ID"
    exit 1
  fi
  ok "Found zone: $ZONE_ID"
fi

# Add custom domain to worker via API
info "Adding custom domain '$CUSTOM_DOMAIN' to worker '$WORKER_NAME'..."

DOMAIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
  -H "$AUTH_HEADER" \
  -H "Content-Type: application/json" \
  "$API_BASE/accounts/$ACCOUNT_ID/workers/domains" \
  -d "{
    \"hostname\": \"$CUSTOM_DOMAIN\",
    \"zone_id\": \"$ZONE_ID\",
    \"service\": \"$WORKER_NAME\",
    \"environment\": \"production\"
  }")

HTTP_CODE=$(echo "$DOMAIN_RESPONSE" | tail -1)
BODY=$(echo "$DOMAIN_RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" == "200" || "$HTTP_CODE" == "201" ]]; then
  ok "Custom domain configured: $CUSTOM_DOMAIN → $WORKER_NAME"
  echo ""
  echo -e "${CYAN}Details:${NC}"
  echo "  Domain:  https://$CUSTOM_DOMAIN"
  echo "  Worker:  $WORKER_NAME"
  echo "  Zone:    $ZONE_ID"
  echo "  SSL:     Automatic (managed by Cloudflare)"
  echo ""
  info "DNS propagation typically takes 1-5 minutes for proxied domains"
  info "Check status: curl -sI https://$CUSTOM_DOMAIN"
else
  err "Failed to add custom domain (HTTP $HTTP_CODE)"
  if command -v jq &>/dev/null; then
    echo "$BODY" | jq . 2>/dev/null || echo "$BODY"
  elif command -v python3 &>/dev/null; then
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
  else
    echo "$BODY"
  fi
  echo ""
  warn "You can also add custom domains via the dashboard:"
  echo "  https://dash.cloudflare.com/$ACCOUNT_ID/workers/services/view/$WORKER_NAME/production/settings"
fi
