#!/bin/bash
# scan_git_drift.sh - Detect uncommitted TP changes (skills/ vs git repo)
# NOT a need scanner — this is a closure signal injector.
# Called by scan_closure.sh or standalone.
# Returns: "clean" | "drift:<N> files changed"
#
# Compares distributable files (scripts/, assets configs, *.md, tests/)
# Ignores runtime state: needs-state.json, pending_actions.json,
#   audit.log, followups.jsonl, *.lock, last-scan-snapshot.json

SKILL_DIR="${WORKSPACE:-$HOME/.openclaw/workspace}/skills/turing-pyramid"
GIT_REPO="$HOME/workspace/turing-pyramid"

# Bail if git repo doesn't exist
if [[ ! -d "$GIT_REPO/.git" ]]; then
    echo "no-repo"
    exit 0
fi

# Files to ignore (runtime state, not distributable)
EXCLUDE_PATTERNS=(
    "needs-state.json"
    "needs-state.backup.json"
    "pending_actions.json"
    "last-scan-snapshot.json"
    "active-preset.json"
    "mindstate-prev-snapshot.json"
    "mindstate-config.json"
    "audit.log"
    "decisions.log"
    "followups.jsonl"
    "*.lock"
    "archive/"
    "backups/"
    ".git/"
    ".clawhub/"
    "_meta.json"
    "docs/"
)

# Build rsync exclude args
EXCLUDE_ARGS=""
for pat in "${EXCLUDE_PATTERNS[@]}"; do
    EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude=$pat"
done

# Dry-run rsync to detect differences
drift_files=$(rsync -rcn --out-format='%n' $EXCLUDE_ARGS "$SKILL_DIR/" "$GIT_REPO/" 2>/dev/null | grep -v '/$' | wc -l)

if [[ "$drift_files" -eq 0 ]]; then
    echo "clean"
else
    echo "drift:$drift_files files changed"
fi
