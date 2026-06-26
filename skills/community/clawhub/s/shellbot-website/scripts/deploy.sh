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

# Parse args
ENV=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env|-e) ENV="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help)
      echo "Usage: $(basename "$0") [options]"
      echo "  --env, -e <env>    Deploy to specific environment (staging, production)"
      echo "  --dry-run          Show what would be deployed without deploying"
      exit 0 ;;
    *) err "Unknown option: $1"; exit 1 ;;
  esac
done

# Auth check: token preferred, OAuth fallback
if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  if wrangler whoami &>/dev/null; then
    info "Using OAuth credentials from wrangler login"
  else
    err "Not authenticated. Use one of:"
    echo "  1. export CLOUDFLARE_API_TOKEN=<token>  (get from https://dash.cloudflare.com/profile/api-tokens)"
    echo "  2. wrangler login                       (OAuth via browser)"
    exit 1
  fi
fi

if [[ ! -f "wrangler.toml" && ! -f "wrangler.json" && ! -f "wrangler.jsonc" ]]; then
  err "No wrangler config found (wrangler.toml, wrangler.json, or wrangler.jsonc)"
  echo "  Run this script from your project root directory"
  exit 1
fi

# Build deploy command as array to handle args safely
DEPLOY_ARGS=("wrangler" "deploy")
if [[ -n "$ENV" ]]; then
  DEPLOY_ARGS+=("-e" "$ENV")
  info "Deploying to environment: $ENV"
else
  info "Deploying to default environment"
fi

if $DRY_RUN; then
  DEPLOY_ARGS+=("--dry-run")
  warn "Dry run mode — no changes will be made"
fi

# Deploy
"${DEPLOY_ARGS[@]}"

if ! $DRY_RUN; then
  ok "Deployment complete"
  echo ""
  info "View deployments: wrangler deployments list"
  info "Tail logs: wrangler tail"
fi
