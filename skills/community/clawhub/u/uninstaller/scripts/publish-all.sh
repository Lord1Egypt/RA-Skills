#!/bin/bash
# publish-all.sh — Run full publish path (automated + manual prompts)
# Use after release or when syncing to all domains.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "=== Uninstaller Skill — Full Publish Path ==="
echo ""

# 1. ClawHub (if token set)
if [ -n "${CLAWHUB_TOKEN:-}" ]; then
  echo "[1/4] ClawHub (CLAWHUB_TOKEN set)"
  clawhub login --token "$CLAWHUB_TOKEN" --no-browser 2>/dev/null || true
  VERSION="${1:-1.0.$(date +%Y%m%d)}"
  clawhub publish . --slug uninstaller --name "Uninstaller" --version "$VERSION" --changelog "Release $VERSION" --tags latest
  echo "  ✓ Published to ClawHub"
else
  echo "[1/4] ClawHub — SKIP (set CLAWHUB_TOKEN to publish)"
fi
echo ""

# 2. skills.sh — no action (GitHub = source)
echo "[2/4] skills.sh — No action. Repo is source. Users: npx skills add ERerGB/openclaw-uninstall"
echo ""

# 3. Sundial — manual
echo "[3/4] Sundial — Manual (interactive login only)"
read -p "  Run Sundial push now? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  npx sundial-hub auth login 2>/dev/null || true
  npx sundial-hub push . && echo "  ✓ Published to Sundial" || echo "  ✗ Sundial push failed"
fi
echo ""

# 4. ghcr.io (skr) — optional
echo "[4/4] ghcr.io (OCI) — Run in CI or: skr build . -t ghcr.io/ERerGB/openclaw-uninstall:latest && skr push ..."
echo "  (Requires skr CLI: https://github.com/andrewhowdencom/skr)"
echo ""

echo "=== Done ==="
echo "See doc/PUBLISH_PATH.md for full checklist."
