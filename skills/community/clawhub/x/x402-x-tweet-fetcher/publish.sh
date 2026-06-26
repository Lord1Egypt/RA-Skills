#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="./x402-x-tweet-fetcher"
SLUG="x402-x-tweet-fetcher"
NAME="X402 X Tweet Fetcher"
VERSION="${1:-1.0.0}"

echo "Publishing $NAME version $VERSION ..."
clawhub publish "$SKILL_DIR" \
  --slug "$SLUG" \
  --name "$NAME" \
  --version "$VERSION" \
  --tags latest

echo "Done."
