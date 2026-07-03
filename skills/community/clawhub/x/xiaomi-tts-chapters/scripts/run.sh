#!/bin/bash

# 有声小说语音合成快速启动脚本
# 通用版本，支持任意章节目录

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 默认配置
DEFAULT_VOICE="mimo_default"
DEFAULT_DELAY=1.0
DEFAULT_MODEL="mimo-v2.5-tts"
DEFAULT_BASE_URL="https://token-plan-cn.xiaomimimo.com/v1"

# 显示帮助
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "必需参数:"
    echo "  -c, --chapters-dir DIR   章节目录路径"
    echo ""
    echo "可选参数:"
    echo "  -h, --help               显示帮助信息"
    echo "  -a, --api-key KEY        设置API密钥（也可通过 MIMO_API_KEY 环境变量设置）"
    echo "  -o, --output-dir DIR     输出目录路径（默认: 当前目录）"
    echo "  -v, --voice VOICE        语音音色（mimo_default, default_zh, default_en）"
    echo "  -t, --style STYLE        语音风格（温柔, 开心, 悲伤等）"
    echo "  -m, --model MODEL        TTS模型（默认: mimo-v2.5-tts）"
    echo "  -b, --base-url URL       API基础URL"
    echo "  -d, --delay SECS         请求间隔秒数（默认: 1.0）"
    echo "  -s, --start N            起始章节索引（从0开始）"
    echo "  -e, --end N              结束章节索引"
    echo ""
    echo "API密钥获取优先级:"
    echo "  1. -a 参数"
    echo "  2. MIMO_API_KEY 环境变量"
    echo "  3. 交互式输入"
    echo ""
    echo "示例:"
    echo "  $0 -c /path/to/chapters                    # 合成所有章节（使用环境变量或交互输入）"
    echo "  $0 -a YOUR_API_KEY -c /path/to/chapters    # 合成所有章节"
    echo "  $0 -c /path/to/chapters -s 0 -e 5         # 只合成前5章"
    echo "  $0 -c /path/to/chapters -v default_zh     # 使用中文女声"
    echo "  $0 -c /path/to/chapters -t \"温柔\"         # 使用温柔风格"
    echo ""
    echo "环境变量:"
    echo "  MIMO_API_KEY             API密钥（可替代 -a 参数）"
}

# 检查虚拟环境
check_venv() {
    local script_dir="$(cd "$(dirname "$0")" && pwd)"
    local venv_dir="$script_dir/venv"
    
    if [ ! -d "$venv_dir" ]; then
        echo -e "${YELLOW}创建虚拟环境...${NC}"
        python3 -m venv "$venv_dir"
        source "$venv_dir/bin/activate"
        pip install -r "$script_dir/requirements.txt"
    else
        source "$venv_dir/bin/activate"
    fi
}

# 解析参数
API_KEY="${MIMO_API_KEY:-}"
CHAPTERS_DIR=""
OUTPUT_DIR="."
VOICE="$DEFAULT_VOICE"
STYLE=""
MODEL="$DEFAULT_MODEL"
BASE_URL="$DEFAULT_BASE_URL"
DELAY="$DEFAULT_DELAY"
START=0
END=-1

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -a|--api-key)
            API_KEY="$2"
            shift 2
            ;;
        -c|--chapters-dir)
            CHAPTERS_DIR="$2"
            shift 2
            ;;
        -o|--output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -v|--voice)
            VOICE="$2"
            shift 2
            ;;
        -t|--style)
            STYLE="$2"
            shift 2
            ;;
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -b|--base-url)
            BASE_URL="$2"
            shift 2
            ;;
        -d|--delay)
            DELAY="$2"
            shift 2
            ;;
        -s|--start)
            START="$2"
            shift 2
            ;;
        -e|--end)
            END="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# 检查API密钥：参数 > 环境变量 > 交互输入
if [ -z "$API_KEY" ]; then
    if [ -n "$MIMO_API_KEY" ]; then
        API_KEY="$MIMO_API_KEY"
    else
        echo -e "${YELLOW}未检测到API密钥${NC}"
        read -p "请输入小米MiMo API密钥: " API_KEY
        if [ -z "$API_KEY" ]; then
            echo -e "${RED}错误: 未提供API密钥${NC}"
            exit 1
        fi
    fi
fi

if [ -z "$CHAPTERS_DIR" ]; then
    echo -e "${RED}错误: 未指定章节目录${NC}"
    echo "使用 -c 或 --chapters-dir 参数指定章节目录路径"
    exit 1
fi

# 检查章节目录是否存在
if [ ! -d "$CHAPTERS_DIR" ]; then
    echo -e "${RED}错误: 章节目录不存在: $CHAPTERS_DIR${NC}"
    exit 1
fi

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 检查虚拟环境
check_venv

# 构建命令
CMD="python3 \"$SCRIPT_DIR/synthesize.py\" --api-key \"$API_KEY\" --chapters-dir \"$CHAPTERS_DIR\" --output-dir \"$OUTPUT_DIR\" --voice \"$VOICE\" --model \"$MODEL\" --base-url \"$BASE_URL\" --delay \"$DELAY\" --start \"$START\" --end \"$END\""

if [ -n "$STYLE" ]; then
    CMD="$CMD --style \"$STYLE\""
fi

# 显示配置
echo -e "${GREEN}=== 有声小说语音合成 ===${NC}"
echo "API密钥: ${API_KEY:0:10}..."
echo "章节目录: $CHAPTERS_DIR"
echo "输出目录: $OUTPUT_DIR"
echo "语音音色: $VOICE"
echo "TTS模型: $MODEL"
echo "API端点: $BASE_URL"
if [ -n "$STYLE" ]; then
    echo "语音风格: $STYLE"
fi
echo "请求间隔: ${DELAY}秒"
if [ $START -gt 0 ] || [ $END -gt 0 ]; then
    echo "章节范围: $START - $END"
else
    echo "章节范围: 全部"
fi
echo ""

# 执行合成
echo -e "${YELLOW}开始合成...${NC}"
eval $CMD

echo -e "${GREEN}完成！${NC}"
