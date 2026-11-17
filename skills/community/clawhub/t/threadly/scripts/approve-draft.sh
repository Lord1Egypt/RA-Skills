#!/bin/sh
# Usage: approve-draft.sh <draft_id>
#
# Only run this when a human operator has explicitly told you, in this conversation
# turn, to approve this specific draft ID. See SKILL.md's "Guardrail" note.
set -eu
. "$(dirname "$0")/common.sh"

draft_id="${1:?usage: approve-draft.sh <draft_id>}"

curl -s -X POST "$BASE/public/v1/drafts/$draft_id/approve" -H "$AUTH_HEADER" | print_response
