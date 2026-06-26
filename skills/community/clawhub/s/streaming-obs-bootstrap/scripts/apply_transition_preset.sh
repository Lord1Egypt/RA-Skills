#!/usr/bin/env bash
set -euo pipefail

TRANSITION="${1:-Fade}"
DURATION_MS="${2:-300}"

mcporter call "obs.set_current_transition(transition_name: \"$TRANSITION\")" >/dev/null
mcporter call "obs.set_transition_duration(transition_duration: $DURATION_MS)" >/dev/null

echo "Applied transition preset: $TRANSITION (${DURATION_MS}ms)"
