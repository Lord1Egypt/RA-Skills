#!/bin/bash
# unset_proxy.sh — 清除当前 shell 的代理环境变量
# Usage: source scripts/unset_proxy.sh
#       或: eval "$(bash scripts/unset_proxy.sh)"

cat <<'EOF'
unset http_proxy https_proxy host_ip
echo "✅ 代理已清除"
EOF
