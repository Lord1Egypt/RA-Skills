#!/usr/bin/env bash
# Run once after installing this skill from ClawHub (no other repo files needed).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "== zhihu-publish-attach setup =="

chmod +x "$SCRIPT_DIR"/*.sh

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is required." >&2
  exit 1
fi

if ! python3 -m pip --version >/dev/null 2>&1; then
  echo "ERROR: python3 -m pip not available. Install python3-pip or run: python3 -m ensurepip --user" >&2
  exit 1
fi

PY_MM=$(python3 -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')
echo "Python $PY_MM"

if python3 -c 'import selenium' 2>/dev/null; then
  SEL_VER=$(python3 -c 'import selenium; print(getattr(selenium, "__version__", "?"))' 2>/dev/null || echo installed)
  echo "selenium already importable ($SEL_VER) — will still run user install if missing deps."
fi

echo "Installing Python dependencies (--user, no sudo)..."
python3 -m pip install --user -r "$SKILL_DIR/requirements.txt"

if ! python3 -c 'import selenium' 2>/dev/null; then
  echo "ERROR: selenium not importable after install." >&2
  echo "  Check: python3 -c 'import site; print(site.getusersitepackages())'" >&2
  echo "  If PYTHONNOUSERSITE=1 is set, unset it for OpenClaw/exec." >&2
  exit 1
fi

if ! command -v chromedriver >/dev/null 2>&1 && \
   [[ ! -x /usr/local/bin/chromedriver ]] && \
   [[ ! -x "${HOME}/.local/bin/chromedriver" ]] && \
   [[ ! -f "$SCRIPT_DIR/chromedriver.env" ]]; then
  echo ""
  echo "chromedriver not found. Install matching your Chrome version:"
  echo "  bash $SCRIPT_DIR/install_chromedriver.sh"
  echo "  # or manual -> /usr/local/bin/chromedriver (see references/linux-vnc-setup.md)"
else
  echo "chromedriver: ${CHROMEDRIVER_PATH:-$(command -v chromedriver 2>/dev/null || echo /usr/local/bin/chromedriver)}"
  bash "$SCRIPT_DIR/verify_chrome_stack.sh" || echo "WARN: run install_chromedriver.sh or fix version mismatch."
fi

if ! command -v google-chrome-stable >/dev/null 2>&1 && \
   ! command -v google-chrome >/dev/null 2>&1 && \
   ! command -v chromium >/dev/null 2>&1; then
  echo "WARN: Google Chrome / Chromium not found on PATH."
fi

echo ""
echo "Next steps (VNC on Linux server):"
echo "  1) bash $SCRIPT_DIR/start_chrome_debug.sh"
echo "  2) Log in to Zhihu in that Chrome window"
echo "  3) bash $SCRIPT_DIR/zhihu_publish.sh --check --json"
echo ""
echo "OpenClaw agent should use: bash {baseDir}/scripts/zhihu_publish.sh ..."
