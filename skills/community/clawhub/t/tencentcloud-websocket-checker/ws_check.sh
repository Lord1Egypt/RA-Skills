#!/bin/bash
set -uo pipefail

# ============================================================
# WebSocket 连接延迟检测脚本
# 功能：逐阶段测量 WebSocket 建连过程中的各环节耗时
#       包括 DNS解析、TCP握手、TLS握手、WebSocket Upgrade
# 用法：./ws_check.sh <WebSocket URL> [测试轮数]
# 示例：./ws_check.sh wss://example.com/ws 3
# ============================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# 默认测试轮数
DEFAULT_ROUNDS=3

# 阈值定义（毫秒）— 用于性能评级
DNS_THRESHOLD_GOOD=50
DNS_THRESHOLD_WARN=200
TCP_THRESHOLD_GOOD=100
TCP_THRESHOLD_WARN=300
TLS_THRESHOLD_GOOD=200
TLS_THRESHOLD_WARN=500
WS_THRESHOLD_GOOD=200
WS_THRESHOLD_WARN=500
TOTAL_THRESHOLD_GOOD=500
TOTAL_THRESHOLD_WARN=1000

# 全局变量
proto=""
domain=""
port=""
path_part=""
force_proto=""  # 通过 -p/--protocol 指定的协议，优先级最高

# ===================== 工具函数 =====================

# 打印分隔线
print_separator() {
    echo -e "${DIM}$(printf '─%.0s' {1..68})${NC}"
}

# 打印双线分隔
print_double_separator() {
    echo -e "${BOLD}$(printf '═%.0s' {1..68})${NC}"
}

# 性能评级（参数：耗时ms, 好阈值, 警告阈值）
get_rating() {
    local time_ms=$1
    local good=$2
    local warn=$3
    if [ "$time_ms" -le "$good" ]; then
        echo -e "${GREEN}● 优秀${NC}"
    elif [ "$time_ms" -le "$warn" ]; then
        echo -e "${YELLOW}● 正常${NC}"
    else
        echo -e "${RED}● 偏慢${NC}"
    fi
}

# 生成耗时条形图（参数：耗时ms, 总耗时ms）
generate_bar() {
    local time_ms=$1
    local total_ms=$2
    local max_width=30
    if [ "$total_ms" -eq 0 ]; then
        echo ""
        return
    fi
    local width=$((time_ms * max_width / total_ms))
    [ "$width" -eq 0 ] && [ "$time_ms" -gt 0 ] && width=1
    local bar=""
    for ((i = 0; i < width; i++)); do
        bar="${bar}█"
    done
    echo "$bar"
}

# ===================== 依赖检查 =====================

check_dependencies() {
    local missing=()
    local dependencies=("curl" "dig" "awk" "sed")

    for dep in "${dependencies[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "${RED}错误：缺少以下依赖工具：${missing[*]}${NC}"
        echo -e "CentOS 安装命令：yum install -y bind-utils curl gawk sed"
        echo -e "Ubuntu 安装命令：apt install -y dnsutils curl gawk sed"
        exit 1
    fi
}

# ===================== 参数解析 =====================

show_usage() {
    echo -e "${BOLD}WebSocket 连接延迟检测工具${NC}"
    echo ""
    echo -e "${YELLOW}用法：${NC}"
    echo -e "  $0 [选项] <WebSocket URL> [测试轮数]"
    echo ""
    echo -e "${YELLOW}选项：${NC}"
    echo -e "  ${GREEN}-p, --protocol <ws|wss>${NC}  强制指定协议类型（优先级高于 URL 前缀）"
    echo -e "  ${GREEN}-h, --help${NC}               显示此帮助信息"
    echo ""
    echo -e "${YELLOW}示例：${NC}"
    echo -e "  # 方式1：通过 URL 前缀自动识别协议"
    echo -e "  $0 wss://example.com/websocket"
    echo -e "  $0 ws://example.com/websocket"
    echo ""
    echo -e "  # 方式2：通过参数强制指定协议（URL 可省略协议前缀）"
    echo -e "  $0 -p wss example.com/websocket"
    echo -e "  $0 --protocol ws example.com/websocket"
    echo ""
    echo -e "  # 方式3：混合使用（-p 参数优先级高于 URL 前缀）"
    echo -e "  $0 -p ws wss://example.com/websocket  # 实际使用 ws 协议"
    echo ""
    echo -e "  # 指定测试轮数"
    echo -e "  $0 wss://example.com/websocket 5"
    echo -e "  $0 -p wss example.com/websocket 5"
}

