#!/usr/bin/env bash
# Block commits containing real Tavily API keys (tvly-dev-... or tvly-prod-...)
# This is the second line of defense after .gitignore — catches accidental copies.
#
# Install: copied to .git/hooks/pre-commit by setup.sh (or run `git init` after setup)
set -e

PATTERN='tvly-(dev|prod)-[A-Za-z0-9_-]{20,}'
FOUND=0

# Scan staged files (not the whole working tree, to allow the example files)
STAGED=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null)

if [ -z "$STAGED" ]; then
    exit 0
fi

for f in $STAGED; do
    if [ -f "$f" ] && git diff --cached -- "$f" | grep -qE "$PATTERN"; then
        echo "❌ BLOCKED: real Tavily key found in staged file: $f"
        echo "   pattern: $PATTERN"
        echo "   fix: remove the key, use config/keys.example.json as a template instead"
        FOUND=1
    fi
done

if [ "$FOUND" -eq 1 ]; then
    exit 1
fi

exit 0