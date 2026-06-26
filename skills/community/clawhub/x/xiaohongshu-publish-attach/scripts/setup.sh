#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "== xiaohongshu-publish-attach setup =="
chmod +x "$SCRIPT_DIR"/*.sh

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is required." >&2
  exit 1
fi

if ! python3 -m pip --version >/dev/null 2>&1; then
  echo "ERROR: python3 -m pip not available." >&2
  exit 1
fi

echo "Installing Python dependencies (--user)..."
python3 -m pip install --user -r "$SKILL_DIR/requirements.txt"

if ! python3 -c 'import selenium' 2>/dev/null; then
  echo "ERROR: selenium not importable after install." >&2
  exit 1
fi

if ! command -v chromedriver >/dev/null 2>&1 && \
   [[ ! -x "${HOME}/.local/bin/chromedriver" ]] && \
   [[ ! -f "$SCRIPT_DIR/chromedriver.env" ]]; then
  echo "chromedriver not found. Run: bash $SCRIPT_DIR/install_chromedriver.sh"
else
  bash "$SCRIPT_DIR/verify_chrome_stack.sh" || true
fi

echo ""
echo "Next: log in to Xiaohongshu in the same Chrome profile as Zhihu (see references/shared-chrome-with-zhihu.md)"
echo "  bash $SCRIPT_DIR/start_chrome_debug.sh"
echo "  bash $SCRIPT_DIR/xhs_publish.sh --check --json"
