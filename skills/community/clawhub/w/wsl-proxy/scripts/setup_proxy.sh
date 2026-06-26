#!/bin/bash
# setup_proxy.sh — 自动检测并设置 WSL2 代理环境变量
# Usage: eval "$(bash scripts/setup_proxy.sh)"
# 自动扫描常见端口，无需用户指定端口号

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DETECT=$("${SCRIPT_DIR}/detect_proxy.sh" 2>&1)
DETECT_EXIT=$?

if [ $DETECT_EXIT -ne 0 ]; then
    echo "echo \"$DETECT\""
    exit 1
fi

PROXY_URL=$(echo "$DETECT" | grep "^PROXY_URL=" | cut -d= -f2-)
HOST_IP=$(echo "$DETECT" | grep "^PROXY_HOST=" | cut -d= -f2-)
PORT=$(echo "$DETECT" | grep "^PROXY_PORT=" | cut -d= -f2-)

cat <<EOF
# WSL2 代理配置（自动检测端口 ${PORT}）
export host_ip=${HOST_IP}
export http_proxy=${PROXY_URL}
export https_proxy=${PROXY_URL}

# 永久写入 ~/.bashrc（取消注释即可）
# cat >> ~/.bashrc << 'BASHEOF'
# export host_ip=\$(ip route show default | awk '{print \$3}')
# export http_proxy=http://\${host_ip}:${PORT}
# export https_proxy=http://\${host_ip}:${PORT}
# BASHEOF

echo ""
echo "✅ 代理已设置: ${PROXY_URL}"
echo "   验证: curl -s -o /dev/null -w '%{http_code}' https://www.google.com"
EOF
