#!/bin/bash
# ============================================================
# WebSocket 延迟检测 - 报告生成脚本
# 功能：执行检测并输出 CSV 或 JSON 格式的结构化报告
# 用法：./utils/report_generator.sh <url> [轮数] [csv|json]
# ============================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_CHECK="$SCRIPT_DIR/../ws_check.sh"

RED='\033[0;31m'
GREEN='\033[0;32m'
BOLD='\033[1m'
NC='\033[0m'

if [ $# -lt 1 ]; then
    echo "WebSocket 延迟检测 - 报告生成器" >&2
    echo "" >&2
    echo "用法：$0 <url> [轮数] [csv|json]" >&2
    echo "" >&2
    echo "示例：" >&2
    echo "  $0 wss://example.com/ws 5 csv > report.csv" >&2
    echo "  $0 wss://example.com/ws 3 json > report.json" >&2
    exit 1
fi

URL="$1"
ROUNDS="${2:-3}"
FORMAT="${3:-csv}"

# 解析 URL 中的协议
proto=$(echo "$URL" | sed -n 's/^\(ws\|wss\):\/\/.*$/\1/p')
if [ -z "$proto" ]; then
    echo "错误：URL 必须以 ws:// 或 wss:// 开头" >&2
    exit 1
fi

url_no_proto=$(echo "$URL" | sed "s/^${proto}:\/\///")
domain=$(echo "$url_no_proto" | cut -d '/' -f 1 | sed 's/:[0-9]*$//')
port=$(echo "$url_no_proto" | cut -d '/' -f 1 | sed -n 's/^[^:]*:\([0-9]*\)$/\1/p')
path_part="/$(echo "$url_no_proto" | cut -d '/' -f 2-)"

if [ -z "$port" ]; then
    [ "$proto" = "ws" ] && port=80 || port=443
fi

# 构建 curl URL
if [ "$proto" = "wss" ]; then
    curl_proto="https"
else
    curl_proto="http"
fi
full_url="${curl_proto}://${domain}:${port}${path_part}"

# 收集数据
declare -a results=()

for ((round = 1; round <= ROUNDS; round++)); do
    timing_output=$(curl -s -o /dev/null \
        -w "dns:%{time_namelookup} tcp:%{time_connect} tls:%{time_appconnect} transfer:%{time_starttransfer} total:%{time_total} http_code:%{http_code}" \
        -H 'Upgrade: websocket' \
        -H 'Connection: Upgrade' \
        -H 'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==' \
        -H 'Sec-WebSocket-Version: 13' \
        --max-time 15 \
        "$full_url" 2>/dev/null)

    if [ $? -ne 0 ] && [ -z "$timing_output" ]; then
        continue
    fi

    dns_sec=$(echo "$timing_output" | sed -n 's/.*dns:\([0-9.]*\).*/\1/p')
    tcp_sec=$(echo "$timing_output" | sed -n 's/.*tcp:\([0-9.]*\).*/\1/p')
    tls_sec=$(echo "$timing_output" | sed -n 's/.*tls:\([0-9.]*\).*/\1/p')
    transfer_sec=$(echo "$timing_output" | sed -n 's/.*transfer:\([0-9.]*\).*/\1/p')
    total_sec=$(echo "$timing_output" | sed -n 's/.*total:\([0-9.]*\).*/\1/p')
    http_code=$(echo "$timing_output" | sed -n 's/.*http_code:\([0-9]*\).*/\1/p')

    dns_ms=$(echo "$dns_sec" | awk '{printf "%.0f", $1 * 1000}')
    tcp_ms=$(echo "$tcp_sec $dns_sec" | awk '{printf "%.0f", ($1 - $2) * 1000}')

    if [ "$proto" = "wss" ]; then
        tls_ms=$(echo "$tls_sec $tcp_sec" | awk '{printf "%.0f", ($1 - $2) * 1000}')
        ws_ms=$(echo "$transfer_sec $tls_sec" | awk '{printf "%.0f", ($1 - $2) * 1000}')
    else
        tls_ms=0
        ws_ms=$(echo "$transfer_sec $tcp_sec" | awk '{printf "%.0f", ($1 - $2) * 1000}')
    fi

    total_ms=$(echo "$total_sec" | awk '{printf "%.0f", $1 * 1000}')

    # 修正负值
    [ "$tcp_ms" -lt 0 ] 2>/dev/null && tcp_ms=0
    [ "$tls_ms" -lt 0 ] 2>/dev/null && tls_ms=0
    [ "$ws_ms" -lt 0 ] 2>/dev/null && ws_ms=0

    results+=("${round},${dns_ms},${tcp_ms},${tls_ms},${ws_ms},${total_ms},${http_code}")

    [ "$round" -lt "$ROUNDS" ] && sleep 0.5
done

# 输出结果
TIMESTAMP=$(date '+%Y-%m-%dT%H:%M:%S%z')

case "$FORMAT" in
    csv)
        echo "timestamp,url,protocol,round,dns_ms,tcp_ms,tls_ms,ws_upgrade_ms,total_ms,http_code"
        for r in "${results[@]}"; do
            echo "${TIMESTAMP},${URL},${proto},${r}"
        done
        ;;

    json)
        echo "{"
        echo "  \"timestamp\": \"${TIMESTAMP}\","
        echo "  \"url\": \"${URL}\","
        echo "  \"protocol\": \"${proto}\","
        echo "  \"domain\": \"${domain}\","
        echo "  \"port\": ${port},"
        echo "  \"rounds\": ${ROUNDS},"
        echo "  \"results\": ["

        local_count=0
        total_results=${#results[@]}
        for r in "${results[@]}"; do
            local_count=$((local_count + 1))
            IFS=',' read -r round dns tcp tls ws total code <<< "$r"
            comma=""
            [ "$local_count" -lt "$total_results" ] && comma=","
            echo "    {"
            echo "      \"round\": ${round},"
            echo "      \"dns_ms\": ${dns},"
            echo "      \"tcp_ms\": ${tcp},"
            echo "      \"tls_ms\": ${tls},"
            echo "      \"ws_upgrade_ms\": ${ws},"
            echo "      \"total_ms\": ${total},"
            echo "      \"http_code\": ${code}"
            echo "    }${comma}"
        done

        echo "  ]"
        echo "}"
        ;;

    *)
        echo "错误：不支持的格式 $FORMAT，可选 csv 或 json" >&2
        exit 1
        ;;
esac
