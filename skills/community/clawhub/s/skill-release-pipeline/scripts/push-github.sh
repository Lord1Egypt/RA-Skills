#!/usr/bin/env bash
# push-github.sh — Initialize git and push skill to GitHub
# Usage: push-github.sh <skill-folder> --repo owner/repo [--message "commit message"]

set -euo pipefail

FOLDER=""
REPO=""
COMMIT_MSG=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --repo)    REPO="$2"; shift 2 ;;
    --message|-m) COMMIT_MSG="$2"; shift 2 ;;
    -h|--help) echo "Usage: $0 <skill-folder> --repo owner/repo [--message msg]"; exit 0 ;;
    *)         if [[ -z "$FOLDER" ]]; then FOLDER="$1"; shift else echo "Unknown: $1"; exit 1; fi ;;
  esac
done

[[ -z "$FOLDER" || -z "$REPO" ]] && { echo "Usage: $0 <skill-folder> --repo owner/repo"; exit 1; }

FOLDER="$(cd "$FOLDER" && pwd)"
SLUG="$(basename "$FOLDER")"

if [[ -z "$COMMIT_MSG" ]]; then
  COMMIT_MSG="feat: $SLUG skill for OpenClaw"
fi

cd "$FOLDER"

# Init git if needed
if [[ ! -d .git ]]; then
  git init
  echo "Initialized git repo"
fi

# Stage and commit
git add -A
git commit -m "$COMMIT_MSG" --allow-empty
echo "Committed: $COMMIT_MSG"

# Set remote
if git remote get-url origin &>/dev/null; then
  git remote set-url origin "https://github.com/$REPO.git"
else
  git remote add origin "https://github.com/$REPO.git"
fi

# Push
git push -u origin main 2>&1 || git push -u origin master 2>&1

echo ""
echo "✅ Pushed to https://github.com/$REPO"
