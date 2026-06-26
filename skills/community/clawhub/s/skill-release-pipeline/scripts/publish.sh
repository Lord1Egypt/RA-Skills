#!/usr/bin/env bash
# publish.sh — Full pipeline: validate → GitHub → ClawHub
# Usage: publish.sh <skill-folder> --repo owner/repo --version x.y.z [--slug name] [--tags t1,t2]

set -euo pipefail

FOLDER=""
REPO=""
VERSION=""
SLUG=""
TAGS="latest"
COMMIT_MSG=""

usage() {
  echo "Usage: $0 <skill-folder> --repo owner/repo --version x.y.z [--slug name] [--tags t1,t2] [--message msg]"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case $1 in
    --repo)      REPO="$2"; shift 2 ;;
    --version)   VERSION="$2"; shift 2 ;;
    --slug)      SLUG="$2"; shift 2 ;;
    --tags)      TAGS="$2"; shift 2 ;;
    --message|-m) COMMIT_MSG="$2"; shift 2 ;;
    -h|--help)   usage ;;
    *)           if [[ -z "$FOLDER" ]]; then FOLDER="$1"; shift else usage; fi ;;
  esac
done

[[ -z "$FOLDER" || -z "$REPO" || -z "$VERSION" ]] && usage
FOLDER="$(cd "$FOLDER" && pwd)"

# Derive slug from folder name if not provided
if [[ -z "$SLUG" ]]; then
  SLUG="$(basename "$FOLDER")"
fi

if [[ -z "$COMMIT_MSG" ]]; then
  COMMIT_MSG="release: $SLUG v$VERSION"
fi

echo "=== Skill Publisher ==="
echo "Folder:  $FOLDER"
echo "Repo:    $REPO"
echo "Version: $VERSION"
echo "Slug:    $SLUG"
echo ""

# Step 1: Validate SKILL.md
echo "--- Step 1: Validating ---"
if [[ ! -f "$FOLDER/SKILL.md" ]]; then
  echo "ERROR: SKILL.md not found in $FOLDER"
  exit 1
fi

# Check frontmatter
if ! head -1 "$FOLDER/SKILL.md" | grep -q "^---"; then
  echo "ERROR: SKILL.md missing YAML frontmatter (must start with ---)"
  exit 1
fi

if ! grep -q "^name:" "$FOLDER/SKILL.md"; then
  echo "ERROR: SKILL.md frontmatter missing 'name' field"
  exit 1
fi

if ! grep -q "^description:" "$FOLDER/SKILL.md"; then
  echo "ERROR: SKILL.md frontmatter missing 'description' field"
  exit 1
fi

echo "  ✓ SKILL.md valid"

# Step 2: Push to GitHub
echo ""
echo "--- Step 2: Pushing to GitHub ---"
cd "$FOLDER"

if [[ ! -d .git ]]; then
  git init
  echo "  ✓ git init"
fi

git add -A
git commit -m "$COMMIT_MSG" --allow-empty 2>/dev/null || true
echo "  ✓ committed"

# Add remote if not exists
if ! git remote get-url origin &>/dev/null; then
  git remote add origin "https://github.com/$REPO.git"
  echo "  ✓ added remote origin"
fi

git push -u origin main 2>&1 || git push -u origin master 2>&1
echo "  ✓ pushed to GitHub"

# Step 3: Publish to ClawHub
echo ""
echo "--- Step 3: Publishing to ClawHub ---"

# Check auth
if ! npx clawhub whoami &>/dev/null; then
  echo "ERROR: Not logged in to ClawHub. Run: npx clawhub login"
  exit 1
fi

npx clawhub publish "$FOLDER" \
  --version "$VERSION" \
  --slug "$SLUG" \
  --tags "$TAGS"

echo ""
echo "=== Done! ==="
echo "GitHub:  https://github.com/$REPO"
echo "ClawHub: https://clawhub.ai/skills/$SLUG"
echo ""
echo "Install: npx clawhub@latest install $SLUG"
