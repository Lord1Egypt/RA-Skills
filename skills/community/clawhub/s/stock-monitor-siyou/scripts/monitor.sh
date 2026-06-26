#!/bin/bash
# Stock Monitor - 股票监控主脚本（增强版）
# 用法：bash monitor.sh [-c config] [-o] [-v] [-h]
# 监控规则：
# 1. 集合竞价（9:15-9:25）：涨跌≥阈值 提醒
# 2. 盘中（9:30-11:30, 13:00-14:57）：涨停/跌停连发 3 条
# 3. 每 10 分钟：10 分钟内振幅>阈值 提醒

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# 默认配置
CONFIG_FILE="$BASE_DIR/stocks.conf"
VERBOSE=false
ONCE=false

# 缓存文件
CACHE_DIR="/tmp/stock_monitor_cache"
mkdir -p "$CACHE_DIR"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# 打印帮助
print_help() {
    cat << EOF
📊 Stock Monitor - 股票自动监控（增强版）

用法：bash $0 [选项]

选项:
  -c, --config <file>     配置文件路径（默认：stocks.conf）
  -o, --once              只运行一次，不监控
  -v, --verbose           详细输出
  -h, --help              显示帮助

监控规则:
  1. 集合竞价（9:15-9:25）：涨跌≥2% 提醒
  2. 盘中（9:30-11:30, 13:00-14:57）：涨停/跌停连发 3 条
  3. 每 10 分钟：10 分钟内振幅>2% 提醒

EOF
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -o|--once)
            ONCE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            echo -e "${RED}❌ 未知选项：$1${NC}"
            print_help
            exit 1
            ;;
    esac
done

# 检查配置文件
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}❌ 错误：配置文件不存在：$CONFIG_FILE${NC}"
    exit 1
fi

# 检查环境变量
if [ -z "$FEISHU_APP_ID" ] || [ -z "$FEISHU_APP_SECRET" ] || [ -z "$FEISHU_CHAT_ID" ]; then
    echo -e "${RED}❌ 错误：缺少 Feishu 配置${NC}"
    exit 1
fi

if [ -z "$NOIZ_API_KEY" ]; then
    echo -e "${RED}❌ 错误：缺少 NoizAI API Key${NC}"
    exit 1
fi

# 检查是否是节假日
is_holiday() {
    local today=$(date +%Y-%m-%d)
    local holiday_file="$BASE_DIR/holidays.conf"
    
    if [ -f "$holiday_file" ]; then
        if grep -q "^$today," "$holiday_file" 2>/dev/null; then
            local holiday_name=$(grep "^$today," "$holiday_file" | cut -d',' -f2)
            echo "$holiday_name"
            return 0
        fi
    fi
    
    return 1
}

# 检查交易时段
check_trading_session() {
    local current_time=$(date +%H%M)
    local weekday=$(date +%u)
    local today=$(date +%Y-%m-%d)
    
    # 检查节假日
    local holiday_name=$(is_holiday)
    if [ -n "$holiday_name" ]; then
        echo "holiday:$holiday_name"
        return 1
    fi
    
    # 周末
    if [ "$weekday" -ge 6 ]; then
        echo "weekend"
        return 1
    fi
    
    # 集合竞价：9:15-9:25
    if [ "$current_time" -ge 915 ] && [ "$current_time" -lt 925 ]; then
        echo "call_auction"
        return 0
    fi
    
    # 早盘：9:30-11:30
    if [ "$current_time" -ge 930 ] && [ "$current_time" -lt 1130 ]; then
        echo "morning"
        return 0
    fi
    
    # 午盘：13:00-14:57
    if [ "$current_time" -ge 1300 ] && [ "$current_time" -lt 1457 ]; then
        echo "afternoon"
        return 0
    fi
    
    # 其他时间
    echo "closed"
    return 1
}

# 获取股票价格
get_stock_price() {
    local stock_code="$1"
    local response=$(curl -s "https://hq.sinajs.cn/list=$stock_code" 2>/dev/null | timeout 5 cat)
    
    if [ -z "$response" ] || [[ "$response" == *"Forbidden"* ]]; then
        echo "ERROR||0"
        return 1
    fi
    
    local data=$(echo "$response" | cut -d'"' -f2)
    if [ -z "$data" ]; then
        echo "ERROR||0"
        return 1
    fi
    
    local name=$(echo "$data" | cut -d',' -f1)
    local current=$(echo "$data" | cut -d',' -f2)
    local open=$(echo "$data" | cut -d',' -f3)
    local yesterday=$(echo "$data" | cut -d',' -f4)
    local high=$(echo "$data" | cut -d',' -f5)
    local low=$(echo "$data" | cut -d',' -f6)
    
    # 计算涨跌幅
    if [ -n "$yesterday" ] && [ "$yesterday" != "0" ]; then
        local change=$(echo "scale=2; (($current - $yesterday) / $yesterday) * 100" | bc 2>/dev/null || echo "0")
    else
        local change="0"
    fi
    
    # 返回：名称 | 现价 | 涨跌幅 | 开盘 | 最高 | 最低 | 昨收
    echo "$name|$current|$change|$open|$high|$low|$yesterday"
}

