#!/usr/bin/env bash
#
# publish-skill.sh ... publish SKILL.md to a website as plain text
#
# Usage:
#   bash publish-skill.sh <repo-path> <website-path> [--name <name>] [--deploy]
#
# Examples:
#   # Copy SKILL.md to website install directory
#   bash publish-skill.sh /path/to/memory-crystal-private /path/to/wip-websites/wip.computer --name memory-crystal
#
#   # Copy and deploy to VPS
#   bash publish-skill.sh /path/to/memory-crystal-private /path/to/wip-websites/wip.computer --name memory-crystal --deploy
#
#   # Auto-detect name from package.json
#   bash publish-skill.sh /path/to/memory-crystal-private /path/to/wip-websites/wip.computer --deploy
#
# Convention:
#   SKILL.md in the repo -> install/{name}.txt on the website
#   The website serves these as plain text at yoursite.com/install/{name}.txt
#   Any AI can fetch the URL and get clean, parseable content.
#
# Config (optional, in repo root):
#   .skill-publish.json:
#   {
#     "name": "memory-crystal",
#     "website": "/path/to/website",
#     "deploy_command": "bash deploy.sh"
#   }

set -euo pipefail

REPO_PATH="${1:-}"
WEBSITE_PATH="${2:-}"
NAME=""
DO_DEPLOY=false

# Parse flags
shift 2 2>/dev/null || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) NAME="$2"; shift 2 ;;
    --deploy) DO_DEPLOY=true; shift ;;
    *) echo "Unknown flag: $1"; exit 1 ;;
  esac
done

# ── Resolve from config if args are missing ──

if [[ -z "$REPO_PATH" ]]; then
  echo "Usage: bash publish-skill.sh <repo-path> <website-path> [--name <name>] [--deploy]"
  exit 1
fi

# Try to load .skill-publish.json from repo
CONFIG_FILE="$REPO_PATH/.skill-publish.json"
if [[ -f "$CONFIG_FILE" ]]; then
  if command -v node &>/dev/null; then
    [[ -z "$WEBSITE_PATH" ]] && WEBSITE_PATH=$(node -p "require('$CONFIG_FILE').website || ''" 2>/dev/null || echo "")
    [[ -z "$NAME" ]] && NAME=$(node -p "require('$CONFIG_FILE').name || ''" 2>/dev/null || echo "")
    DEPLOY_CMD=$(node -p "require('$CONFIG_FILE').deploy_command || ''" 2>/dev/null || echo "")
  fi
fi

if [[ -z "$WEBSITE_PATH" ]]; then
  echo "Error: website path required (arg 2 or .skill-publish.json)"
  exit 1
fi

# ── Auto-detect name from package.json ──

if [[ -z "$NAME" ]]; then
  if [[ -f "$REPO_PATH/package.json" ]] && command -v node &>/dev/null; then
    NAME=$(node -p "require('$REPO_PATH/package.json').name || ''" 2>/dev/null || echo "")
    # Strip npm scope (@wipcomputer/foo -> foo)
    NAME="${NAME#@*/}"
  fi
fi

if [[ -z "$NAME" ]]; then
  echo "Error: could not determine skill name. Use --name or add to package.json"
  exit 1
fi

# ── Find SKILL.md ──

SKILL_FILE=""

# Check skills/*/SKILL.md first (standard location)
if [[ -z "$SKILL_FILE" ]]; then
  FOUND=$(find "$REPO_PATH/skills" -maxdepth 2 -name "SKILL.md" 2>/dev/null | head -1)
  [[ -n "$FOUND" ]] && SKILL_FILE="$FOUND"
fi

# Check root SKILL.md
if [[ -z "$SKILL_FILE" && -f "$REPO_PATH/SKILL.md" ]]; then
  SKILL_FILE="$REPO_PATH/SKILL.md"
fi

if [[ -z "$SKILL_FILE" ]]; then
  echo "Error: no SKILL.md found in $REPO_PATH"
  exit 1
fi

# ── Publish ──

INSTALL_DIR="$WEBSITE_PATH/install"
mkdir -p "$INSTALL_DIR"

cp "$SKILL_FILE" "$INSTALL_DIR/$NAME.txt"
echo "Published: install/$NAME.txt (from $(basename "$SKILL_FILE"))"

# ── Deploy if requested ──

if [[ "$DO_DEPLOY" == "true" ]]; then
  # Look for deploy script in website directory
  DEPLOY_SCRIPT=""
  if [[ -n "${DEPLOY_CMD:-}" ]]; then
    DEPLOY_SCRIPT="$DEPLOY_CMD"
  elif [[ -f "$WEBSITE_PATH/../deploy.sh" ]]; then
    DEPLOY_SCRIPT="bash $WEBSITE_PATH/../deploy.sh"
  elif [[ -f "$WEBSITE_PATH/deploy.sh" ]]; then
    DEPLOY_SCRIPT="bash $WEBSITE_PATH/deploy.sh"
  fi

  if [[ -n "$DEPLOY_SCRIPT" ]]; then
    echo "Deploying website..."
    eval "$DEPLOY_SCRIPT"
  else
    echo "Warning: --deploy requested but no deploy script found."
    echo "  Looked for: deploy.sh in website directory"
    echo "  Or set deploy_command in .skill-publish.json"
  fi
fi
