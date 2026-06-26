#!/bin/bash
# Video Pro - 单视频生成脚本
# 免费版限制：每日3次，最大30秒，720p分辨率

set -e

# 配置
PROJECT_DIR="$HOME/openclaw-video-pro"
OUTPUT_DIR="$PROJECT_DIR/output"
LOG_DIR="$PROJECT_DIR/logs"
CONFIG_FILE="$HOME/.video-pro/config.json"

# 创建目录
mkdir -p "$OUTPUT_DIR" "$LOG_DIR" "$(dirname "$CONFIG_FILE")"

# 检查项目是否存在
if [ ! -d "$PROJECT_DIR" ]; then
    echo "错误: 视频生成项目未安装"
    echo "请先运行: git clone https://github.com/ZhenRobotics/openclaw-video.git $PROJECT_DIR"
    echo "然后运行: cd $PROJECT_DIR && npm install"
    exit 1
fi

# 检查API密钥
if [ -z "$OPENAI_API_KEY" ]; then
    echo "错误: OPENAI_API_KEY 环境变量未设置"
    echo "请设置: export OPENAI_API_KEY='你的OpenAI API密钥'"
    exit 1
fi

# 解析参数
SCRIPT=""
TEMPLATE="basic"
VOICE="alloy"
SPEED="1.0"
OUTPUT_NAME="generated_$(date +%Y%m%d_%H%M%S).mp4"

while [[ $# -gt 0 ]]; do
    case $1 in
        --template)
            TEMPLATE="$2"
            shift 2
            ;;
        --voice)
            VOICE="$2"
            shift 2
            ;;
        --speed)
            SPEED="$2"
            shift 2
            ;;
        --output)
            OUTPUT_NAME="$2"
            shift 2
            ;;
        *)
            SCRIPT="$1"
            shift
            ;;
    esac
done

# 检查脚本内容
if [ -z "$SCRIPT" ]; then
    echo "用法: $0 '视频脚本内容' [选项]"
    echo "选项:"
    echo "  --template TEMPLATE    模板名称 (默认: basic)"
    echo "  --voice VOICE          语音选择 (默认: alloy)"
    echo "  --speed SPEED          语速 (默认: 1.0)"
    echo "  --output FILENAME      输出文件名"
    echo ""
    echo "免费版限制:"
    echo "  - 每日最多3次生成"
    echo "  - 视频最长30秒"
    echo "  - 720p分辨率"
    echo "  - 基础模板和语音"
    echo ""
    echo "升级到高级版解锁更多功能:"
    echo "  https://clawhub.com/@cza999/video-pro"
    exit 1
fi

# 检查免费版限制
check_free_limit() {
    local TODAY=$(date +%Y%m%d)
    local COUNT_FILE="$CONFIG_FILE"
    local TODAY_COUNT=0
    
    if [ -f "$COUNT_FILE" ]; then
        TODAY_COUNT=$(jq -r ".usage.$TODAY // 0" "$COUNT_FILE" 2>/dev/null || echo 0)
    fi
    
    if [ "$TODAY_COUNT" -ge 3 ]; then
        echo "免费版限制: 今日已使用3次生成机会"
        echo "请升级到高级版或明天再试"
        echo "升级链接: https://clawhub.com/@cza999/video-pro"
        exit 1
    fi
    
    # 更新使用计数
    mkdir -p "$(dirname "$COUNT_FILE")"
    if [ -f "$COUNT_FILE" ]; then
        jq ".usage.$TODAY = ($TODAY_COUNT + 1)" "$COUNT_FILE" > "${COUNT_FILE}.tmp" && mv "${COUNT_FILE}.tmp" "$COUNT_FILE"
    else
        echo "{\"usage\": {\"$TODAY\": 1}}" > "$COUNT_FILE"
    fi
}

# 检查脚本长度
check_script_length() {
    local word_count=$(echo "$SCRIPT" | wc -w)
    if [ "$word_count" -gt 100 ]; then
        echo "警告: 脚本较长，可能超过30秒限制"
        echo "免费版建议控制在100词以内"
    fi
}

# 执行生成
generate_video() {
    echo "开始生成视频..."
    echo "脚本: ${SCRIPT:0:50}..."
    echo "模板: $TEMPLATE"
    echo "语音: $VOICE"
    echo "语速: $SPEED"
    
    cd "$PROJECT_DIR"
    
    # 记录开始时间
    local start_time=$(date +%s)
    
    # 调用视频生成脚本
    if [ -f "./generate-for-openclaw.sh" ]; then
        ./generate-for-openclaw.sh "$SCRIPT" --voice "$VOICE" --speed "$SPEED"
    elif [ -f "./agents/video-cli.sh" ]; then
        ./agents/video-cli.sh generate "$SCRIPT" --voice "$VOICE" --speed "$SPEED"
    else
        echo "错误: 未找到视频生成脚本"
        exit 1
    fi
    
    # 记录结束时间
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    # 检查输出文件
    local output_file=""
    if [ -f "./out/generated.mp4" ]; then
        output_file="./out/generated.mp4"
    elif [ -f "./output/generated.mp4" ]; then
        output_file="./output/generated.mp4"
    else
        # 查找最新的mp4文件
        output_file=$(find . -name "*.mp4" -type f -newer /tmp -printf "%T@ %p\n" 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)
    fi
    
    if [ -n "$output_file" ] && [ -f "$output_file" ]; then
        # 复制到输出目录
        cp "$output_file" "$OUTPUT_DIR/$OUTPUT_NAME"
        
        # 获取视频信息
        local video_info=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of csv=p=0 "$OUTPUT_DIR/$OUTPUT_NAME" 2>/dev/null || echo "未知")
        
        echo ""
        echo "✅ 视频生成成功!"
        echo "📁 文件: $OUTPUT_DIR/$OUTPUT_NAME"
        echo "⏱️  生成时间: ${duration}秒"
        echo "📊 视频信息: $video_info"
        echo ""
        echo "免费版剩余次数: $((2 - TODAY_COUNT))/3"
        echo ""
        echo "💡 升级到高级版享受更多功能:"
        echo "   - 批量生成"
        echo "   - 高级模板"
        echo "   - 自定义语音"
        echo "   - 优先处理"
        echo "   👉 https://clawhub.com/@cza999/video-pro"
    else
        echo "错误: 未找到生成的视频文件"
        exit 1
    fi
}

# 主流程
check_free_limit
check_script_length
generate_video

# 记录日志
echo "$(date '+%Y-%m-%d %H:%M:%S') | $SCRIPT | $TEMPLATE | $VOICE | $SPEED | $OUTPUT_NAME" >> "$LOG_DIR/generation.log"