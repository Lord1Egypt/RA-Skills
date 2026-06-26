#!/bin/bash
# SnapTrade Trading Skill - Environment Setup
# Run this once before using the skill for the first time.
# Uses a virtual environment to avoid modifying system Python packages.

set -e

VENV_DIR=".venv-snaptrade"

echo "Creating virtual environment at $VENV_DIR ..."
python3 -m venv "$VENV_DIR"

echo "Installing pinned dependencies..."
"$VENV_DIR/bin/pip" install --quiet \
  "snaptrade-python-sdk==11.0.187" \
  "python-dotenv==1.2.2"

echo "Verifying installed versions..."
SNAPTRADE_VER=$("$VENV_DIR/bin/pip" show snaptrade-python-sdk | grep "^Version:" | awk '{print $2}')
DOTENV_VER=$("$VENV_DIR/bin/pip" show python-dotenv | grep "^Version:" | awk '{print $2}')
echo "  snaptrade-python-sdk: $SNAPTRADE_VER (expected 11.0.187)"
echo "  python-dotenv:        $DOTENV_VER (expected 1.2.2)"

if [ "$SNAPTRADE_VER" != "11.0.187" ] || [ "$DOTENV_VER" != "1.2.2" ]; then
  echo ""
  echo "ERROR: Installed versions do not match expected. Aborting."
  echo "For high-security environments, verify package hashes at:"
  echo "  https://pypi.org/project/snaptrade-python-sdk/#files"
  echo "  https://pypi.org/project/python-dotenv/#files"
  exit 1
fi

echo ""
echo "Setup complete. Activate the environment with:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "Next: set the following environment variables (or add to a .env file):"
echo "  SNAPTRADE_CLIENT_ID=<your clientId>"
echo "  SNAPTRADE_CONSUMER_KEY=<your consumerKey>"
echo "  SNAPTRADE_USER_ID=<userId for this user>"
echo "  SNAPTRADE_USER_SECRET=<userSecret for this user>"
