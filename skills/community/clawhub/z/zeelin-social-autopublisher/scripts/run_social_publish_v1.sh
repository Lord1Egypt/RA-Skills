#!/bin/bash
# 同 v3，统一入口
exec "$(cd "$(dirname "$0")" && pwd)/run_social_publish_v3.sh" "$@"
