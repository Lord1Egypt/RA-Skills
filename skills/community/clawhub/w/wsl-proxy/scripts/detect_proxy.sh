#!/bin/bash
# detect_proxy.sh — 自动检测 WSL2 宿主机上的 HTTP 代理端口
# Usage: bash scripts/detect_proxy.sh
# 输出: host_ip 和 port 到 stdout，找不到返回非零

HOST_IP=$(ip route show default | awk '{print $3}')
COMMON_PORTS=(7890 7897 1080 10808 10809 1081 8888 8080 9090 6152 7891)

if [ -z "$HOST_IP" ]; then
    echo "❌ 无法获取宿主机网关 IP"
    exit 1
fi

echo "宿主网关 IP: $HOST_IP"
echo "正在扫描常见代理端口..."
echo ""

for PORT in "${COMMON_PORTS[@]}"; do
    if timeout 2 bash -c "echo > /dev/tcp/${HOST_IP}/${PORT}" 2>/dev/null; then
        # 确认是 HTTP 代理（发个 GET 请求看看）
        RESP=$(timeout 3 bash -c "exec 3<>/dev/tcp/${HOST_IP}/${PORT}; echo -e 'GET http://httpbin.org/get HTTP/1.0\r\nHost: httpbin.org\r\nConnection: close\r\n\r\n' >&3; head -1 <&3" 2>/dev/null)
        if echo "$RESP" | grep -qi "HTTP/"; then
            echo "✅ 端口 $PORT: 可达，响应 HTTP 代理"
            echo "PROXY_HOST=${HOST_IP}"
            echo "PROXY_PORT=${PORT}"
            echo "PROXY_URL=http://${HOST_IP}:${PORT}"
            exit 0
        else
            echo "⚠️  端口 $PORT: 可达但非 HTTP 代理（可能是 SOCKS 或其他协议）"
        fi
    fi
done

echo ""
echo "❌ 未检测到常见 HTTP 代理端口。可能原因："
echo "   1. Windows 上未启动 Clash/V2Ray/SS 等代理工具"
echo "   2. 代理端口不在常见列表中（7890/7897/1080/10808/10809/8888/8080/9090）"
echo "   3. 代理工具使用了非标准端口"
echo ""
echo "请确认后重试，或在 .env 中配置 PROXY_PORT 环境变量。"
exit 1
