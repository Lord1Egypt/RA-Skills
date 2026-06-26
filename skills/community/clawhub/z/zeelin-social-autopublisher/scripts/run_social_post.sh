#!/bin/bash
# 旧版依赖 /tmp JSON；现改为直接走 v5（主题 → 生成 JSON → 顺序发布）
set -euo pipefail
exec "$(cd "$(dirname "$0")" && pwd)/run_social_ops_v5.sh" "${1:?Usage: $0 <topic>}"
