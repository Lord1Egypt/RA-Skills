#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[info]${NC} $*"; }
ok()    { echo -e "${GREEN}[ok]${NC} $*"; }
err()   { echo -e "${RED}[error]${NC} $*" >&2; }

DB_NAME=""
BINDING="DB"
MIGRATION_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --binding) BINDING="$2"; shift 2 ;;
    --migration-file) MIGRATION_FILE="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $(basename "$0") <db-name> [--binding NAME] [--migration-file path]"
      exit 0 ;;
    -*) err "Unknown option: $1"; exit 1 ;;
    *) DB_NAME="$1"; shift ;;
  esac
done

if [[ -z "$DB_NAME" ]]; then
  err "Database name is required"
  echo "Usage: $(basename "$0") <db-name> [--binding NAME]"
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

info "Creating D1 database: $DB_NAME"
OUTPUT=$(wrangler d1 create "$DB_NAME" 2>&1)
echo "$OUTPUT"

# Extract database ID — try structured output first, fall back to UUID pattern
DB_ID=$(echo "$OUTPUT" | grep -o 'database_id = "[^"]*"' | cut -d'"' -f2 || true)
if [[ -z "$DB_ID" ]]; then
  DB_ID=$(echo "$OUTPUT" | grep -oE '"id"\s*:\s*"[0-9a-f-]+"' | head -1 | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' || true)
fi
if [[ -z "$DB_ID" ]]; then
  DB_ID=$(echo "$OUTPUT" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -1 || true)
fi

if [[ -z "$DB_ID" ]]; then
  err "Database may have been created but could not extract database ID from wrangler output."
  err "Check manually: wrangler d1 list"
  exit 1
fi

ok "Database created: $DB_NAME (ID: $DB_ID)"
echo ""
echo -e "${CYAN}Add to wrangler.toml:${NC}"
echo ""
echo "[[d1_databases]]"
echo "binding = \"$BINDING\""
echo "database_name = \"$DB_NAME\""
echo "database_id = \"$DB_ID\""

# Apply initial migration if provided
if [[ -n "$MIGRATION_FILE" ]]; then
  if [[ -f "$MIGRATION_FILE" ]]; then
    info "Applying migration: $MIGRATION_FILE"
    if wrangler d1 execute "$DB_NAME" --file "$MIGRATION_FILE"; then
      ok "Migration applied"
    else
      err "Migration failed. Database was created but migration did not apply."
      err "Apply manually: wrangler d1 execute $DB_NAME --file $MIGRATION_FILE"
      exit 1
    fi
  else
    err "Migration file not found: $MIGRATION_FILE"
    exit 1
  fi
fi
