#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[info]${NC} $*"; }
ok()    { echo -e "${GREEN}[ok]${NC} $*"; }
err()   { echo -e "${RED}[error]${NC} $*" >&2; }

BUCKET_NAME=""
BINDING="BUCKET"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --binding) BINDING="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $(basename "$0") <bucket-name> [--binding NAME]"
      exit 0 ;;
    -*) err "Unknown option: $1"; exit 1 ;;
    *) BUCKET_NAME="$1"; shift ;;
  esac
done

if [[ -z "$BUCKET_NAME" ]]; then
  err "Bucket name is required"
  echo "Usage: $(basename "$0") <bucket-name> [--binding NAME]"
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

info "Creating R2 bucket: $BUCKET_NAME"
wrangler r2 bucket create "$BUCKET_NAME"

ok "R2 bucket created: $BUCKET_NAME"
echo ""
echo -e "${CYAN}Add to wrangler.toml:${NC}"
echo ""
echo "[[r2_buckets]]"
echo "binding = \"$BINDING\""
echo "bucket_name = \"$BUCKET_NAME\""
