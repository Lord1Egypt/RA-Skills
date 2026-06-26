#!/bin/bash
# Release script for same-idea skill

set -e

SKILL_NAME="same-idea"
VERSION=${1:-"1.0.0"}
REPO_URL="https://github.com/jianghaidong/same-idea-skill"

echo "🚀 Releasing $SKILL_NAME v$VERSION"

# Check if git repo exists
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git remote add origin $REPO_URL
fi

# Add all files
git add .

# Commit
git commit -m "Release v$VERSION - Same Idea skill for finding resonating quotes" || true

# Create tag
git tag -a "v$VERSION" -m "Release version $VERSION" || true

# Push
git push origin main || git push origin master || true
git push origin --tags || true

echo "✅ Released v$VERSION"
echo "📦 GitHub URL: $REPO_URL"
