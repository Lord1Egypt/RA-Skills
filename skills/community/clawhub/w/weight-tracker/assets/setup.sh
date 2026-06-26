#!/bin/bash
# 体重追踪器 - 初始化脚本
# 支持 macOS / Windows (WSL) / Linux

set -e

# ========== 平台检测 ==========
detect_platform() {
    local platform=$(uname -s)
    if [[ "$platform" == "Darwin" ]]; then
        echo "macos"
    elif [[ "$platform" == "Linux" ]]; then
        if grep -qEi "(Microsoft|WSL)" /proc/version 2>/dev/null; then
            echo "windows-wsl"
        else
            echo "linux"
        fi
    else
        echo "unknown"
    fi
}

PLATFORM=$(detect_platform)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ========== 跨平台工具函数 ==========

format_date() {
    local date_str=$1
    local format=$2
    if [ "$PLATFORM" == "macos" ]; then
        date -j -f "%Y-%m-%d" "$date_str" "+$format" 2>/dev/null || echo "$date_str"
    else
        date -d "$date_str" "+$format" 2>/dev/null || echo "$date_str"
    fi
}

get_today() {
    if [ "$PLATFORM" == "macos" ]; then
        date +%Y-%m-%d
    else
        date -I 2>/dev/null || date +%Y-%m-%d
    fi
}

get_future_date() {
    local days=${1:-90}
    if [ "$PLATFORM" == "macos" ]; then
        date -v+${days}d +%Y-%m-%d
    else
        date -d "+${days} days" +%Y-%m-%d 2>/dev/null || echo "$(get_today)"
    fi
}

is_port_available() {
    local port=$1
    if [ "$PLATFORM" == "macos" ]; then
        ! lsof -i :$port >/dev/null 2>&1
    else
        ! ss -tuln 2>/dev/null | grep -q ":$port " && ! netstat -tuln 2>/dev/null | grep -q ":$port "
    fi
}

