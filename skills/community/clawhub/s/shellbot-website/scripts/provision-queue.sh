#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[info]${NC} $*"; }
ok()    { echo -e "${GREEN}[ok]${NC} $*"; }
err()   { echo -e "${RED}[error]${NC} $*" >&2; }

QUEUE_NAME=""
BINDING="QUEUE"
QUEUE_TYPE="producer"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --binding) BINDING="$2"; shift 2 ;;
    --type)
      if [[ "$2" != "producer" && "$2" != "consumer" && "$2" != "both" ]]; then
        err "Invalid queue type: $2 (must be producer, consumer, or both)"
        exit 1
      fi
      QUEUE_TYPE="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $(basename "$0") <queue-name> [--binding NAME] [--type producer|consumer|both]"
      exit 0 ;;
    -*) err "Unknown option: $1"; exit 1 ;;
    *) QUEUE_NAME="$1"; shift ;;
  esac
done

if [[ -z "$QUEUE_NAME" ]]; then
  err "Queue name is required"
  echo "Usage: $(basename "$0") <queue-name> [--binding NAME] [--type producer|consumer|both]"
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

info "Creating queue: $QUEUE_NAME"
wrangler queues create "$QUEUE_NAME"

ok "Queue created: $QUEUE_NAME"
echo ""
echo -e "${CYAN}Add to wrangler.toml:${NC}"
echo ""

if [[ "$QUEUE_TYPE" == "producer" || "$QUEUE_TYPE" == "both" ]]; then
  echo "# Producer binding"
  echo "[[queues.producers]]"
  echo "binding = \"$BINDING\""
  echo "queue = \"$QUEUE_NAME\""
  echo ""
fi

if [[ "$QUEUE_TYPE" == "consumer" || "$QUEUE_TYPE" == "both" ]]; then
  echo "# Consumer binding"
  echo "[[queues.consumers]]"
  echo "queue = \"$QUEUE_NAME\""
  echo "max_batch_size = 10"
  echo "max_batch_timeout = 5"
fi
