#!/bin/sh
# Usage: reject-draft.sh <draft_id> <reason>
#
# Only run this when a human operator has explicitly told you, in this conversation
# turn, to reject this specific draft ID. See SKILL.md's "Guardrail" note.
set -eu
. "$(dirname "$0")/common.sh"

draft_id="${1:?usage: reject-draft.sh <draft_id> <reason>}"
reason="${2:?usage: reject-draft.sh <draft_id> <reason>}"

curl -s -X POST "$BASE/public/v1/drafts/$draft_id/reject" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d "{\"reason\": \"$reason\"}" | print_response
