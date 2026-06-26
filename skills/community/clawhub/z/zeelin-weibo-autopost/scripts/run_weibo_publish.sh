#!/bin/bash
# 兼容旧路径：请改用 run_weibo_ops.sh
exec "$(cd "$(dirname "$0")" && pwd)/run_weibo_ops.sh" "$@"
