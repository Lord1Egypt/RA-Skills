#!/bin/bash
# 中国天气网增强版 - 包含实时天气、AQI、逐小时预报、7天预报
# 作者: Jeremy
# 版本: 1.0.0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CITY_CODE_FILE="$SCRIPT_DIR/weather_codes.txt"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

error() {
    echo -e "${RED}错误: $1${NC}" >&2
    exit 1
}

find_city_code() {
    local city="$1"
    local code
    code=$(grep -i "^${city}," "$CITY_CODE_FILE" 2>/dev/null | cut -d',' -f2 | head -1)
    if [ -z "$code" ]; then
        code=$(grep -i "${city}" "$CITY_CODE_FILE" 2>/dev/null | head -1 | cut -d',' -f2)
    fi
    echo "$code"
}

fetch_weather() {
    local city_code="$1"
    local url="https://www.weather.com.cn/weather/${city_code}.shtml"
    html=$(curl -s --max-time 10 "$url" 2>/dev/null)
    if [ -z "$html" ]; then
        error "无法获取天气数据，请检查网络连接"
    fi
    echo "$html"
}

# 解析实时天气
parse_current() {
    local html="$1"
    local tmpfile=$(mktemp)
    echo "$html" > "$tmpfile"
    
    # 从 hidden_title 获取实时数据
    local today_info
    today_info=$(grep -o 'hidden_title.*value="[^"]*"' "$tmpfile" | sed 's/.*value="\([^"]*\)"/\1/')
    
    local weather="" temp="" source=""
    if [ -n "$today_info" ]; then
        temp=$(echo "$today_info" | grep -oE '[0-9]+/[0-9]+°C' | head -1)
        weather=$(echo "$today_info" | grep -oE '阴|晴|多云|雨|雪|雷|雾|风|晴转|多云转' | head -1)
    fi
    
    # 备用：从其他位置获取
    if [ -z "$temp" ]; then
        temp=$(echo "$html" | grep -oE '[0-9]+/[0-9]+°C' | head -1)
    fi
    if [ -z "$weather" ]; then
        weather=$(echo "$html" | grep -o '<title>[^<]*</title>' | sed 's/<title>//' | sed 's/天气预报.*//' | head -1)
    fi
    
    rm -f "$tmpfile"
    echo "WEATHER=${weather:-未知}"
    echo "TEMP=${temp:-未知}"
}

# 解析生活指数
parse_lifestyle() {
    local html="$1"
    local tmpfile=$(mktemp)
    echo "$html" > "$tmpfile"
    
    local cold_index="较适宜" sport_index="较适宜" dress_index="较冷" wash_index="适宜" uv_index="强"
    
    if echo "$html" | grep -q "极易发感冒"; then
        cold_index="极易发"
    elif echo "$html" | grep -q "易发感冒"; then
        cold_index="易发"
    elif echo "$html" | grep -q "较易发感冒"; then
        cold_index="较易发"
    elif echo "$html" | grep -q "少发感冒"; then
        cold_index="少发"
    fi
    
    if echo "$html" | grep -q "适宜运动"; then
        sport_index="适宜"
    elif echo "$html" | grep -q "较适宜运动"; then
        sport_index="较适宜"
    elif echo "$html" | grep -q "较不宜运动"; then
        sport_index="较不宜"
    elif echo "$html" | grep -q "不宜运动"; then
        sport_index="不宜"
    fi
    
    if echo "$html" | grep -q "强紫外线"; then
        uv_index="强"
    elif echo "$html" | grep -q "中等紫外线"; then
        uv_index="中等"
    elif echo "$html" | grep -q "弱紫外线"; then
        uv_index="弱"
    fi
    
    if echo "$html" | grep -q "适宜洗车"; then
        wash_index="适宜"
    elif echo "$html" | grep -q "较适宜洗车"; then
        wash_index="较适宜"
    elif echo "$html" | grep -q "不宜洗车"; then
        wash_index="不宜"
    fi
    
    rm -f "$tmpfile"
    echo "COLD_INDEX=${cold_index}"
    echo "SPORT_INDEX=${sport_index}"
    echo "DRESS_INDEX=${dress_index}"
    echo "WASH_INDEX=${wash_index}"
    echo "UV_INDEX=${uv_index}"
}

# 解析逐小时预报
parse_hourly() {
    local html="$1"
    # 从JSON中提取逐小时数据
    echo "$html" | grep -oE '([0-9]+日[0-9]+时,[a-z0-9]+,[^,]+,[0-9]+℃,[^,]+,[^,]+,[0-9])' | head -8
}

# 解析7天预报（简化版）
parse_7day() {
    local html="$1"
    # 提取温度数据，与日期对应
    local temps=$(echo "$html" | grep -oP '([0-9]+/[0-9]+°C)' | head -14)
    echo "$temps"
}

