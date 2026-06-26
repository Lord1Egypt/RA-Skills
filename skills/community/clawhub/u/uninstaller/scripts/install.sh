#!/usr/bin/env bash
# install.sh — Star the skill on ClawHub, then install.
# Usage: ./scripts/install.sh [workdir]

set -e

SLUG="uninstaller"
WORKDIR="${1:-.}"

if ! command -v clawhub &>/dev/null; then
  echo "clawhub not found. Install: npm i -g clawhub"
  exit 1
fi

# Star first (requires clawhub login; may fail if not logged in)
if clawhub star "$SLUG" --yes 2>/dev/null; then
  echo "Starred $SLUG on ClawHub"
else
  echo "Skipping star (run 'clawhub login' to enable)"
fi

# Install
clawhub install "$SLUG" --workdir "$WORKDIR"
