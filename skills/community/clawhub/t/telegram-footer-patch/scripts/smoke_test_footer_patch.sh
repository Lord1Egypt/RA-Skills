#!/usr/bin/env bash
set -euo pipefail

DIST="${1:-/usr/lib/node_modules/openclaw/dist}"
PATCH_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PATCH_SCRIPT="$PATCH_DIR/patch_reply_footer.py"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[err] python3 not found" >&2
  exit 2
fi
if ! command -v node >/dev/null 2>&1; then
  echo "[err] node not found" >&2
  exit 2
fi

if [[ ! -d "$DIST" ]]; then
  echo "[err] dist directory not found: $DIST" >&2
  exit 2
fi

echo "== 1) target discovery =="
python3 "$PATCH_SCRIPT" --dist "$DIST" --dry-run --list-targets

echo
echo "== 2) dry-run auto-discover =="
python3 "$PATCH_SCRIPT" --dist "$DIST" --dry-run --auto-discover

echo
echo "== 3) apply auto-discover patch =="
python3 "$PATCH_SCRIPT" --dist "$DIST" --auto-discover

echo
echo "== 4) marker verification =="
python3 "$PATCH_SCRIPT" --dist "$DIST" --auto-discover --verify

echo
echo "== 5) syntax verification for patched candidate files =="
mapfile -t TARGET_LINES < <(python3 "$PATCH_SCRIPT" --dist "$DIST" --auto-discover --list-targets)
PATCHED_FILES=()
for line in "${TARGET_LINES[@]}"; do
  file="${line%%  candidate=*}"
  [[ -f "$file" ]] || continue
  case "$line" in
    *"candidate=true"*"marker=true"*)
      PATCHED_FILES+=("$file")
      echo "[check] node --check $file"
      node --check "$file"
      ;;
  esac
done

echo
echo "== 6) sanity grep =="
for file in "${PATCHED_FILES[@]}"; do
  if grep -qF 'formatTokens(' "$file"; then
    echo "[err] patched file still references formatTokens: $file" >&2
    exit 1
  fi
done
echo "[ok] patched files do not reference formatTokens"

echo
echo "== done =="
echo "Patch + verify completed."
echo "Important: this only verifies candidate bundle patching + syntax."
echo "For live acceptance, restart the gateway and confirm a REAL Telegram private-chat reply actually shows the footer."
echo "If the real reply still has no footer, treat it as not fixed yet and keep tracing the live path."
