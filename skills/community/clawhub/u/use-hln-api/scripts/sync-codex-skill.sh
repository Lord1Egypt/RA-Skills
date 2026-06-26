#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/skills/use-hln-api"

if [[ ! -f "$SRC/SKILL.md" ]]; then
  echo "Missing canonical skill at $SRC/SKILL.md" >&2
  exit 1
fi

if diff -q "$SRC/SKILL.md" "$ROOT/SKILL.md" >/dev/null 2>&1 \
  && diff -qr "$SRC/references" "$ROOT/references" >/dev/null 2>&1; then
  echo "Codex root files are already in sync with skills/use-hln-api/"
  exit 0
fi

rm -rf "$ROOT/references"
mkdir -p "$ROOT/references"

cp "$SRC/SKILL.md" "$ROOT/SKILL.md"
cp -R "$SRC/references/." "$ROOT/references/"

echo "Synced Codex root files from skills/use-hln-api/"
