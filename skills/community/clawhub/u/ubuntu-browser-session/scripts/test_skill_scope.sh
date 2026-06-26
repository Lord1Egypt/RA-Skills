#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$BASE_DIR/.." && pwd)"

test ! -e "$BASE_DIR/protected-page-followup.sh"
test ! -e "$BASE_DIR/test_protected_page_followup.sh"
! rg -n "Ready-Page Follow-Up|only valid follow-up context|rediscover a tab|protected-page-followup\\.sh" "$SKILL_DIR/SKILL.md" >/dev/null
! rg -n 'Wrapper Already Returned `targetId`|protected-page-followup\.sh' "$SKILL_DIR/references/manual-fallback.md" >/dev/null