# 计算涨停跌停价
get_limit_price() {
    local yesterday="$1"
    local change_limit="$2"  # 10% 或 20%
    
    local up_limit=$(echo "scale=2; $yesterday * (1 + $change_limit / 100)" | bc 2>/dev/null || echo "0")
    local down_limit=$(echo "scale=2; $yesterday * (1 - $change_limit / 100)" | bc 2>/dev/null || echo "0")
    
    echo "$up_limit|$down_limit"
}

# 发送语音提醒
send_voice_alert() {
    local message="$1"
    local repeat="$2"  # 重复次数
    
    echo -e "${BLUE}🎤 发送语音提醒...${NC}"
    
    for i in $(seq 1 $repeat); do
        if [ -d "$BASE_DIR/../feishu-edge-tts/scripts" ]; then
            bash "$BASE_DIR/../feishu-edge-tts/scripts/send_voice.sh" -t "$message" --no-send false 2>&1 | tail -3
        else
            echo "语音：$message"
        fi
        sleep 1
    done
}

# 发送文字提醒
send_text_alert() {
    local message="$1"
    
    echo -e "${MAGENTA}📝 发送文字提醒...${NC}"
    echo "$message"
}

# 检查集合竞价异动
check_call_auction() {
    local stock_code="$1"
    local stock_name="$2"
    local threshold="$3"
    
    local result=$(get_stock_price "$stock_code")
    local name=$(echo "$result" | cut -d'|' -f1)
    local open=$(echo "$result" | cut -d'|' -f4)
    local change=$(echo "$result" | cut -d'|' -f3)
    
    if [ "$result" == "ERROR||0" ]; then
        return
    fi
    
    # 检查是否达到阈值
    local change_abs=$(echo "$change" | tr -d '-')
    
    if (( $(echo "$change_abs >= $threshold" | bc -l 2>/dev/null || echo 0) )); then
        local direction="涨"
        if (( $(echo "$change < 0" | bc -l 2>/dev/null || echo 0) )); then
            direction="跌"
        fi
        
        local message="主人～ 集合竞价异动！$stock_name 开盘${change}%，达到${threshold}%阈值！请留意！"
        echo -e "${YELLOW}⚠️  集合竞价异动：$stock_name $change%${NC}"
        
        send_voice_alert "$message" 1
    fi
}

# 检查涨停跌停
check_limit_up_down() {
    local stock_code="$1"
    local stock_name="$2"
    local yesterday="$3"
    local current="$4"
    
    # 判断是主板还是创业板/科创板
    local change_limit="10"
    if [[ "$stock_code" == sh688* ]] || [[ "$stock_code" == sz300* ]]; then
        change_limit="20"
    fi
    
    local limits=$(get_limit_price "$yesterday" "$change_limit")
    local up_limit=$(echo "$limits" | cut -d'|' -f1)
    local down_limit=$(echo "$limits" | cut -d'|' -f2)
    
    # 检查涨停
    if (( $(echo "$current >= $up_limit" | bc -l 2>/dev/null || echo 0) )); then
        local message="主人！$stock_name 涨停啦！现价$current 元，太棒了！🎉"
        echo -e "${GREEN}🎉 涨停：$stock_name $current 元${NC}"
        
        # 连发 3 条
        send_voice_alert "$message" 3
    fi
    
    # 检查跌停
    if (( $(echo "$current <= $down_limit" | bc -l 2>/dev/null || echo 0) )); then
        local message="主人...$stock_name 跌停了，现价$current 元，要注意风险...😟"
        echo -e "${RED}📉 跌停：$stock_name $current 元${NC}"
        
        # 连发 3 条
        send_voice_alert "$message" 3
    fi
}

