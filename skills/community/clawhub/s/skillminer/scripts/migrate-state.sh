#!/usr/bin/env bash
# migrate-state.sh — migrate skillminer state.json from 0.x to 0.5
#
# Usage: scripts/migrate-state.sh [<state-file>]
#
# This is a no-op fill-in-defaults migration: 0.2/0.3/0.4 → 0.5.
# The 0.5 schema introduces no new required fields beyond 0.4.
# This script bumps schema_version and ensures any optional arrays exist.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE="${1:-$SKILL_DIR/state/state.json}"

[[ -f "$STATE" ]] || { echo "error: state file not found: $STATE" >&2; exit 1; }
command -v jq >/dev/null || { echo "error: jq is required" >&2; exit 1; }

# Bug 4: acquire the same skillminer lock as manage-ledger.sh to prevent races.
# Non-blocking: if another process holds the lock, fail fast — blocking flock on a
# valid FD never fails on contention, which would silently hang migrate indefinitely.
LOCK_NAME="/tmp/skillminer-$(cd "$SKILL_DIR" && pwd | sha1sum | cut -c1-16).lock"
exec 200>"$LOCK_NAME"
if ! flock -n -x 200; then
  echo "error: skillminer lock held by another process ($LOCK_NAME) — wait for it to finish, then retry" >&2
  exit 3
fi

# Bug 4: stale-tmp cleanup (belt and suspenders — same pattern as manage-ledger)
rm -f "${STATE}.tmp"

CURRENT_VERSION=$(jq -r '.schema_version // ""' "$STATE")

case "$CURRENT_VERSION" in
  0.5)
    echo "already at schema_version 0.5, nothing to do"
    exit 0
    ;;
  0.2|0.3|0.4)
    echo "migrating $STATE from $CURRENT_VERSION → 0.5 ..."
    ;;
  *)
    echo "error: unsupported schema_version '$CURRENT_VERSION'" >&2
    exit 1
    ;;
esac

# Backup before migration
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP="${STATE}.bak.pre-migrate-${STAMP}"
cp "$STATE" "$BACKUP"
echo "backup created: $BACKUP"

# Apply migration: bump version, fill in defaults for optional arrays
TMP="$(mktemp "${STATE}.migrate.XXXXXX")"
jq '
  .schema_version = "0.5"
  | .observations  //= []
  | .rejected      //= []
  | .deferred      //= []
  | .silenced      //= []
' "$STATE" > "$TMP"

# Validate
jq -e . "$TMP" >/dev/null || { echo "error: migration produced invalid JSON" >&2; rm -f "$TMP"; exit 1; }
mv "$TMP" "$STATE"

echo "migration complete: $STATE is now schema_version 0.5"
