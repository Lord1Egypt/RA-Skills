#!/usr/bin/env bash
# =============================================================================
# Sonic Phoenix — Safety Guard Hook
# =============================================================================
# A PreToolUse hook for Bash commands that intercepts attempts to run
# destructive utility scripts and injects a confirmation warning into the
# agent's context.
#
# Destructive scripts in the Sonic Phoenix pipeline:
#   - 05D_force_delete_residue.py  — deletes the entire Unidentified directory
#   - 05F_final_scrub.py           — deletes garbage files outside Sorted/
#   - total_scrub.py               — removes EVERYTHING except protected dirs
#   - absolute_zero_sort.py        — rmtree's the Unidentified tree after sort
#
# Hook type : PreToolUse (Bash)
# Input     : CLAUDE_TOOL_INPUT environment variable (the command about to run)
# Output    : Warning text injected into agent context if a match is found
#
# Setup (Claude Code — .claude/settings.json):
#
#   {
#     "hooks": {
#       "PreToolUse": [{
#         "matcher": "Bash",
#         "hooks": [{
#           "type": "command",
#           "command": "./ultimate-music-manager/hooks/safety-guard.sh"
#         }]
#       }]
#     }
#   }
# =============================================================================

set -euo pipefail

INPUT="${CLAUDE_TOOL_INPUT:-}"

# List of destructive script patterns to intercept.
# Each entry is a substring match against the command being executed.
DESTRUCTIVE_SCRIPTS=(
    "05D_force_delete_residue"
    "05F_final_scrub"
    "total_scrub"
    "absolute_zero_sort"
)

# Check if the command references any destructive script
matched_script=""
for pattern in "${DESTRUCTIVE_SCRIPTS[@]}"; do
    if [[ "$INPUT" == *"$pattern"* ]]; then
        matched_script="$pattern"
        break
    fi
done

# Only output if a destructive script is detected
if [ -n "$matched_script" ]; then
    cat << EOF
<sonic-phoenix-safety-warning>
DESTRUCTIVE OPERATION DETECTED: $matched_script

This script permanently deletes or removes files. Before proceeding:

1. Confirm the user explicitly requested this operation.
2. Verify that Duplicates_Staging/ has been reviewed and cleared.
3. Verify that the Sorted/ hierarchy looks correct (run status.sh).
4. Remind the user that this action CANNOT be undone.

The canonical pipeline (Phases 1-5, 05I) never deletes files.
Destructive utilities are separate, opt-in tools.

If the user did NOT explicitly ask to delete files, DO NOT proceed.
</sonic-phoenix-safety-warning>
EOF
fi
