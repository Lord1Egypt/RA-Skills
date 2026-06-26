#!/usr/bin/env bash
# Publish this repository to ClawdHub using the official clawdhub CLI.
# Requires: clawdhub login (or CLAWDHUB_TOKEN via login --token).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required to read version from pyproject.toml" >&2
  exit 1
fi

VERSION="$(python3 -c "import pathlib, tomllib; print(tomllib.load(open(pathlib.Path('pyproject.toml'), 'rb'))['project']['version'])")"
CHANGELOG="${CHANGELOG:-Tai Alpha Stock ${VERSION}}"

TMP="$(mktemp -d)"
cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

cd "$TMP"
npm init -y >/dev/null 2>&1
# undici: clawdhub 0.3.0 imports it but does not declare it; keeps CLI working on current Node.
npm install clawdhub@0.3.0 undici@6 >/dev/null 2>&1

# clawdhub 0.3.x hardcodes REQUEST_TIMEOUT_MS = 15_000 in dist/http.js. Multi-file
# skill uploads routinely exceed 15s (multipart + registry processing), which
# surfaces as: Non-error was thrown: "Timeout". Patch the temp install only.
HTTP_JS="$TMP/node_modules/clawdhub/dist/http.js"
if [[ -f "$HTTP_JS" ]]; then
  python3 -c "
from pathlib import Path
import sys
path = Path(sys.argv[1])
text = path.read_text(encoding='utf-8')
old = 'const REQUEST_TIMEOUT_MS = 15_000'
new = 'const REQUEST_TIMEOUT_MS = 180_000'
if old not in text:
    print('clawdhub_publish: expected timeout line not found; skipping patch', file=sys.stderr)
    sys.exit(0)
text = text.replace(old, new, 1)
# Undici H2 is experimental on some Node builds; disable to reduce flaky connects.
text = text.replace('allowH2: true', 'allowH2: false', 1)
path.write_text(text, encoding='utf-8')
" "$HTTP_JS"
fi

exec "$TMP/node_modules/.bin/clawdhub" publish "$REPO_ROOT" \
  --slug tai-alpha-stock \
  --name "Tai Alpha Stock" \
  --version "$VERSION" \
  --changelog "$CHANGELOG" \
  "$@"
