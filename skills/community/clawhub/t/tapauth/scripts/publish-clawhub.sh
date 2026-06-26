#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# publish-clawhub.sh — Publish TapAuth skill to ClawHub (OpenClaw registry)
#
# Swaps SKILL-OPENCLAW.md → SKILL.md before publishing so OpenClaw agents
# get the secrets-manager-first documentation instead of the generic version.
#
# Usage:
#   bash scripts/publish-clawhub.sh [--dry-run]
#   bash scripts/publish-clawhub.sh --version 1.0.6
#   bash scripts/publish-clawhub.sh --version 1.0.6 --changelog "Grant polling and OpenClaw reload guidance"
###############################################################################

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# --- Argument parsing --------------------------------------------------------
DRY_RUN="false"
VERSION=""
CHANGELOG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)    DRY_RUN="true"; shift ;;
    --version)
      [[ $# -lt 2 ]] && { echo "FATAL: --version requires a value"; exit 1; }
      VERSION="$2"; shift 2 ;;
    --changelog)
      [[ $# -lt 2 ]] && { echo "FATAL: --changelog requires a value"; exit 1; }
      CHANGELOG="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# --- Validate ----------------------------------------------------------------
if [[ ! -f "$SKILL_DIR/SKILL-OPENCLAW.md" ]]; then
  echo "FATAL: SKILL-OPENCLAW.md not found in $SKILL_DIR"
  exit 1
fi

if [[ ! -f "$SKILL_DIR/SKILL.md" ]]; then
  echo "FATAL: SKILL.md not found in $SKILL_DIR"
  exit 1
fi

CLAWHUB_CMD=()
if command -v clawhub &>/dev/null; then
  CLAWHUB_CMD=(clawhub)
elif command -v npx &>/dev/null; then
  CLAWHUB_CMD=(npx -y clawhub@latest)
elif [[ "$DRY_RUN" != "true" ]]; then
  echo "FATAL: clawhub CLI not found and npx is unavailable."
  exit 1
fi

# --- Build staging directory -------------------------------------------------
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "Staging skill for ClawHub..."
echo "  Source: $SKILL_DIR"
echo "  Staging: $TMP_DIR"

# Copy everything
cp -r "$SKILL_DIR"/* "$TMP_DIR/"

# Swap SKILL-OPENCLAW.md → SKILL.md
cp "$TMP_DIR/SKILL-OPENCLAW.md" "$TMP_DIR/SKILL.md"
rm "$TMP_DIR/SKILL-OPENCLAW.md"

echo "  Swapped SKILL-OPENCLAW.md → SKILL.md"

# Verify the swap worked
if grep -q "OpenClaw Secrets Manager" "$TMP_DIR/SKILL.md"; then
  echo "  Verified: SKILL.md contains OpenClaw-specific content"
else
  echo "WARNING: SKILL.md may not contain expected OpenClaw content"
fi

# --- Publish or dry-run ------------------------------------------------------
if [[ "$DRY_RUN" == "true" ]]; then
  echo ""
  echo "[DRY RUN] Would publish to ClawHub:"
  echo "  Slug: tapauth"
  echo "  Version: ${VERSION:-<from skill.json>}"
  echo "  Files:"
  find "$TMP_DIR" -type f | sed "s|$TMP_DIR/||" | sort | sed 's/^/    /'
  echo ""
  echo "  SKILL.md first 5 lines:"
  head -5 "$TMP_DIR/SKILL.md" | sed 's/^/    /'
  echo ""
  echo "[DRY RUN] No changes made."
else
  echo ""
  echo "Publishing to ClawHub..."

  PUBLISH_ARGS=("${CLAWHUB_CMD[@]}" publish "$TMP_DIR/" --slug tapauth --name "TapAuth")
  [[ -n "$VERSION" ]] && PUBLISH_ARGS+=(--version "$VERSION")
  [[ -n "$CHANGELOG" ]] && PUBLISH_ARGS+=(--changelog "$CHANGELOG")

  "${PUBLISH_ARGS[@]}"

  echo ""
  echo "Published to ClawHub."
fi
