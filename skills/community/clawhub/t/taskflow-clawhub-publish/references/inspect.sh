#!/usr/bin/env bash
# Verification commands used by the verify child task.
# Usage: inspect.sh <slug> <expectedVersion>
set -euo pipefail
SLUG="${1:?slug required}"
EXPECTED_VERSION="${2:?expected version required}"

# 1) Inspect the published artifact metadata by slug.
clawhub inspect "$SLUG"

# 2) Optional: install into a throwaway dir and read back the recorded metadata.
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
clawhub install "$SLUG" --workdir "$TMP_DIR" --no-input
test -f "$TMP_DIR/$SLUG/_meta.json"
test -f "$TMP_DIR/$SLUG/.clawhub/origin.json"

# 3) Confirm the installed version equals what the publish step was asked to write.
INSTALLED_VERSION="$(node -e "console.log(require('$TMP_DIR/$SLUG/_meta.json').version)")"
test "$INSTALLED_VERSION" = "$EXPECTED_VERSION"
