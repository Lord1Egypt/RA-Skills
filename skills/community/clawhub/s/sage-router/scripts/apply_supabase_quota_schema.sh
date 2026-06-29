#!/usr/bin/env bash
set -euo pipefail

PROJECT_REF="${SUPABASE_PROJECT_REF:-awtangrlqqsdpksarhwo}"
SUPABASE_ACCESS_TOKEN="${SUPABASE_ACCESS_TOKEN:?Set SUPABASE_ACCESS_TOKEN to a Supabase Management API token.}"
MIGRATION_PATH="${1:-supabase/migrations/20260619021500_sage_router_usage_quotas.sql}"

if [[ ! -f "$MIGRATION_PATH" ]]; then
  printf 'Migration file not found: %s\n' "$MIGRATION_PATH" >&2
  exit 2
fi

if ! command -v jq >/dev/null 2>&1; then
  printf 'jq is required\n' >&2
  exit 2
fi

jq -Rs '{query: ., read_only: false}' "$MIGRATION_PATH" |
  curl -fsS -X POST "https://api.supabase.com/v1/projects/${PROJECT_REF}/database/query" \
    -H "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    --data @- >/dev/null

printf 'Applied Supabase schema migration to project %s from %s\n' "$PROJECT_REF" "$MIGRATION_PATH"
