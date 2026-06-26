#!/usr/bin/env bash
set -euo pipefail

# Prepare a physically clean ClawHub release folder.
# Default output: ~/Documents/youos-release-<version>

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -f "clawhub.json" ]]; then
  echo "Error: clawhub.json not found in $ROOT_DIR" >&2
  exit 1
fi

VERSION="$(python3 - <<'PY'
import json
from pathlib import Path
j=json.loads(Path('clawhub.json').read_text())
print(j.get('version','').strip())
PY
)"

if [[ -z "$VERSION" ]]; then
  echo "Error: could not read version from clawhub.json" >&2
  exit 1
fi

OUT_DIR="${1:-$HOME/Documents/youos-release-${VERSION}}"

echo "Preparing ClawHub release bundle"
echo "  source : $ROOT_DIR"
echo "  version: $VERSION"
echo "  output : $OUT_DIR"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

# Strict allowlist. ClawHub bundles must be TEXT-ONLY (binaries are rejected at
# upload), so this excludes screenshots/ (the registry resolves clawhub.json's
# screenshot paths from the homepage repo) and extension/ (it ships PNG icons —
# users get the extension from the GitHub repo / Gmail page, per SKILL.md).
ALLOWED=(
  "app"
  "clawhub.json"
  "configs"
  "PRIVACY.md"
  "pyproject.toml"
  "README.md"
  "scripts"
  "SKILL.md"
)

for item in "${ALLOWED[@]}"; do
  if [[ -e "$ROOT_DIR/$item" ]]; then
    rsync -a "$ROOT_DIR/$item" "$OUT_DIR/"
  else
    echo "WARN: missing allowlisted item: $item"
  fi
done

# Extra hygiene inside copied tree.
find "$OUT_DIR" -name '.DS_Store' -delete || true
find "$OUT_DIR" -name '__pycache__' -type d -prune -exec rm -rf {} + || true
find "$OUT_DIR" -name '*.pyc' -delete || true

# Text-only guard: ClawHub rejects binary files at upload. Flag any that slipped
# in (e.g. images, archives) so we catch them before publishing, not on rejection.
BINARIES="$(find "$OUT_DIR" -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.gif' -o -iname '*.ico' -o -iname '*.zip' -o -iname '*.gz' -o -iname '*.safetensors' -o -iname '*.pdf' \))"
if [[ -n "$BINARIES" ]]; then
  echo "ERROR: non-text files in the bundle (ClawHub rejects these). Remove them:" >&2
  echo "$BINARIES" >&2
  exit 1
fi

# Final strict check: only allowlisted top-level entries remain.
for entry in $(cd "$OUT_DIR" && ls -1A); do
  keep=false
  for allowed in "${ALLOWED[@]}"; do
    if [[ "$entry" == "$allowed" ]]; then
      keep=true
      break
    fi
  done
  if [[ "$keep" == false ]]; then
    echo "WARN: unexpected top-level entry: $entry"
  fi
done

echo "Done. Minimal bundle ready at: $OUT_DIR"
