#!/usr/bin/env bash
# init-workspace.sh — Create .learnings/ and .self-improving/ in the workspace root.
# Safe to run multiple times; never overwrites existing files.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE="${1:-$(pwd)}"

echo "Initializing self-improving workspace in: $WORKSPACE"

# --- .learnings/ ---
mkdir -p "$WORKSPACE/.learnings"

for tmpl in LEARNINGS.md ERRORS.md FEATURE_REQUESTS.md REVIEW_QUEUE.md; do
  target="$WORKSPACE/.learnings/$tmpl"
  source="$SKILL_DIR/assets/$tmpl"
  if [ ! -f "$target" ]; then
    if [ -f "$source" ]; then
      cp "$source" "$target"
      echo "  [OK] Created .learnings/$tmpl"
    else
      echo "  [WARN] Template not found: assets/$tmpl — creating empty file"
      touch "$target"
    fi
  else
    echo "  [SKIP] .learnings/$tmpl already exists"
  fi
done

# --- .self-improving/ ---
mkdir -p "$WORKSPACE/.self-improving/domains"
mkdir -p "$WORKSPACE/.self-improving/projects"
mkdir -p "$WORKSPACE/.self-improving/archive"

for tmpl in HOT.md INDEX.md heartbeat-state.md; do
  target="$WORKSPACE/.self-improving/$tmpl"
  source="$SKILL_DIR/assets/$tmpl"
  if [ ! -f "$target" ]; then
    if [ -f "$source" ]; then
      cp "$source" "$target"
      echo "  [OK] Created .self-improving/$tmpl"
    else
      echo "  [WARN] Template not found: assets/$tmpl — creating empty file"
      touch "$target"
    fi
  else
    echo "  [SKIP] .self-improving/$tmpl already exists"
  fi
done

echo ""
echo "Done. Workspace learning directories are ready."
echo "  .learnings/        — raw intake (errors, corrections, feature requests)"
echo "  .self-improving/   — tiered memory (HOT, domains, projects, archive)"
