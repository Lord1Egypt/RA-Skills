#!/bin/bash
# Auto-create GitHub repository via API
# Usage: ./create-github-repo.sh <repo-name> <description> <github-token>

set -e

REPO_NAME="$1"
DESCRIPTION="$2"
GITHUB_TOKEN="$3"

if [ -z "$REPO_NAME" ] || [ -z "$GITHUB_TOKEN" ]; then
  echo "Usage: $0 <repo-name> <description> <github-token>"
  exit 1
fi

# Default description if not provided
if [ -z "$DESCRIPTION" ]; then
  DESCRIPTION="OpenClaw skill repository"
fi

echo "Creating GitHub repo: $REPO_NAME"

# Create repository via GitHub API
RESPONSE=$(curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{
    \"name\": \"$REPO_NAME\",
    \"description\": \"$DESCRIPTION\",
    \"private\": false,
    \"auto_init\": false,
    \"has_issues\": true,
    \"has_projects\": false,
    \"has_wiki\": false
  }")

# Check if creation was successful
if echo "$RESPONSE" | grep -q '"id"'; then
  REPO_URL=$(echo "$RESPONSE" | jq -r '.html_url')
  echo "✅ Repository created: $REPO_URL"
  exit 0
else
  ERROR_MSG=$(echo "$RESPONSE" | jq -r '.message // "Unknown error"')
  echo "❌ Failed to create repository: $ERROR_MSG"
  exit 1
fi
