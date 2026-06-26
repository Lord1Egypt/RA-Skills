#!/bin/bash
# check_proxy.sh — 检测 WSL2 代理状态（自动端口检测）
# Usage: bash scripts/check_proxy.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DETECT=$("${SCRIPT_DIR}/detect_proxy.sh" 2>&1)
DETECT_EXIT=$?

echo "=== WSL2 代理状态检查 ==="
echo ""
echo "--- 端口检测 ---"
echo "$DETECT"
echo ""

# 如果检测成功，提取 URL 并测试连通性
if [ $DETECT_EXIT -eq 0 ]; then
    PROXY_URL=$(echo "$DETECT" | grep "^PROXY_URL=" | cut -d= -f2-)
    HOST_IP=$(echo "$DETECT" | grep "^PROXY_HOST=" | cut -d= -f2-)
    PORT=$(echo "$DETECT" | grep "^PROXY_PORT=" | cut -d= -f2-)

    echo ""
    echo "--- 环境变量 ---"
    echo "http_proxy:   ${http_proxy:-<未设置>}"
    echo "https_proxy:  ${https_proxy:-<未设置>}"
    echo ""

    echo "--- 配置建议 ---"
    echo "运行以下命令设置代理："
    echo "  export http_proxy=${PROXY_URL}"
    echo "  export https_proxy=${PROXY_URL}"
    echo ""

    echo "--- 外网访问测试 ---"
    if [ -n "$http_proxy" ]; then
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 https://www.google.com 2>/dev/null)
        if [ "$HTTP_CODE" = "200" ]; then
            echo "Google: ✅ HTTP $HTTP_CODE（代理工作正常）"
        else
            echo "Google: ⚠️ HTTP $HTTP_CODE（可能需要验证或代理规则问题）"
        fi
    else
        echo "当前 shell 未设置代理环境变量。"
        echo "先运行: eval \"\$(bash scripts/setup_proxy.sh)\""
    fi
fi
