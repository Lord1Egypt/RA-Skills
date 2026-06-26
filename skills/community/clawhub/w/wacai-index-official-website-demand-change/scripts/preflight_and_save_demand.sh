#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="/Users/dyshi/.openclaw/workspace/skills/index-official-website-demand-change"
PROJECT_DIR="${1:-}"
TARGET_BRANCH="${2:-feat/test}"
TMP_FILE="$(mktemp)"
cleanup() {
  rm -f "$TMP_FILE"
}
trap cleanup EXIT

if [[ -z "$PROJECT_DIR" ]]; then
  echo "Usage: $0 <project-dir> [branch] [input-file]" >&2
  exit 2
fi

if [[ $# -ge 3 ]]; then
  cat "$3" > "$TMP_FILE"
else
  cat > "$TMP_FILE"
fi

if [[ ! -s "$TMP_FILE" ]]; then
  echo "Demand content is empty." >&2
  exit 2
fi

bash "$SKILL_DIR/scripts/git_prepare_branch.sh" "$PROJECT_DIR" "$TARGET_BRANCH"
python3 "$SKILL_DIR/scripts/save_product_demand.py" --project-dir "$PROJECT_DIR" --file "$TMP_FILE"

echo "Demand saved and branch prepared."