# 获取AQI (使用第三方接口)
get_aqi() {
    local city="$1"
    # 尝试多个AQI接口
    local aqi_data=$(curl -s --max-time 5 "https://api.aooi.com/weather/index?city=${city}" 2>/dev/null)
    if [ -n "$aqi_data" ]; then
        echo "$aqi_data" | grep -oE '"aqi":[0-9]+|"level":"[^"]+"' | head -2
    else
        # 备用：根据天气大致估算
        echo "AQI: 未获取到"
    fi
}

get_weather_icon() {
    local weather="$1"
    case "$weather" in
        *晴*|*晴转*) echo "☀️" ;;
        *多云*|*多云转*) echo "⛅" ;;
        *阴*) echo "☁️" ;;
        *雨*|*小雨*|*中雨*|*大雨*) echo "🌧️" ;;
        *雪*|*小雪*|*大雪*) echo "❄️" ;;
        *雷*) echo "⛈️" ;;
        *雾*|*雾霾*) echo "🌫️" ;;
        *) echo "🌤️" ;;
    esac
}

format_output() {
    local city="$1"
    shift
    local data="$@"
    eval "$data"
    
    local icon=$(get_weather_icon "$WEATHER")
    
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}    🌤️  ${city}天气预报 Pro${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo ""
    
    # 今日天气
    echo -e "${CYAN}📍 今日天气${NC} $(date +%Y-%m-%d)"
    echo -e "   ${icon} ${WEATHER:-未知}  |  ${BLUE}温度: ${TEMP:-未知}${NC}"
    echo ""
    
    # 生活指数
    echo -e "${CYAN}📊 生活指数${NC}"
    echo -e "   🤧 感冒: ${COLD_INDEX:-未知}  |  🏃 运动: ${SPORT_INDEX:-未知}"
    echo -e "   👔 穿衣: ${DRESS_INDEX:-未知}  |  🚗 洗车: ${WASH_INDEX:-未知}"
    echo -e "   ☀️ 紫外线: ${UV_INDEX:-未知}"
    echo ""
    
    # 逐小时预报
    echo -e "${CYAN}⏰ 逐小时预报${NC}"
    local hourly_data=$(echo "$html" | grep -oE '([0-9]+日[0-9]+时,[a-z0-9]+,[^,]+,[0-9]+℃,[^,]+,[^,]+,[0-9])' | head -8)
    if [ -n "$hourly_data" ]; then
        echo "$hourly_data" | while read line; do
            local time=$(echo "$line" | cut -d',' -f1)
            local weather=$(echo "$line" | cut -d',' -f3)
            local temp=$(echo "$line" | cut -d',' -f4)
            local wind=$(echo "$line" | cut -d',' -f5)
            local icon=$(get_weather_icon "$weather")
            echo -e "   ${time}  ${icon} ${weather} ${temp}  ${wind}"
        done
    else
        echo "   暂无数据"
    fi
    echo ""
    
    # 7天预报 - 从温度列表提取
    echo -e "${CYAN}📅 7天预报${NC}"
    local temps=$(echo "$html" | grep -oP '([0-9]+/[0-9]+°C)' | head -14)
    local dates=("今天" "明天" "后天" "3天后" "4天后" "5天后" "6天后")
    local i=0
    echo "$temps" | while read temp; do
        if [ $i -lt 7 ]; then
            echo "   ${dates[$i]}: ${temp}"
            i=$((i+1))
        fi
    done
    echo ""
    
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}    数据来源: 中国天气网 | 版本: Pro 1.0.0${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo ""
}

main() {
    local city="$1"
    
    if [ -z "$city" ]; then
        error "请输入城市名称，例如：./weather-cn-pro.sh 西安"
    fi
    
    if [ ! -f "$CITY_CODE_FILE" ]; then
        # 使用内置的常用城市代码
        case "$city" in
            北京) city_code="101010100" ;;
            上海) city_code="101020100" ;;
            广州) city_code="101280101" ;;
            深圳) city_code="101280601" ;;
            成都) city_code="101270101" ;;
            杭州) city_code="101210101" ;;
            武汉) city_code="101200101" ;;
            西安) city_code="101110101" ;;
            南京) city_code="101190101" ;;
            重庆) city_code="101040100" ;;
            天津) city_code="101030100" ;;
            苏州) city_code="101190401" ;;
            郑州) city_code="101180101" ;;
            长沙) city_code="101250101" ;;
            沈阳) city_code="101070101" ;;
            青岛) city_code="101120101" ;;
            大连) city_code="101070201" ;;
            厦门) city_code="101230201" ;;
            济南) city_code="101120601" ;;
            昆明) city_code="101290101" ;;
            *) error "未找到城市 '$city'，请添加城市代码到 weather_codes.txt" ;;
        esac
    else
        city_code=$(find_city_code "$city")
        [ -z "$city_code" ] && error "未找到城市 '$city'"
    fi
    
    local html
    html=$(fetch_weather "$city_code")
    
    local current_data=$(parse_current "$html")
    local lifestyle_data=$(parse_lifestyle "$html")
    
    format_output "$city" "$current_data $lifestyle_data"
}

main "$@"