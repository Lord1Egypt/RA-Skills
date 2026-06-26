#!/usr/bin/env bash
# debug-flow.sh — Local debug: install → verify → uninstall flow
# Usage: ./scripts/debug-flow.sh [step] [--debug]
#   step: 1=install 2=verify 3=uninstall or omit=interactive
#   --debug: auto-run uninstall without prompt, use --preserve all

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

DEBUG=false
step=""
for arg in "$@"; do
  [[ "$arg" == "--debug" ]] && DEBUG=true || step="${step:-$arg}"
done

echo "=== OpenClaw Uninstall Skill — Debug Flow ==="
echo "Skill path: $SKILL_DIR"
echo ""

step="${step:-}"

# Step 1: Install (simulate — copy to ~/.openclaw/skills/)
do_install() {
  echo "[Step 1] Install"
  echo "  - From ClawHub: clawhub install uninstaller"
  echo "  - Or local copy: cp -r $SKILL_DIR ~/.openclaw/skills/"
  if [[ -d "$HOME/.openclaw/skills/uninstaller" ]]; then
    echo "  ✓ Already at ~/.openclaw/skills/uninstaller"
  else
    echo "  Running: mkdir -p ~/.openclaw/skills && cp -r $SKILL_DIR ~/.openclaw/skills/uninstaller"
    mkdir -p "$HOME/.openclaw/skills"
    cp -r "$SKILL_DIR" "$HOME/.openclaw/skills/uninstaller"
    echo "  ✓ Copied"
  fi
  echo ""
}

# Step 2: Verify residue (read-only)
do_verify() {
  echo "[Step 2] Verify residue (read-only)"
  "$SCRIPT_DIR/verify-clean.sh" || true
  echo ""
}

# Step 3: Uninstall (confirm)
do_uninstall() {
  echo "[Step 3] Uninstall"
  echo "  Option A — IM-initiated (requires host=gateway):"
  echo "    $SCRIPT_DIR/schedule-uninstall.sh"
  echo ""
  echo "  Option B — CLI one-shot:"
  echo "    openclaw uninstall --all --yes --non-interactive"
  echo ""
  echo "  Option C — Direct one-shot (with --preserve all):"
  echo "    $SCRIPT_DIR/uninstall-oneshot.sh --preserve all"
  echo ""
  if [[ "$DEBUG" == "true" ]]; then
    echo "  [DEBUG] Auto-running without prompt..."
    exec "$SCRIPT_DIR/uninstall-oneshot.sh" --preserve all
  fi
  read -p "Run Option C (direct uninstall)? [y/N] " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    exec "$SCRIPT_DIR/uninstall-oneshot.sh" --preserve all
  else
    echo "  Skipped. Run one of the commands above manually."
  fi
}

case "$step" in
  1) do_install ;;
  2) do_verify ;;
  3) do_uninstall ;;
  *)
    do_install
    do_verify
    if [[ "$DEBUG" == "true" ]]; then
      do_uninstall
    else
      echo "Next: run ./scripts/debug-flow.sh 3 or ./scripts/debug-flow.sh --debug for uninstall"
    fi
    ;;
esac
