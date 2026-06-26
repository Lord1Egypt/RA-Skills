#!/bin/bash

if [ ! -f package.json ]; then
  echo "❌ package.json not found"
  exit 1
fi

# axios 检查
AXIOS_VERSION=$(npm list axios --depth=0 2>/dev/null | grep axios | awk -F@ '{print $NF}')

if [ ! -z "$AXIOS_VERSION" ]; then
  SAFE_VERSION="0.21.2"

  if [ "$(printf '%s\n' "$SAFE_VERSION" "$AXIOS_VERSION" | sort -V | head -n1)" != "$SAFE_VERSION" ]; then
    echo "❌ axios version vulnerable: $AXIOS_VERSION"
  else
    echo "✅ axios version safe"
  fi
fi

# vue2 检查
VUE_VERSION=$(npm list vue --depth=0 2>/dev/null | grep vue | awk -F@ '{print $NF}')

if [ ! -z "$VUE_VERSION" ]; then
  echo "⚠️ vue version is outdated: $VUE_VERSION"
fi

# npm audit
echo "🔍 running npm audit..."
npm audit --audit-level=high 2>/dev/null | grep "high" | head -n 3
