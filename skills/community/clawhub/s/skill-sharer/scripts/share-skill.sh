#!/bin/bash
# share-skill.sh — Share a skill to Enterprise-Crew-skills repo
# Usage: share-skill.sh <skill-folder> [--description "desc"] [--name "name"] [--yes]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_NAME="${SKILL_SHARER_REPO:-Enterprise-Crew-skills}"
REPO_OWNER="${SKILL_SHARER_OWNER:-<your-github-user>}"
REPO_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}"
WORK_DIR="/tmp/skill-sharer-$$"

# Parse args
SKILL_PATH=""
DESCRIPTION=""
SKILL_NAME=""
AUTO_YES=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --description) DESCRIPTION="$2"; shift 2 ;;
    --name) SKILL_NAME="$2"; shift 2 ;;
    --yes) AUTO_YES=true; shift ;;
    *) SKILL_PATH="$1"; shift ;;
  esac
done

if [[ -z "$SKILL_PATH" ]]; then
  echo "Usage: share-skill.sh <skill-folder> [--description \"desc\"] [--name \"name\"] [--yes]"
  echo ""
  echo "Options:"
  echo "  --description  Short description of the skill"
  echo "  --name         Skill name (default: folder name)"
  echo "  --yes          Skip confirmation prompt"
  exit 1
fi

# Resolve absolute path
SKILL_PATH="$(cd "$SKILL_PATH" && pwd)"

# Default skill name from folder
if [[ -z "$SKILL_NAME" ]]; then
  SKILL_NAME="$(basename "$SKILL_PATH")"
fi

# Try to get description from SKILL.md
if [[ -z "$DESCRIPTION" && -f "$SKILL_PATH/SKILL.md" ]]; then
  DESCRIPTION=$(sed -n 's/^description: *//p' "$SKILL_PATH/SKILL.md" | head -1)
fi

if [[ -z "$DESCRIPTION" ]]; then
  echo "⚠️  No description provided. Use --description or add one to SKILL.md"
  read -rp "Description: " DESCRIPTION
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Skill Sharer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Skill:       $SKILL_NAME"
echo "  Source:      $SKILL_PATH"
echo "  Description: $DESCRIPTION"
echo "  Repo:        $REPO_URL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Clone repo
echo "📥 Cloning $REPO_NAME..."
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"
gh repo clone "${REPO_OWNER}/${REPO_NAME}" "$WORK_DIR/repo" -- --depth 1 2>/dev/null
echo ""

# Step 2: Check if skill already exists
if [[ -d "$WORK_DIR/repo/$SKILL_NAME" ]]; then
  echo "⚠️  Skill '$SKILL_NAME' already exists in repo. Will update."
  rm -rf "$WORK_DIR/repo/$SKILL_NAME"
fi

# Step 3: Sanitize
echo "🧹 Sanitizing skill files..."
mkdir -p "$WORK_DIR/repo/$SKILL_NAME"
bash "$SCRIPT_DIR/sanitize.sh" "$SKILL_PATH" "$WORK_DIR/repo/$SKILL_NAME"

# Never publish the local rules conf
rm -f "$WORK_DIR/repo/$SKILL_NAME/scripts/sanitize-rules.conf" 2>/dev/null
echo ""

# Step 4: Generate README for the skill
echo "📝 Generating skill README..."
bash "$SCRIPT_DIR/generate-readme.sh" "$WORK_DIR/repo/$SKILL_NAME" "$SKILL_NAME" "$DESCRIPTION"
echo ""

# Step 5: Update root README
echo "📋 Updating repo index..."
bash "$SCRIPT_DIR/update-index.sh" "$WORK_DIR/repo" "$SKILL_NAME" "$DESCRIPTION"
echo ""

# Step 6: Show what changed
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Files to publish:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
find "$WORK_DIR/repo/$SKILL_NAME" -type f | sed "s|$WORK_DIR/repo/||" | sort
echo ""

# Show sanitization diff (what was stripped)
echo "🔍 Sanitization check — searching for potential leaks..."
LEAKS=0
while IFS= read -r f; do
  if file "$f" | grep -q "binary\|image"; then continue; fi
  # Check for common leak patterns
  if grep -qiE '(sk-[a-zA-Z0-9]{20}|xoxb-|xoxp-|ghp_|Bearer [a-zA-Z0-9]{20}|password|api.key)' "$f" 2>/dev/null; then
    echo "  ⚠️  Possible leak in: $(basename "$f")"
    LEAKS=$((LEAKS + 1))
  fi
done < <(find "$WORK_DIR/repo/$SKILL_NAME" -type f)

if [[ $LEAKS -eq 0 ]]; then
  echo "  ✅ No obvious leaks detected"
else
  echo ""
  echo "  🚨 Found $LEAKS file(s) with potential leaks — review before pushing!"
fi
echo ""

# Step 7: Confirm and push
if [[ "$AUTO_YES" != "true" ]]; then
  read -rp "Push to GitHub? [y/N] " CONFIRM
  if [[ ! "$CONFIRM" =~ ^[Yy] ]]; then
    echo "❌ Aborted. Sanitized files at: $WORK_DIR/repo/$SKILL_NAME"
    exit 0
  fi
fi

# Step 8: Commit and push
cd "$WORK_DIR/repo"
git add -A
git commit -m "Add skill: $SKILL_NAME — $DESCRIPTION"
git push

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Published: $REPO_URL/tree/main/$SKILL_NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Cleanup
rm -rf "$WORK_DIR"
