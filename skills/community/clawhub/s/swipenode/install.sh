#!/bin/bash
set -e

echo "Installing SwipeNode from the official open-source GitHub repository..."
echo "Source: https://github.com/sirToby99/swipenode"

# Pinned to a specific version for security and reproducible builds
go install github.com/sirToby99/swipenode@v1.6.4

echo "✅ SwipeNode successfully installed to your Go bin directory (usually ~/go/bin)."
echo "Make sure ~/go/bin is in your system PATH!"
