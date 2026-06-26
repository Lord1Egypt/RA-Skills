#!/usr/bin/env bash
# groove-utilities-check — bash fast-path implementation
# Compares installed version against latest GitHub release.
# Exits 0 on success (even if offline). Falls back to SKILL.md on error.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GROOVE_SKILL="${SCRIPT_DIR}/../../groove/SKILL.md"

# Resolve installed version
if [ ! -f "$GROOVE_SKILL" ]; then
  echo "groove-utilities-check: cannot find groove/SKILL.md — run /groove-admin-install" >&2
  exit 1
fi
installed=$(grep 'version:' "$GROOVE_SKILL" | head -1 | sed "s/.*version:[[:space:]]*[\"']\([^\"']*\)[\"'].*/\1/" | tr -d '[:space:]')

# Fetch latest GitHub release
if ! command -v curl &>/dev/null; then
  echo "groove-utilities-check: curl not available" >&2
  exit 1
fi

if ! command -v python3 &>/dev/null; then
  echo "groove-utilities-check: python3 not available" >&2
  exit 1
fi

latest=$(curl -sf --max-time 5 "https://api.github.com/repos/andreadellacorte/groove/releases/latest" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['tag_name'].lstrip('v'))" 2>/dev/null || echo "")

if [ -z "$latest" ]; then
  echo "groove-utilities-check: could not reach GitHub (offline or rate limited) — skipping"
  exit 0
fi

# Update cache if present
if [ -d ".groove/.cache" ]; then
  date '+%Y-%m-%d' > ".groove/.cache/last-version-check"
fi

# Report
if [ "$installed" = "$latest" ]; then
  echo "groove is up to date (v${installed})"
else
  echo "New version of groove available: v${latest} (installed: v${installed}) — run: /groove-admin-update"
fi
