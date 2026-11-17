#!/bin/bash
# 双击运行：应用 workbuddy-skin
cd "$(dirname "$0")/.."
node src/apply.mjs
read -n 1 -s -r -p "按任意键退出…"
