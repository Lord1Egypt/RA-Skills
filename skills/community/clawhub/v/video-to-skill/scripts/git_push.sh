#!/bin/bash
# Step 5: Push Skill to GitHub
# Usage: ./git_push.sh <skill_md_file> <repo_url> [branch]
set -e

SKILL_FILE="$1"
REPO_URL="${2:-https://github.com/eeyan2025-art/skillhub.git}"
BRANCH="${3:-main}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
GITHUB_REPO_DIR="/tmp/skillhub_repo_$$"

if [ -z "$SKILL_FILE" ]; then
  echo "ERROR: skill file is required"
  exit 1
fi

if [ ! -f "$SKILL_FILE" ]; then
  echo "ERROR: file not found: $SKILL_FILE"
  exit 1
fi

# 从 frontmatter 提取 skill name
SKILL_NAME=$(sed -n '/^---$/,/^---$/p' "$SKILL_FILE" | grep '^name:' | sed 's/^name: *//' | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

if [ -z "$SKILL_NAME" ]; then
  echo "ERROR: could not extract skill name from SKILL.md"
  echo "Generate a proper frontmatter with 'name:' field"
  exit 1
fi

echo "Pushing skill: $SKILL_NAME"
rm -rf "$GITHUB_REPO_DIR"

if [ -n "$GITHUB_TOKEN" ]; then
  HOST_PATH=$(echo "$REPO_URL" | sed 's|https://||')
  AUTH_URL="https://${GITHUB_TOKEN}@${HOST_PATH}"
else
  AUTH_URL="$REPO_URL"
fi

echo "Cloning repository..."
git clone "$AUTH_URL" "$GITHUB_REPO_DIR" 2>&1 || {
  echo "ERROR: failed to clone repository"
  echo "LOCAL_FILE=$SKILL_FILE"
  exit 1
}

cd "$GITHUB_REPO_DIR"
mkdir -p "$GITHUB_REPO_DIR/skills"

if [ -d "$GITHUB_REPO_DIR/skills/$SKILL_NAME" ]; then
  BACKUP_DIR="${GITHUB_REPO_DIR}/skills/${SKILL_NAME}.bak.$(date +%s)"
  mv "$GITHUB_REPO_DIR/skills/$SKILL_NAME" "$BACKUP_DIR"
  echo "Backed up existing skill to: $BACKUP_DIR"
fi

mkdir -p "$GITHUB_REPO_DIR/skills/$SKILL_NAME"
cp "$SKILL_FILE" "$GITHUB_REPO_DIR/skills/$SKILL_NAME/SKILL.md"

git config user.email "bot@openclaw.ai" 2>/dev/null || true
git config user.name "OpenClaw Bot" 2>/dev/null || true

git add .
git commit -m "Add/Update skill: $SKILL_NAME (from YouTube)" || {
  echo "Nothing to commit (skill already exists with same content)"
  echo "GITHUB_LINK=https://github.com/eeyan2025-art/skillhub/tree/main/skills/$SKILL_NAME"
  exit 0
}

git push origin "$BRANCH" 2>&1

GITHUB_LINK="https://github.com/eeyan2025-art/skillhub/blob/main/skills/$SKILL_NAME/SKILL.md"
echo "GITHUB_LINK=$GITHUB_LINK"
rm -rf "$GITHUB_REPO_DIR"