get_available_ports() {
    local default_ports=(8000 8080 8888 3000 5000 9000)
    local available=()
    
    for port in "${default_ports[@]}"; do
        if is_port_available $port; then
            available+=($port)
        fi
        if [ ${#available[@]} -eq 3 ]; then
            break
        fi
    done
    
    if [ ${#available[@]} -lt 3 ]; then
        for port in 3001 5001 8001 8081 8889 9001; do
            if is_port_available $port; then
                available+=($port)
            fi
            if [ ${#available[@]} -eq 3 ]; then
                break
            fi
        done
    fi
    
    echo "${available[@]}"
}

# ========== 文本定义 ==========

# 英文文本
read_prompts_en() {
    GREETING="🏃 Weight Tracker - Setup Wizard"
    PLATFORM_INFO="Platform:"
    AVAILABLE_PORTS="Available ports:"
    ENTER_INFO="Enter your weight loss goal info:"
    PROMPT_TITLE="Title"
    PROMPT_TITLE_HINT="(e.g., My Weight Loss Journey)"
    PROMPT_LANG="Language"
    PROMPT_LANG_HINT="en = English, zh = 中文"
    PROMPT_PORT="Select port or enter custom port"
    PROMPT_PORT_HINT="(web server port for viewing the tracker)"
    PROMPT_PORT_CUSTOM="Enter port number:"
    PROMPT_START_WEIGHT="Start weight (kg)"
    PROMPT_START_WEIGHT_HINT="(your weight at the start)"
    PROMPT_TARGET_WEIGHT="Target weight (kg)"
    PROMPT_TARGET_WEIGHT_HINT="(your goal weight)"
    PROMPT_START_DATE="Start date"
    PROMPT_START_DATE_HINT="(YYYY-MM-DD, when your plan starts)"
    PROMPT_END_DATE="End date"
    PROMPT_END_DATE_HINT="(YYYY-MM-DD, when you plan to reach your goal)"
    PROMPT_INIT_WEIGHT="Current weight (kg)"
    PROMPT_INIT_WEIGHT_HINT="(your weight today)"
    PROMPT_INIT_DATE="Record date"
    PROMPT_INIT_DATE_HINT="(date for this weight record, default: today)"
    SELECT_PORT="Choice"
    INVALID_LANG="Invalid language, using 'en'"
    SETUP_COMPLETE="✅ Setup complete!"
    CONFIG="Config"
    DATA="Data"
    PORT="Port"
    TO_START="To start server, run:"
    TO_OPEN="Then open:"
    PRESS_W="Press W to export data"
    DONE="================================"
    SELECT_CUSTOM="Custom"
}

# 中文文本
read_prompts_zh() {
    GREETING="🏃 体重追踪器 - 设置向导"
    PLATFORM_INFO="平台:"
    AVAILABLE_PORTS="可用端口:"
    ENTER_INFO="请输入您的减肥目标信息:"
    PROMPT_TITLE="标题"
    PROMPT_TITLE_HINT="(例如: 我的减肥计划)"
    PROMPT_LANG="语言"
    PROMPT_LANG_HINT="en = English, zh = 中文"
    PROMPT_PORT="选择端口或输入自定义端口"
    PROMPT_PORT_HINT="(网页服务器的端口，用于查看追踪器)"
    PROMPT_PORT_CUSTOM="输入端口号:"
    PROMPT_START_WEIGHT="起始体重 (kg)"
    PROMPT_START_WEIGHT_HINT="(减肥计划开始时的体重)"
    PROMPT_TARGET_WEIGHT="目标体重 (kg)"
    PROMPT_TARGET_WEIGHT_HINT="(您想要达成的体重)"
    PROMPT_START_DATE="开始日期"
    PROMPT_START_DATE_HINT="(YYYY-MM-DD 格式，减肥计划开始的日期)"
    PROMPT_END_DATE="结束日期"
    PROMPT_END_DATE_HINT="(YYYY-MM-DD 格式，计划达成目标的日期)"
    PROMPT_INIT_WEIGHT="当前体重 (kg)"
    PROMPT_INIT_WEIGHT_HINT="(今天的体重)"
    PROMPT_INIT_DATE="记录日期"
    PROMPT_INIT_DATE_HINT="(这条体重记录的日期，默认今天)"
    SELECT_PORT="选择"
    INVALID_LANG="无效的语言，使用默认 'en'"
    SETUP_COMPLETE="✅ 设置完成!"
    CONFIG="配置文件"
    DATA="数据文件"
    PORT="端口"
    TO_START="启动服务器，运行:"
    TO_OPEN="然后打开:"
    PRESS_W="按 W 键导出数据"
    DONE="================================"
    SELECT_CUSTOM="自定义"
}

# ========== 主程序 ==========

echo "🏃 Weight Tracker - Setup Wizard"
echo "================================"
echo "Platform: $PLATFORM"
echo ""

# 读取当前配置作为默认值
if [ -f "$SCRIPT_DIR/config.json" ]; then
    DEFAULT_TITLE=$(grep -o '"title": [^,]*' "$SCRIPT_DIR/config.json" | cut -d'"' -f4)
    DEFAULT_LANG=$(grep -o '"language": "[^"]*"' "$SCRIPT_DIR/config.json" | cut -d'"' -f4)
    DEFAULT_PORT=$(grep -o '"port": [^,]*' "$SCRIPT_DIR/config.json" | awk '{print $2}')
    DEFAULT_START_WEIGHT=$(grep -o '"startWeight": [^,]*' "$SCRIPT_DIR/config.json" | awk '{print $2}')
    DEFAULT_TARGET_WEIGHT=$(grep -o '"targetWeight": [^,]*' "$SCRIPT_DIR/config.json" | awk '{print $2}')
    DEFAULT_START_DATE=$(grep -o '"startDate": "[^"]*"' "$SCRIPT_DIR/config.json" | cut -d'"' -f4)
    DEFAULT_END_DATE=$(grep -o '"endDate": "[^"]*"' "$SCRIPT_DIR/config.json" | cut -d'"' -f4)
fi

: ${DEFAULT_TITLE:="Weight Tracker"}
: ${DEFAULT_LANG:="en"}
: ${DEFAULT_PORT:=8080}
: ${DEFAULT_START_WEIGHT:=70}
: ${DEFAULT_TARGET_WEIGHT:=60}
: ${DEFAULT_START_DATE:=$(get_today)}
: ${DEFAULT_END_DATE:=$(get_future_date 90)}

# ========== 第一步：选择语言 ==========
echo "Please select your language / 请选择语言:"
echo "  1) English"
echo "  2) 中文"
echo ""
read -p "Choice / 选择 (1/2): " LANG_CHOICE

if [ "$LANG_CHOICE" == "2" ]; then
    LANG="zh"
    read_prompts_zh
else
    LANG="en"
    read_prompts_en
fi

echo ""
echo "$GREETING"
echo "================================"

# ========== 第二步：根据语言显示配置 ==========

if [ "$LANG" == "zh" ]; then
    echo ""
    echo "第 1 步：基本设置"
    echo "-----------------------------------"
    echo "$PROMPT_PORT $AVAILABLE_PORTS"
    
    AVAILABLE_PORTS_ARRAY=($(get_available_ports))
    if [ ${#AVAILABLE_PORTS_ARRAY[@]} -eq 0 ]; then
        AVAILABLE_PORTS_ARRAY=(8000 8080 8888)
    fi
    echo "${AVAILABLE_PORTS_ARRAY[@]}"
    echo ""
    
    echo "$PROMPT_TITLE ($PROMPT_TITLE_HINT)"
    read -p "  $PROMPT_TITLE [$DEFAULT_TITLE]: " TITLE
    
    echo ""
    echo "$PROMPT_PORT_HINT"
    PS3="$SELECT_PORT (1-${#AVAILABLE_PORTS_ARRAY[@]}): "
    select port_choice in "${AVAILABLE_PORTS_ARRAY[@]}" "$SELECT_CUSTOM"; do
        if [ "$port_choice" = "$SELECT_CUSTOM" ]; then
            read -p "$PROMPT_PORT_CUSTOM " CUSTOM_PORT
            SELECTED_PORT=${CUSTOM_PORT:-8080}
            break
        elif [ -n "$port_choice" ]; then
            SELECTED_PORT=$port_choice
            break
        fi
    done
    : ${SELECTED_PORT:=$DEFAULT_PORT}
    
    echo ""
    echo "第 2 步：减肥目标"
    echo "-----------------------------------"
    echo "$PROMPT_START_WEIGHT ($PROMPT_START_WEIGHT_HINT)"
    read -p "  $PROMPT_START_WEIGHT [$DEFAULT_START_WEIGHT]: " START_WEIGHT
    echo "$PROMPT_TARGET_WEIGHT ($PROMPT_TARGET_WEIGHT_HINT)"
    read -p "  $PROMPT_TARGET_WEIGHT [$DEFAULT_TARGET_WEIGHT]: " TARGET_WEIGHT
    
    echo ""
    echo "第 3 步：计划周期"
    echo "-----------------------------------"
    echo "$PROMPT_START_DATE ($PROMPT_START_DATE_HINT)"
    read -p "  $PROMPT_START_DATE [$DEFAULT_START_DATE]: " START_DATE
    echo "$PROMPT_END_DATE ($PROMPT_END_DATE_HINT)"
    read -p "  $PROMPT_END_DATE [$DEFAULT_END_DATE]: " END_DATE
    
    echo ""
    echo "第 4 步：初始体重记录"
    echo "-----------------------------------"
    echo "$PROMPT_INIT_WEIGHT ($PROMPT_INIT_WEIGHT_HINT)"
    read -p "  $PROMPT_INIT_WEIGHT [$DEFAULT_START_WEIGHT]: " INIT_WEIGHT
    echo "$PROMPT_INIT_DATE ($PROMPT_INIT_DATE_HINT)"
    read -p "  $PROMPT_INIT_DATE [$DEFAULT_START_DATE]: " INIT_DATE
    
else
    echo ""
    echo "Step 1: Basic Settings"
    echo "-----------------------------------"
    echo "$PROMPT_PORT $AVAILABLE_PORTS"
    
    AVAILABLE_PORTS_ARRAY=($(get_available_ports))
    if [ ${#AVAILABLE_PORTS_ARRAY[@]} -eq 0 ]; then
        AVAILABLE_PORTS_ARRAY=(8000 8080 8888)
    fi
    echo "${AVAILABLE_PORTS_ARRAY[@]}"
    echo ""
    
    echo "$PROMPT_TITLE ($PROMPT_TITLE_HINT)"
    read -p "  $PROMPT_TITLE [$DEFAULT_TITLE]: " TITLE
    
    echo ""
    echo "$PROMPT_PORT_HINT"
    PS3="$SELECT_PORT (1-${#AVAILABLE_PORTS_ARRAY[@]}): "
    select port_choice in "${AVAILABLE_PORTS_ARRAY[@]}" "$SELECT_CUSTOM"; do
        if [ "$port_choice" = "$SELECT_CUSTOM" ]; then
            read -p "$PROMPT_PORT_CUSTOM " CUSTOM_PORT
            SELECTED_PORT=${CUSTOM_PORT:-8080}
            break
        elif [ -n "$port_choice" ]; then
            SELECTED_PORT=$port_choice
            break
        fi
    done
    : ${SELECTED_PORT:=$DEFAULT_PORT}
    
    echo ""
    echo "Step 2: Weight Loss Goal"
    echo "-----------------------------------"
    echo "$PROMPT_START_WEIGHT ($PROMPT_START_WEIGHT_HINT)"
    read -p "  $PROMPT_START_WEIGHT [$DEFAULT_START_WEIGHT]: " START_WEIGHT
    echo "$PROMPT_TARGET_WEIGHT ($PROMPT_TARGET_WEIGHT_HINT)"
    read -p "  $PROMPT_TARGET_WEIGHT [$DEFAULT_TARGET_WEIGHT]: " TARGET_WEIGHT
    
    echo ""
    echo "Step 3: Plan Period"
    echo "-----------------------------------"
    echo "$PROMPT_START_DATE ($PROMPT_START_DATE_HINT)"
    read -p "  $PROMPT_START_DATE [$DEFAULT_START_DATE]: " START_DATE
    echo "$PROMPT_END_DATE ($PROMPT_END_DATE_HINT)"
    read -p "  $PROMPT_END_DATE [$DEFAULT_END_DATE]: " END_DATE
    
    echo ""
    echo "Step 4: Initial Weight Record"
    echo "-----------------------------------"
    echo "$PROMPT_INIT_WEIGHT ($PROMPT_INIT_WEIGHT_HINT)"
    read -p "  $PROMPT_INIT_WEIGHT [$DEFAULT_START_WEIGHT]: " INIT_WEIGHT
    echo "$PROMPT_INIT_DATE ($PROMPT_INIT_DATE_HINT)"
    read -p "  $PROMPT_INIT_DATE [$DEFAULT_START_DATE]: " INIT_DATE
fi

# ========== 应用默认值 ==========
: ${TITLE:=$DEFAULT_TITLE}
: ${LANG:=$DEFAULT_LANG}
: ${START_WEIGHT:=$DEFAULT_START_WEIGHT}
: ${TARGET_WEIGHT:=$DEFAULT_TARGET_WEIGHT}
: ${START_DATE:=$DEFAULT_START_DATE}
: ${END_DATE:=$DEFAULT_END_DATE}
: ${INIT_WEIGHT:=$START_WEIGHT}
: ${INIT_DATE:=$START_DATE}

# ========== 创建配置文件 ==========

if [ "$LANG" == "zh" ]; then
    START_LABEL=$(format_date "$START_DATE" "%-m月%-d日")
    END_LABEL=$(format_date "$END_DATE" "%-m月%-d日")
else
    START_LABEL=$(format_date "$START_DATE" "%m/%d")
    END_LABEL=$(format_date "$END_DATE" "%m/%d")
fi

cat > "$SCRIPT_DIR/config.json" << EOF
{
  "title": "$TITLE",
  "language": "$LANG",
  "port": $SELECTED_PORT,
  "startWeight": $START_WEIGHT,
  "targetWeight": $TARGET_WEIGHT,
  "startDate": "$START_DATE",
  "endDate": "$END_DATE",
  "startDateLabel": "$START_LABEL",
  "endDateLabel": "$END_LABEL"
}
EOF

cat > "$SCRIPT_DIR/weight_history.json" << EOF
{
  "records": [
    {"date": "$INIT_DATE", "weight": $INIT_WEIGHT}
  ]
}
EOF

# ========== 完成提示 ==========
echo ""
echo "$SETUP_COMPLETE"
echo "$DONE"
echo "$CONFIG: config.json"
echo "$DATA: weight_history.json (${INIT_DATE}: ${INIT_WEIGHT}kg)"
echo "$PORT: $SELECTED_PORT"
echo ""
echo "$TO_START"
echo "   cd $SCRIPT_DIR"
echo "   python3 -m http.server $SELECTED_PORT"
echo ""
echo "$TO_OPEN http://localhost:$SELECTED_PORT/jianfei.html"
echo ""
echo "$PRESS_W"
echo "$DONE"
