#!/bin/bash
# Setup script: Download the full Uiverse Galaxy component library
# Usage: bash setup.sh [--proxy http://host:port]
#
# This downloads all 3800+ components from GitHub into assets/galaxy/
# The published skill includes a curated subset; run this for the full library.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
GALAXY_DIR="$SCRIPT_DIR/assets/galaxy"
REPO_URL="https://github.com/uiverse-io/galaxy/archive/refs/heads/main.tar.gz"

PROXY=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --proxy) PROXY="-x $2"; shift 2 ;;
        *) shift ;;
    esac
done

echo "📥 Downloading full Uiverse Galaxy library..."

# Remove existing partial data
rm -rf "$GALAXY_DIR"
mkdir -p "$GALAXY_DIR"

# Download and extract
TMPFILE=$(mktemp)
if curl $PROXY -L -o "$TMPFILE" --connect-timeout 30 --max-time 600 "$REPO_URL" 2>&1; then
    tar -xzf "$TMPFILE" -C "$GALAXY_DIR" --strip-components=1
    rm -f "$TMPFILE"
    TOTAL=$(find "$GALAXY_DIR" -name "*.html" | wc -l)
    echo "✅ Done! $TOTAL components installed to $GALAXY_DIR"
else
    rm -f "$TMPFILE"
    echo "❌ Download failed. Try with proxy: bash setup.sh --proxy http://your-proxy:port"
    echo "   Or clone manually: git clone https://github.com/uiverse-io/galaxy.git $GALAXY_DIR"
    exit 1
fi
