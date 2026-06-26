#!/bin/bash
# snappwd-share.sh - Create a secure SnapPwd link from the command line
# Usage: ./snappwd-share.sh "your secret here"
# Or: echo "your secret" | ./snappwd-share.sh

set -e

# Check if snappwd-cli is installed
if ! command -v snappwd &> /dev/null; then
    echo "Error: snappwd-cli is not installed."
    echo ""
    echo "Install it with:"
    echo "  npm install -g @snappwd/cli"
    echo ""
    echo "Or use the web interface at: https://snappwd.io"
    exit 1
fi

# Get secret from argument or stdin
SECRET=""
if [ -n "$1" ]; then
    SECRET="$1"
elif [ ! -t 0 ]; then
    SECRET=$(cat)
else
    echo "Error: No secret provided."
    echo "Usage: $0 \"your secret\""
    echo "   or: echo \"secret\" | $0"
    exit 1
fi

# Create the secure link
echo "Creating secure link..."
LINK=$(snappwd put "$SECRET")

echo ""
echo "Secure link created:"
echo "$LINK"
echo ""
echo "⚠️  This link will self-destruct after one view."
echo "Share it carefully."