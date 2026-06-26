#!/bin/bash
# 兼容旧路径：请改用 run_social_ops_v5.sh
exec "$(cd "$(dirname "$0")" && pwd)/run_social_ops_v5.sh" "$@"