# 检查 10 分钟振幅
check_10min_amplitude() {
    local stock_code="$1"
    local stock_name="$2"
    local threshold="$3"
    
    local cache_file="$CACHE_DIR/${stock_code}_10min.cache"
    local current_time=$(date +%s)
    
    # 获取当前价格
    local result=$(get_stock_price "$stock_code")
    local high=$(echo "$result" | cut -d'|' -f5)
    local low=$(echo "$result" | cut -d'|' -f6)
    local current=$(echo "$result" | cut -d'|' -f2)
    
    if [ "$result" == "ERROR||0" ]; then
        return
    fi
    
    # 读取缓存
    local prev_high=""
    local prev_low=""
    local prev_time=""
    
    if [ -f "$cache_file" ]; then
        prev_high=$(cat "$cache_file" | head -1)
        prev_low=$(cat "$cache_file" | tail -1)
        prev_time=$(stat -c %Y "$cache_file" 2>/dev/null || echo "0")
    fi
    
    # 更新缓存
    echo "$high" > "$cache_file"
    echo "$low" >> "$cache_file"
    
    # 如果是第一次，不检查
    if [ -z "$prev_high" ] || [ -z "$prev_low" ]; then
        return
    fi
    
    # 检查是否超过 10 分钟
    local time_diff=$((current_time - prev_time))
    if [ "$time_diff" -lt 600 ]; then
        return
    fi
    
    # 计算 10 分钟内振幅
    local max_high=$(echo "$high $prev_high" | awk '{print ($1>$2)?$1:$2}')
    local min_low=$(echo "$low $prev_low" | awk '{print ($1<$2)?$1:$2}')
    local amplitude=$(echo "scale=2; (($max_high - $min_low) / $min_low) * 100" | bc 2>/dev/null || echo "0")
    
    if (( $(echo "$amplitude >= $threshold" | bc -l 2>/dev/null || echo 0) )); then
        local message="主人～ $stock_name 10 分钟内振幅${amplitude}%，超过${threshold}%！有异动！"
        echo -e "${YELLOW}⚠️  10 分钟振幅：$stock_name ${amplitude}%${NC}"
        
        send_voice_alert "$message" 1
    fi
}

# 主监控逻辑
monitor_stocks() {
    local session="$1"
    
    echo -e "${BLUE}📊 开始监控股票（$session）...${NC}"
    echo "配置文件：$CONFIG_FILE"
    echo ""
    
    # 读取配置
    while IFS=',' read -r stock_code stock_name call_auction_threshold limit_check amplitude_threshold || [ -n "$stock_code" ]; do
        # 跳过空行和注释
        [[ -z "$stock_code" || "$stock_code" =~ ^# ]] && continue
        
        # 去除空格
        stock_code=$(echo "$stock_code" | tr -d ' ')
        stock_name=$(echo "$stock_name" | tr -d ' ')
        call_auction_threshold=${call_auction_threshold:-2}
        limit_check=${limit_check:-1}
        amplitude_threshold=${amplitude_threshold:-2}
        
        echo -e "${YELLOW}检查：$stock_name ($stock_code)${NC}"
        
        # 获取股价
        local result=$(get_stock_price "$stock_code")
        
        if [ "$result" == "ERROR||0" ]; then
            echo -e "${RED}  ❌ 获取股价失败${NC}"
            continue
        fi
        
        # 解析结果
        local name=$(echo "$result" | cut -d'|' -f1)
        local price=$(echo "$result" | cut -d'|' -f2)
        local change=$(echo "$result" | cut -d'|' -f3)
        local open=$(echo "$result" | cut -d'|' -f4)
        local high=$(echo "$result" | cut -d'|' -f5)
        local low=$(echo "$result" | cut -d'|' -f6)
        local yesterday=$(echo "$result" | cut -d'|' -f7)
        
        echo "  现价：$price 元"
        echo "  涨跌：$change%"
        
        # 根据时段执行不同检查
        case "$session" in
            call_auction)
                # 集合竞价检查
                check_call_auction "$stock_code" "$stock_name" "$call_auction_threshold"
                ;;
            morning|afternoon)
                # 盘中检查涨停跌停
                if [ "$limit_check" = "1" ]; then
                    check_limit_up_down "$stock_code" "$stock_name" "$yesterday" "$price"
                fi
                
                # 检查 10 分钟振幅
                check_10min_amplitude "$stock_code" "$stock_name" "$amplitude_threshold"
                ;;
        esac
        
        echo ""
        sleep 1  # 避免请求过快
        
    done < "$CONFIG_FILE"
    
    echo -e "${GREEN}✅ 监控完成${NC}"
}

# 主程序
echo "======================================"
echo "📊 Stock Monitor - 股票自动监控（增强版）"
echo "======================================"
echo ""

# 检查交易时段
session_info=$(check_trading_session)
session_type=$(echo "$session_info" | cut -d':' -f1)

case "$session_type" in
    holiday)
        holiday_name=$(echo "$session_info" | cut -d':' -f2)
        echo -e "${YELLOW}⏰ 今天节假日（$holiday_name），不监控${NC}"
        exit 0
        ;;
    weekend)
        echo -e "${YELLOW}⏰ 周末，不监控${NC}"
        exit 0
        ;;
    call_auction)
        echo -e "${GREEN}✅ 集合竞价时段（9:15-9:25）${NC}"
        monitor_stocks "call_auction"
        ;;
    morning)
        echo -e "${GREEN}✅ 早盘时段（9:30-11:30）${NC}"
        monitor_stocks "morning"
        ;;
    afternoon)
        echo -e "${GREEN}✅ 午盘时段（13:00-14:57）${NC}"
        monitor_stocks "afternoon"
        ;;
    closed)
        echo -e "${YELLOW}⏰ 非交易时间，不监控${NC}"
        exit 0
        ;;
esac
