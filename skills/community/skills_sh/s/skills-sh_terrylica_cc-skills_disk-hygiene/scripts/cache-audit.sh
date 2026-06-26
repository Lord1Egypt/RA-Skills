#!/usr/bin/env bash
# cache-audit.sh - Measure all developer cache sizes on macOS
# Usage: bash scripts/cache-audit.sh

set -euo pipefail

echo "=== Developer Cache Audit ==="
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo ""

declare -a names=(
  "uv"
  "Homebrew"
  "pip"
  "npm"
  "cargo registry"
  "rustup"
  "sccache"
  "Playwright"
  "huggingface"
  "Docker"
)

declare -a paths=(
  "$HOME/Library/Caches/uv"
  "$HOME/Library/Caches/Homebrew"
  "$HOME/Library/Caches/pip"
  "$HOME/.npm/_cacache"
  "$HOME/.cargo/registry/cache"
  "$HOME/.rustup/toolchains"
  "$HOME/Library/Caches/Mozilla.sccache"
  "$HOME/Library/Caches/ms-playwright"
  "$HOME/.cache/huggingface"
  "$HOME/Library/Containers/com.docker.docker/Data"
)

total_kb=0

for i in "${!names[@]}"; do
  name="${names[$i]}"
  path="${paths[$i]}"
  if [ -d "$path" ]; then
    size_human=$(du -sh "$path" 2>/dev/null | cut -f1)
    size_kb=$(du -sk "$path" 2>/dev/null | cut -f1)
    total_kb=$((total_kb + size_kb))
    printf "%-20s %8s  %s\n" "$name" "$size_human" "$path"
  fi
done

echo ""
total_gb=$(echo "scale=1; $total_kb / 1048576" | bc 2>/dev/null || echo "N/A")
echo "Total: ${total_gb} GB"
