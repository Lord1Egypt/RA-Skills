#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[info]${NC} $*"; }
ok()    { echo -e "${GREEN}[ok]${NC} $*"; }
err()   { echo -e "${RED}[error]${NC} $*" >&2; }

SHOW_RESOURCES=false
TAIL_LOGS=false
WORKER=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --resources|-r) SHOW_RESOURCES=true; shift ;;
    --tail|-t) TAIL_LOGS=true; shift ;;
    --worker|-w) WORKER="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $(basename "$0") [options]"
      echo "  --resources, -r    List all resources (D1, KV, R2, Queues)"
      echo "  --tail, -t         Tail worker logs (live)"
      echo "  --worker, -w       Specify worker name"
      exit 0 ;;
    *) WORKER="$1"; shift ;;
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

# Show deployment status
echo -e "${CYAN}=== Deployments ===${NC}"
wrangler deployments list 2>/dev/null || echo "  (run from a project directory with wrangler config)"
echo ""

if $SHOW_RESOURCES; then
  echo -e "${CYAN}=== D1 Databases ===${NC}"
  wrangler d1 list 2>/dev/null || echo "  (none or error)"
  echo ""

  echo -e "${CYAN}=== KV Namespaces ===${NC}"
  wrangler kv namespace list 2>/dev/null || echo "  (none or error)"
  echo ""

  echo -e "${CYAN}=== R2 Buckets ===${NC}"
  wrangler r2 bucket list 2>/dev/null || echo "  (none or error)"
  echo ""

  echo -e "${CYAN}=== Queues ===${NC}"
  wrangler queues list 2>/dev/null || echo "  (none or error)"
  echo ""
fi

if $TAIL_LOGS; then
  info "Tailing logs (Ctrl+C to stop)..."
  if [[ -n "$WORKER" ]]; then
    wrangler tail "$WORKER"
  else
    wrangler tail
  fi
fi
