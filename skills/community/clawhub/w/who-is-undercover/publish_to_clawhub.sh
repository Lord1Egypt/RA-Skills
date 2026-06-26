#!/bin/bash
# Publish Who is Undercover skill to ClawHub

echo "=== Publishing Who is Undercover to ClawHub ==="

# Navigate to skill directory
cd "$(dirname "$0")"

# Login to ClawHub (if not already logged in)
echo "1. Checking ClawHub login status..."
clawhub whoami || echo "Please run 'clawhub login' first"

# Validate skill package
echo "2. Validating skill package..."
node publish_test.js

# Publish to ClawHub
echo "3. Publishing to ClawHub..."
clawhub publish who-is-undercover

# Sync local installation
echo "4. Syncing local installation..."
clawhub sync

echo "=== Publish Complete ==="
echo "Skill published successfully to ClawHub!"
echo "You can now install it with: openclaw skill install who-is-undercover"