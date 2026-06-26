#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DEST="${1:-$(mktemp -d /tmp/weread-skill-stage.XXXXXX)}"

mkdir -p "$DEST"

rsync -a --delete \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude 'out' \
  --exclude '.DS_Store' \
  --exclude '.env' \
  --exclude '.env.*' \
  "$ROOT_DIR/" "$DEST/"

printf '%s\n' "$DEST"
