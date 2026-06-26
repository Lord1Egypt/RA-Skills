#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[info]${NC} $*"; }
ok()    { echo -e "${GREEN}[ok]${NC} $*"; }
warn()  { echo -e "${YELLOW}[warn]${NC} $*"; }
err()   { echo -e "${RED}[error]${NC} $*" >&2; }

WORKER_NAME=""
FORCE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force|-f) FORCE=true; shift ;;
    -h|--help)
      echo "Usage: $(basename "$0") <worker-name> [--force]"
      echo "  --force, -f    Skip confirmation prompt"
      exit 0 ;;
    -*) err "Unknown option: $1"; exit 1 ;;
    *) WORKER_NAME="$1"; shift ;;
  esac
done

if [[ -z "$WORKER_NAME" ]]; then
  err "Worker name is required"
  echo "Usage: $(basename "$0") <worker-name> [--force]"
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

if ! $FORCE; then
  err "Destructive operation requires --force flag."
  echo ""
  warn "This will delete worker '$WORKER_NAME' and cannot be undone."
  echo "  Worker: $WORKER_NAME"
  echo ""
  echo "  Re-run with: $(basename "$0") $WORKER_NAME --force"
  exit 1
fi

info "Deleting worker: $WORKER_NAME"
wrangler delete "$WORKER_NAME" --force

ok "Worker '$WORKER_NAME' deleted"
echo ""
info "Note: Associated resources (D1, KV, R2, Queues) are NOT deleted."
info "Use 'wrangler d1 delete', 'wrangler kv namespace delete', etc. to clean up."
