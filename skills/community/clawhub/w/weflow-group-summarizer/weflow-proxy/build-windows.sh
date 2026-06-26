#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Clawhub filters .mod files, so we store as .mod.txt and restore before build
cp go.mod.txt go.mod
trap 'rm -f go.mod' EXIT

echo "Cross-compiling weflow-proxy for Windows (amd64)..."
GOOS=windows GOARCH=amd64 go build -o weflow-proxy.exe .

echo "Done: $(ls -lh weflow-proxy.exe | awk '{print $5, $NF}')"
