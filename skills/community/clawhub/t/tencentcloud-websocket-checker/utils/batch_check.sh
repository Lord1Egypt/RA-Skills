#!/bin/bash
# ============================================================
# 批量 WebSocket 连接检测脚本
# 功能：从 URL 列表文件中读取地址，逐个执行延迟检测
# 用法：./utils/batch_check.sh <url_list_file> [测试轮数]
# ============================================================

set -uo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_CHECK="$SCRIPT_DIR/../ws_check.sh"

if [ $# -lt 1 ]; then
    echo -e "${BOLD}批量 WebSocket 延迟检测${NC}"
    echo ""
    echo -e "用法：$0 <url_list_file> [测试轮数]"
    echo ""
    echo -e "URL 列表文件格式（每行一个 URL）："
    echo -e "  wss://server1.example.com/ws"
    echo -e "  wss://server2.example.com/ws"
    echo -e "  ws://server3.example.com/ws"
    echo ""
    echo -e "示例："
    echo -e "  $0 urls.txt 3"
    exit 1
fi

URL_FILE="$1"
ROUNDS="${2:-3}"

if [ ! -f "$URL_FILE" ]; then
    echo -e "${RED}错误：文件 $URL_FILE 不存在${NC}"
    exit 1
fi

if [ ! -f "$WS_CHECK" ]; then
    echo -e "${RED}错误：未找到 ws_check.sh（路径：$WS_CHECK）${NC}"
    exit 1
fi

# 读取 URL 列表（忽略空行和注释行）
mapfile -t URLS < <(grep -v '^[[:space:]]*$' "$URL_FILE" | grep -v '^[[:space:]]*#')

TOTAL=${#URLS[@]}

echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}  批量 WebSocket 延迟检测${NC}"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  ${DIM}URL 列表${NC}  ：$URL_FILE"
echo -e "  ${DIM}URL 数量${NC}  ：$TOTAL"
echo -e "  ${DIM}每个轮数${NC}  ：$ROUNDS"
echo -e "  ${DIM}开始时间${NC}  ：$(date '+%Y-%m-%d %H:%M:%S')"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

SUCCESS=0
FAIL=0

for i in "${!URLS[@]}"; do
    url="${URLS[$i]}"
    idx=$((i + 1))

    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  [${idx}/${TOTAL}] ${url}${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"

    if bash "$WS_CHECK" "$url" "$ROUNDS" 2>&1; then
        SUCCESS=$((SUCCESS + 1))
    else
        FAIL=$((FAIL + 1))
        echo -e "${RED}  ⚠ 检测失败${NC}"
    fi

    # URL 之间短暂间隔
    [ "$idx" -lt "$TOTAL" ] && sleep 1
done

echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}  批量检测完成${NC}"
echo -e "  总计：${TOTAL}    ${GREEN}成功：${SUCCESS}${NC}    ${RED}失败：${FAIL}${NC}"
echo -e "  完成时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
