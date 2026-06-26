#!/bin/bash

CONFIG_FILE="vue.config.js"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "⚠️ vue.config.js not found"
  exit 0
fi

# devtool 检查
if grep -q "devtool" "$CONFIG_FILE"; then
  if grep -q "eval" "$CONFIG_FILE"; then
    echo "⚠️ devtool uses eval (security risk)"
  fi
else
  echo "⚠️ no devtool config found"
fi

# production source map
if grep -q "productionSourceMap: true" "$CONFIG_FILE"; then
  echo "❌ productionSourceMap enabled (leaks source code)"
fi

# optimization
if ! grep -q "minimize" "$CONFIG_FILE"; then
  echo "⚠️ no optimization.minimize found"
fi