# 解析命令行参数，设置 force_proto / url / rounds
parse_args() {
    force_proto=""
    local positional_args=()

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -p|--protocol)
                if [ -z "${2:-}" ]; then
                    echo -e "${RED}错误：-p/--protocol 参数需要指定协议类型（ws 或 wss）${NC}"
                    exit 1
                fi
                local p_val="$2"
                p_val=$(echo "$p_val" | tr '[:upper:]' '[:lower:]')
                if [ "$p_val" != "ws" ] && [ "$p_val" != "wss" ]; then
                    echo -e "${RED}错误：协议类型必须为 ws 或 wss，当前值：$2${NC}"
                    exit 1
                fi
                force_proto="$p_val"
                shift 2
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            -*)
                echo -e "${RED}错误：未知选项 $1${NC}"
                echo -e "使用 $0 --help 查看帮助"
                exit 1
                ;;
            *)
                positional_args+=("$1")
                shift
                ;;
        esac
    done

    # 检查位置参数
    if [ ${#positional_args[@]} -lt 1 ]; then
        show_usage
        exit 1
    fi

    PARSED_URL="${positional_args[0]}"
    PARSED_ROUNDS="${positional_args[1]:-$DEFAULT_ROUNDS}"
}

# ===================== URL 解析 =====================

parse_url() {
    local url="$1"

    # 提取 URL 中的协议前缀（可选）
    local url_proto
    url_proto=$(echo "$url" | sed -n 's/^\(ws\|wss\):\/\/.*$/\1/p')

    # 去掉协议前缀（如果有）
    local url_no_proto
    if [ -n "$url_proto" ]; then
        url_no_proto=$(echo "$url" | sed "s/^${url_proto}:\/\///")
    else
        # URL 没有协议前缀，也可能是 http/https 前缀（容错处理）
        url_no_proto=$(echo "$url" | sed 's/^https\?:\/\///')
    fi

    # 确定最终使用的协议：-p 参数 > URL 前缀 > 默认 wss
    if [ -n "$force_proto" ]; then
        proto="$force_proto"
        if [ -n "$url_proto" ] && [ "$url_proto" != "$force_proto" ]; then
            echo -e "  ${YELLOW}注意：-p 参数指定协议 ${BOLD}${force_proto}${NC}${YELLOW}，覆盖 URL 中的 ${url_proto}:// 前缀${NC}"
        fi
    elif [ -n "$url_proto" ]; then
        proto="$url_proto"
    else
        echo -e "${RED}错误：无法确定协议类型！${NC}"
        echo -e "请通过以下方式之一指定协议："
        echo -e "  1. URL 前缀：wss://example.com/ws 或 ws://example.com/ws"
        echo -e "  2. -p 参数：$0 -p wss example.com/ws"
        exit 1
    fi

    # 分离域名端口部分和路径部分
    local domain_port_part
    domain_port_part=$(echo "$url_no_proto" | cut -d '/' -f 1)
    path_part="/$(echo "$url_no_proto" | cut -d '/' -f 2-)"
    [ "$path_part" = "/" ] || true

    # 提取域名和端口
    domain=$(echo "$domain_port_part" | sed 's/:[0-9]*$//')
    port=$(echo "$domain_port_part" | sed -n 's/^[^:]*:\([0-9]*\)$/\1/p')
    if [ -z "$port" ]; then
        if [ "$proto" = "ws" ]; then
            port=80
        else
            port=443
        fi
    fi
}

# ===================== 使用 curl 精确测量各阶段耗时 =====================

# 核心测量函数：利用 curl 的 -w 格式化输出获取各阶段精确时间
# curl 提供的时间节点说明：
#   time_namelookup  : DNS 解析完成的时间
#   time_connect     : TCP 连接建立完成的时间
#   time_appconnect  : TLS/SSL 握手完成的时间（仅 HTTPS）
#   time_starttransfer: 收到第一个字节的时间（包含 WebSocket Upgrade 响应）
#   time_total       : 请求完成的总时间
#
# 各阶段耗时计算：
#   DNS 解析 = time_namelookup
#   TCP 握手 = time_connect - time_namelookup
#   TLS 握手 = time_appconnect - time_connect （仅 wss）
#   WS 升级  = time_starttransfer - time_appconnect（wss）
#             = time_starttransfer - time_connect   （ws）

run_single_measurement() {
    local proto="$1"
    local domain="$2"
    local port="$3"
    local path="$4"

    # 构建 URL：curl 需要使用 http/https 协议
    local curl_proto
    if [ "$proto" = "wss" ]; then
        curl_proto="https"
    else
        curl_proto="http"
    fi
    local full_url="${curl_proto}://${domain}:${port}${path}"

    # 使用 curl 发送 WebSocket Upgrade 请求并获取各时间节点
    local timing_output
    timing_output=$(curl -s -o /dev/null \
        -w "dns:%{time_namelookup} tcp:%{time_connect} tls:%{time_appconnect} transfer:%{time_starttransfer} total:%{time_total} http_code:%{http_code}" \
        -H 'Upgrade: websocket' \
        -H 'Connection: Upgrade' \
        -H 'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==' \
        -H 'Sec-WebSocket-Version: 13' \
        --max-time 15 \
        "$full_url" 2>/dev/null)

    if [ $? -ne 0 ] && [ -z "$timing_output" ]; then
        echo "ERROR"
        return 1
    fi

    echo "$timing_output"
}

# 解析单次测量结果，输出毫秒级别的各阶段耗时
parse_timing() {
    local timing_str="$1"
    local proto="$2"

    local dns_sec tcp_sec tls_sec transfer_sec total_sec http_code

    dns_sec=$(echo "$timing_str" | sed -n 's/.*dns:\([0-9.]*\).*/\1/p')
    tcp_sec=$(echo "$timing_str" | sed -n 's/.*tcp:\([0-9.]*\).*/\1/p')
    tls_sec=$(echo "$timing_str" | sed -n 's/.*tls:\([0-9.]*\).*/\1/p')
    transfer_sec=$(echo "$timing_str" | sed -n 's/.*transfer:\([0-9.]*\).*/\1/p')
    total_sec=$(echo "$timing_str" | sed -n 's/.*total:\([0-9.]*\).*/\1/p')
    http_code=$(echo "$timing_str" | sed -n 's/.*http_code:\([0-9]*\).*/\1/p')

    # 转换为毫秒并计算各阶段耗时
    local dns_ms tcp_ms tls_ms ws_ms total_ms
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

    # 修正负值（网络波动可能导致微小负值）
    [ "$tcp_ms" -lt 0 ] 2>/dev/null && tcp_ms=0
    [ "$tls_ms" -lt 0 ] 2>/dev/null && tls_ms=0
    [ "$ws_ms" -lt 0 ] 2>/dev/null && ws_ms=0

    echo "${dns_ms} ${tcp_ms} ${tls_ms} ${ws_ms} ${total_ms} ${http_code}"
}

# ===================== 独立 DNS 诊断 =====================

diagnose_dns() {
    local domain="$1"
    echo -e "\n${CYAN}[诊断] DNS 解析详情：${NC}"

    # 获取解析的 IP 地址
    local ips
    ips=$(dig "$domain" A +short 2>/dev/null | head -5)
    if [ -z "$ips" ]; then
        echo -e "  ${RED}DNS 解析失败，无法获取 IP 地址！${NC}"
        echo -e "  建议：尝试 dig @8.8.8.8 $domain A"
        return 1
    fi

    echo -e "  解析结果："
    while IFS= read -r ip; do
        echo -e "    → ${GREEN}$ip${NC}"
    done <<< "$ips"

    # 检查是否使用 CDN/CNAME
    local cname
    cname=$(dig "$domain" CNAME +short 2>/dev/null)
    if [ -n "$cname" ]; then
        echo -e "  CNAME 指向：${BLUE}$cname${NC}"
    fi
}

# ===================== 主函数 =====================

main() {
    if [ $# -lt 1 ]; then
        show_usage
        exit 1
    fi

    # 解析命令行参数
    parse_args "$@"

    local url="$PARSED_URL"
    local rounds="$PARSED_ROUNDS"

    # 检查依赖
    check_dependencies

    # 解析 URL（内部会结合 force_proto 确定最终协议）
    parse_url "$url"

    # ==================== 打印头部信息 ====================
    echo ""
    print_double_separator
    echo -e "${BOLD}  WebSocket 连接延迟检测工具${NC}"
    print_double_separator
    # 构建实际完整 URL 用于显示
    local display_url="${proto}://${domain}:${port}${path_part}"
    echo -e "  ${DIM}原始输入${NC}  ：$url"
    echo -e "  ${DIM}实际地址${NC}  ：$display_url"
    if [ -n "$force_proto" ]; then
        echo -e "  ${DIM}协议类型${NC}  ：${BOLD}${proto}${NC} ${YELLOW}(由 -p 参数指定)${NC}"
    else
        echo -e "  ${DIM}协议类型${NC}  ：${proto}"
    fi
    if [ "$proto" = "wss" ]; then
        echo -e "  ${DIM}安全连接${NC}  ：${GREEN}是（TLS 加密）${NC}"
    else
        echo -e "  ${DIM}安全连接${NC}  ：${YELLOW}否（明文传输）${NC}"
    fi
    echo -e "  ${DIM}目标域名${NC}  ：$domain"
    echo -e "  ${DIM}目标端口${NC}  ：$port"
    echo -e "  ${DIM}请求路径${NC}  ：$path_part"
    echo -e "  ${DIM}检测环节${NC}  ：DNS → TCP$([ "$proto" = "wss" ] && echo " → TLS") → WS Upgrade"
    echo -e "  ${DIM}测试轮数${NC}  ：$rounds"
    echo -e "  ${DIM}测试时间${NC}  ：$(date '+%Y-%m-%d %H:%M:%S')"
    print_double_separator

    # ==================== DNS 诊断 ====================
    diagnose_dns "$domain"

    # ==================== 多轮测量 ====================
    echo -e "\n${CYAN}[测量] 正在进行 $rounds 轮连接测试...${NC}\n"

    local all_dns=()
    local all_tcp=()
    local all_tls=()
    local all_ws=()
    local all_total=()
    local last_http_code=""
    local success_count=0
    local fail_count=0

    for ((round = 1; round <= rounds; round++)); do
        echo -ne "  第 ${round}/${rounds} 轮测试..."

        local timing_raw
        timing_raw=$(run_single_measurement "$proto" "$domain" "$port" "$path_part")

        if [ "$timing_raw" = "ERROR" ]; then
            echo -e " ${RED}失败（连接超时或网络不可达）${NC}"
            fail_count=$((fail_count + 1))
            continue
        fi

        local parsed
        parsed=$(parse_timing "$timing_raw" "$proto")

        local dns_ms tcp_ms tls_ms ws_ms total_ms http_code
        dns_ms=$(echo "$parsed" | awk '{print $1}')
        tcp_ms=$(echo "$parsed" | awk '{print $2}')
        tls_ms=$(echo "$parsed" | awk '{print $3}')
        ws_ms=$(echo "$parsed" | awk '{print $4}')
        total_ms=$(echo "$parsed" | awk '{print $5}')
        http_code=$(echo "$parsed" | awk '{print $6}')
        last_http_code="$http_code"

        all_dns+=("$dns_ms")
        all_tcp+=("$tcp_ms")
        all_tls+=("$tls_ms")
        all_ws+=("$ws_ms")
        all_total+=("$total_ms")

        success_count=$((success_count + 1))

        # 显示单轮概要
        if [ "$proto" = "wss" ]; then
            echo -e " ${GREEN}完成${NC}  DNS:${dns_ms}ms  TCP:${tcp_ms}ms  TLS:${tls_ms}ms  WS:${ws_ms}ms  总计:${total_ms}ms  [HTTP ${http_code}]"
        else
            echo -e " ${GREEN}完成${NC}  DNS:${dns_ms}ms  TCP:${tcp_ms}ms  WS:${ws_ms}ms  总计:${total_ms}ms  [HTTP ${http_code}]"
        fi

        # 轮次之间短暂间隔，避免干扰
        [ "$round" -lt "$rounds" ] && sleep 0.5
    done

    # 检查是否至少有一轮成功
    if [ "$success_count" -eq 0 ]; then
        echo -e "\n${RED}所有测试轮次均失败！请检查网络连通性。${NC}"
        echo -e "排查建议："
        echo -e "  1. 检查域名解析：dig $domain"
        echo -e "  2. 检查端口连通：curl -v https://$domain:$port/"
        echo -e "  3. 检查防火墙/安全组规则"
        echo -e "  4. 检查代理配置：echo \$http_proxy \$https_proxy"
        exit 1
    fi

    # ==================== 计算统计数据 ====================
    # 计算平均值和最小/最大值（兼容 bash 4.2 以下，不使用 nameref）
    calc_stats() {
        local arr_name=$1
        local sum=0 min=999999 max=0
        local count
        eval "count=\${#${arr_name}[@]}"
        if [ "$count" -eq 0 ]; then
            echo "0 0 0"
            return
        fi
        local i v
        for ((i = 0; i < count; i++)); do
            eval "v=\${${arr_name}[$i]}"
            sum=$((sum + v))
            [ "$v" -lt "$min" ] && min=$v
            [ "$v" -gt "$max" ] && max=$v
        done
        local avg=$((sum / count))
        echo "$avg $min $max"
    }

    local dns_stats tcp_stats tls_stats ws_stats total_stats
    dns_stats=$(calc_stats "all_dns")
    tcp_stats=$(calc_stats "all_tcp")
    tls_stats=$(calc_stats "all_tls")
    ws_stats=$(calc_stats "all_ws")
    total_stats=$(calc_stats "all_total")

    local dns_avg dns_min dns_max
    dns_avg=$(echo "$dns_stats" | awk '{print $1}')
    dns_min=$(echo "$dns_stats" | awk '{print $2}')
    dns_max=$(echo "$dns_stats" | awk '{print $3}')

    local tcp_avg tcp_min tcp_max
    tcp_avg=$(echo "$tcp_stats" | awk '{print $1}')
    tcp_min=$(echo "$tcp_stats" | awk '{print $2}')
    tcp_max=$(echo "$tcp_stats" | awk '{print $3}')

    local tls_avg tls_min tls_max
    tls_avg=$(echo "$tls_stats" | awk '{print $1}')
    tls_min=$(echo "$tls_stats" | awk '{print $2}')
    tls_max=$(echo "$tls_stats" | awk '{print $3}')

    local ws_avg ws_min ws_max
    ws_avg=$(echo "$ws_stats" | awk '{print $1}')
    ws_min=$(echo "$ws_stats" | awk '{print $2}')
    ws_max=$(echo "$ws_stats" | awk '{print $3}')

    local total_avg total_min total_max
    total_avg=$(echo "$total_stats" | awk '{print $1}')
    total_min=$(echo "$total_stats" | awk '{print $2}')
    total_max=$(echo "$total_stats" | awk '{print $3}')

    # 计算各阶段累加的平均总耗时（用于百分比计算）
    local sum_avg
    if [ "$proto" = "wss" ]; then
        sum_avg=$((dns_avg + tcp_avg + tls_avg + ws_avg))
    else
        sum_avg=$((dns_avg + tcp_avg + ws_avg))
    fi
    [ "$sum_avg" -eq 0 ] && sum_avg=1  # 防止除零

    # ==================== 输出详细报告 ====================
    echo ""
    print_double_separator
    echo -e "${BOLD}  📊 性能分析报告（基于 ${success_count} 轮成功测试${fail_count:+, ${fail_count} 轮失败}）${NC}"
    print_double_separator

    # 表头
    printf "  ${BOLD}%-14s %8s %8s %8s %6s  %-8s  %-s${NC}\n" "阶段" "平均" "最小" "最大" "占比" "评级" "分布"
    print_separator

    # DNS 解析
    local dns_pct=$((dns_avg * 100 / sum_avg))
    local dns_bar
    dns_bar=$(generate_bar "$dns_avg" "$sum_avg")
    local dns_rating
    dns_rating=$(get_rating "$dns_avg" "$DNS_THRESHOLD_GOOD" "$DNS_THRESHOLD_WARN")
    printf "  %-18s %5s ms %5s ms %5s ms %4s%%  " "🔍 DNS解析" "$dns_avg" "$dns_min" "$dns_max" "$dns_pct"
    echo -e "${dns_rating}  ${BLUE}${dns_bar}${NC}"

    # TCP 握手
    local tcp_pct=$((tcp_avg * 100 / sum_avg))
    local tcp_bar
    tcp_bar=$(generate_bar "$tcp_avg" "$sum_avg")
    local tcp_rating
    tcp_rating=$(get_rating "$tcp_avg" "$TCP_THRESHOLD_GOOD" "$TCP_THRESHOLD_WARN")
    printf "  %-18s %5s ms %5s ms %5s ms %4s%%  " "🤝 TCP握手" "$tcp_avg" "$tcp_min" "$tcp_max" "$tcp_pct"
    echo -e "${tcp_rating}  ${CYAN}${tcp_bar}${NC}"

    # TLS 握手（仅 wss）
    if [ "$proto" = "wss" ]; then
        local tls_pct=$((tls_avg * 100 / sum_avg))
        local tls_bar
        tls_bar=$(generate_bar "$tls_avg" "$sum_avg")
        local tls_rating
        tls_rating=$(get_rating "$tls_avg" "$TLS_THRESHOLD_GOOD" "$TLS_THRESHOLD_WARN")
        printf "  %-18s %5s ms %5s ms %5s ms %4s%%  " "🔒 TLS握手" "$tls_avg" "$tls_min" "$tls_max" "$tls_pct"
        echo -e "${tls_rating}  ${MAGENTA}${tls_bar}${NC}"
    fi

    # WebSocket Upgrade
    local ws_pct=$((ws_avg * 100 / sum_avg))
    local ws_bar
    ws_bar=$(generate_bar "$ws_avg" "$sum_avg")
    local ws_rating
    ws_rating=$(get_rating "$ws_avg" "$WS_THRESHOLD_GOOD" "$WS_THRESHOLD_WARN")
    printf "  %-18s %5s ms %5s ms %5s ms %4s%%  " "🔄 WS升级" "$ws_avg" "$ws_min" "$ws_max" "$ws_pct"
    echo -e "${ws_rating}  ${YELLOW}${ws_bar}${NC}"

    print_separator

    # 总计
    local total_rating
    total_rating=$(get_rating "$total_avg" "$TOTAL_THRESHOLD_GOOD" "$TOTAL_THRESHOLD_WARN")
    printf "  %-18s %5s ms %5s ms %5s ms  100%%  " "📈 总计" "$total_avg" "$total_min" "$total_max"
    echo -e "${total_rating}"

    print_double_separator

    # ==================== 瓶颈分析 ====================
    echo -e "\n${BOLD}  🔎 瓶颈分析${NC}"
    print_separator

    # 找出耗时最大的阶段
    local bottleneck=""
    local bottleneck_ms=0
    local bottleneck_suggestion=""

    if [ "$dns_avg" -gt "$bottleneck_ms" ]; then
        bottleneck="DNS解析"
        bottleneck_ms=$dns_avg
        bottleneck_suggestion="建议：\n    • 使用本地 DNS 缓存（如 nscd/dnsmasq）\n    • 更换公共 DNS（如 8.8.8.8 / 119.29.29.29）\n    • 检查 /etc/resolv.conf 配置\n    • 考虑在应用层缓存 DNS 结果"
    fi
    if [ "$tcp_avg" -gt "$bottleneck_ms" ]; then
        bottleneck="TCP握手"
        bottleneck_ms=$tcp_avg
        bottleneck_suggestion="建议：\n    • 检查客户端到服务端的网络延迟：ping $domain\n    • 检查网络路由：traceroute $domain\n    • 考虑使用离客户端更近的接入节点或 CDN\n    • 启用 TCP Fast Open (TFO)"
    fi
    if [ "$proto" = "wss" ] && [ "$tls_avg" -gt "$bottleneck_ms" ]; then
        bottleneck="TLS握手"
        bottleneck_ms=$tls_avg
        bottleneck_suggestion="建议：\n    • 启用 TLS Session Resumption / TLS 1.3\n    • 检查证书链是否过长：openssl s_client -connect $domain:$port\n    • 启用 OCSP Stapling 减少验证延迟\n    • 考虑使用 CDN 进行 TLS 终结"
    fi
    if [ "$ws_avg" -gt "$bottleneck_ms" ]; then
        bottleneck="WebSocket升级"
        bottleneck_ms=$ws_avg
        bottleneck_suggestion="建议：\n    • 检查服务端 WebSocket Upgrade 处理逻辑\n    • 查看服务端日志是否有慢请求记录\n    • 检查是否有中间代理（Nginx/负载均衡）引入延迟\n    • 检查服务端是否有认证/鉴权环节拖慢响应"
    fi

    echo -e "  ${RED}⚠ 最大瓶颈：${BOLD}${bottleneck}${NC}${RED}（平均 ${bottleneck_ms}ms，占总耗时 $((bottleneck_ms * 100 / sum_avg))%）${NC}"
    echo -e "  ${bottleneck_suggestion}"

    # HTTP 状态码提示
    if [ -n "$last_http_code" ]; then
        echo ""
        case "$last_http_code" in
            101)
                echo -e "  ${GREEN}✅ HTTP 状态码 101 — WebSocket Upgrade 成功${NC}"
                ;;
            200)
                echo -e "  ${YELLOW}⚠ HTTP 状态码 200 — 服务端返回普通 HTTP 响应，未升级为 WebSocket${NC}"
                echo -e "    可能原因：服务端不支持 WebSocket 或需要特定请求头/参数"
                ;;
            301|302|307|308)
                echo -e "  ${YELLOW}⚠ HTTP 状态码 $last_http_code — 发生重定向${NC}"
                echo -e "    建议：检查目标地址是否正确，是否需要跟随重定向"
                ;;
            400)
                echo -e "  ${YELLOW}⚠ HTTP 状态码 400 — 请求参数可能有误${NC}"
                ;;
            403)
                echo -e "  ${RED}⚠ HTTP 状态码 403 — 访问被拒绝，可能缺少鉴权信息${NC}"
                ;;
            404)
                echo -e "  ${RED}⚠ HTTP 状态码 404 — WebSocket 端点不存在${NC}"
                echo -e "    建议：确认请求路径 $path_part 是否正确"
                ;;
            502|503|504)
                echo -e "  ${RED}⚠ HTTP 状态码 $last_http_code — 服务端异常${NC}"
                echo -e "    建议：检查服务端运行状态和上游服务健康"
                ;;
            000)
                echo -e "  ${RED}⚠ HTTP 状态码 000 — 未收到响应（连接被重置或超时）${NC}"
                ;;
            *)
                echo -e "  ${DIM}HTTP 状态码：$last_http_code${NC}"
                ;;
        esac
    fi

    # ==================== 连接流程时序图 ====================
    echo ""
    print_separator
    echo -e "  ${BOLD}📐 连接流程时序图${NC}"
    print_separator

    local cursor=0
    local scale_factor=1
    # 自动调整刻度：当总耗时很大时缩小刻度
    if [ "$sum_avg" -gt 1000 ]; then
        scale_factor=$((sum_avg / 40))
    elif [ "$sum_avg" -gt 0 ]; then
        scale_factor=$((sum_avg / 30))
    fi
    [ "$scale_factor" -eq 0 ] && scale_factor=1

    echo -e "  ${DIM}0ms${NC}"
    echo -e "  │"

    # DNS
    local dns_width=$((dns_avg / scale_factor))
    [ "$dns_width" -eq 0 ] && [ "$dns_avg" -gt 0 ] && dns_width=1
    local dns_block=""
    for ((i = 0; i < dns_width; i++)); do dns_block="${dns_block}▓"; done
    echo -e "  ├─${BLUE}${dns_block}${NC}─ DNS解析 (${dns_avg}ms)"
    cursor=$((cursor + dns_avg))
    echo -e "  │ ${DIM}${cursor}ms${NC}"

    # TCP
    local tcp_width=$((tcp_avg / scale_factor))
    [ "$tcp_width" -eq 0 ] && [ "$tcp_avg" -gt 0 ] && tcp_width=1
    local tcp_block=""
    for ((i = 0; i < tcp_width; i++)); do tcp_block="${tcp_block}▓"; done
    echo -e "  ├─${CYAN}${tcp_block}${NC}─ TCP握手 (${tcp_avg}ms)"
    cursor=$((cursor + tcp_avg))
    echo -e "  │ ${DIM}${cursor}ms${NC}"

    # TLS（仅 wss）
    if [ "$proto" = "wss" ]; then
        local tls_width=$((tls_avg / scale_factor))
        [ "$tls_width" -eq 0 ] && [ "$tls_avg" -gt 0 ] && tls_width=1
        local tls_block=""
        for ((i = 0; i < tls_width; i++)); do tls_block="${tls_block}▓"; done
        echo -e "  ├─${MAGENTA}${tls_block}${NC}─ TLS握手 (${tls_avg}ms)"
        cursor=$((cursor + tls_avg))
        echo -e "  │ ${DIM}${cursor}ms${NC}"
    fi

    # WS Upgrade
    local ws_width=$((ws_avg / scale_factor))
    [ "$ws_width" -eq 0 ] && [ "$ws_avg" -gt 0 ] && ws_width=1
    local ws_block=""
    for ((i = 0; i < ws_width; i++)); do ws_block="${ws_block}▓"; done
    echo -e "  └─${YELLOW}${ws_block}${NC}─ WS升级 (${ws_avg}ms)"
    echo -e "    ${DIM}${sum_avg}ms (各阶段累计)${NC}"

    # ==================== 尾部信息 ====================
    echo ""
    print_double_separator
    echo -e "  ${DIM}测试完成于 $(date '+%Y-%m-%d %H:%M:%S') | 成功 $success_count/$rounds 轮 | curl 版本: $(curl --version | head -1 | awk '{print $2}')${NC}"
    print_double_separator
    echo ""
}

# 执行主函数
main "$@"
