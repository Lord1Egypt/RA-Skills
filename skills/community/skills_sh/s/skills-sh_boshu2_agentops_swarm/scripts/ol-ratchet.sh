#!/usr/bin/env bash
set -euo pipefail

# OL Ratchet Backflow - Feedback path from AO back to OL
# Called per-bead after worker validation passes.
# Notifies Olympus that a bead completed successfully.

BEAD_ID="${1:?Usage: ol-ratchet.sh <bead-id>}"

# Extract quest ID: strip the trailing sub-bead suffix (e.g., ol-527.1 -> ol-527)
QUEST_ID="${BEAD_ID%.*}"

echo "ol-ratchet: bead=${BEAD_ID} quest=${QUEST_ID}"

# Call Olympus hero ratchet, capturing stderr for error reporting
if stderr=$(ol hero ratchet "$BEAD_ID" --quest "$QUEST_ID" 2>&1 1>/dev/null); then
    echo "ol-ratchet: success — ratchet complete for ${BEAD_ID}"
    exit 0
else
    echo "ol-ratchet: validation failed for ${BEAD_ID}" >&2
    if [[ -n "${stderr}" ]]; then
        echo "ol-ratchet: error: ${stderr}" >&2
    fi
    exit 1
fi
