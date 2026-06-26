#!/bin/bash

FILE="babel.config.js"

if [ ! -f "$FILE" ]; then
  echo "⚠️ babel.config.js not found"
  exit 0
fi

# polyfill 检查
if grep -q "@babel/polyfill" "$FILE"; then
  echo "⚠️ @babel/polyfill is deprecated"
fi

# core-js 检查
if grep -q "core-js" "$FILE"; then
  VERSION=$(grep core-js "$FILE" | grep -o "[0-9]" | head -n1)

  if [ "$VERSION" -lt 3 ]; then
    echo "❌ core-js version too low"
  else
    echo "✅ core-js version ok"
  fi
fi

# useBuiltIns
if ! grep -q "useBuiltIns" "$FILE"; then
  echo "⚠️ useBuiltIns not configured"
fi
