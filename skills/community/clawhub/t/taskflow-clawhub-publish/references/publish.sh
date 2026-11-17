#!/usr/bin/env bash
# Concrete ingestion commands used by the publish child task.
# Usage: publish.sh <skillFolder> <slug> <name> <version> <changelog>
set -euo pipefail
SKILL_FOLDER="${1:?skill folder required}"
SLUG="${2:?slug required}"
NAME="${3:?name required}"
VERSION="${4:?version required}"
CHANGELOG="${5:?changelog required}"

# 1) Dry-run preview: validates shape without writing to the registry.
clawhub publish "$SKILL_FOLDER" --slug "$SLUG" --name "$NAME" \
  --version "$VERSION" --changelog "$CHANGELOG" --dry-run --json

# 2) Real publish: irreversible write to the ClawHub resource center.
clawhub publish "$SKILL_FOLDER" --slug "$SLUG" --name "$NAME" \
  --version "$VERSION" --changelog "$CHANGELOG" --json

# 3) Verify: the newly published artifact must be inspectable by slug.
clawhub inspect "$SLUG"
