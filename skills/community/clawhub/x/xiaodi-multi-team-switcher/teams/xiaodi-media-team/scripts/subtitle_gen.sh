#!/bin/bash
# 字幕生成脚本
# 用法: subtitle_gen.sh <input_video> [--output <output>] [--language <zh|en>]

set -e

# 默认参数
INPUT=""
OUTPUT=""
LANGUAGE="zh"
WHISPER_MODEL="medium"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --output|-o)
            OUTPUT="$2"
            shift 2
            ;;
        --language|-l)
            LANGUAGE="$2"
            shift 2
            ;;
        --model|-m)
            WHISPER_MODEL="$2"
            shift 2
            ;;
        -*)
            echo "未知参数: $1"
            exit 1
            ;;
        *)
            if [[ -z "$INPUT" ]]; then
                INPUT="$1"
            fi
            shift
            ;;
    esac
done

# 检查输入
if [[ -z "$INPUT" ]]; then
    echo "❌ 错误: 请指定输入视频文件"
    echo "用法: $0 <input_video> [--output <output>] [--language <zh|en>]"
    exit 1
fi

if [[ ! -f "$INPUT" ]]; then
    echo "❌ 错误: 文件不存在: $INPUT"
    exit 1
fi

# 检查 whisper 是否安装
if ! command -v whisper &> /dev/null; then
    echo "⚠️ Whisper 未安装，尝试使用 ffmpeg 内置功能"
    echo "提示: 安装 whisper: pip install openai-whisper"
    
    # 先提取音频
    BASENAME=$(basename "$INPUT" | sed 's/\.[^.]*$//')
    TEMP_AUDIO="/tmp/xiaodi-media/${BASENAME}_temp.wav"
    mkdir -p "$(dirname "$TEMP_AUDIO")"
    
    ffmpeg -y -i "$INPUT" -vn -c:a pcm_s16le -ar 16000 -ac 1 "$TEMP_AUDIO" 2>&1 | tail -3
    
    echo ""
    echo "⚠️ Whisper 未安装，无法生成字幕"
    echo "请安装: pip install openai-whisper"
    echo "临时音频文件: $TEMP_AUDIO"
    exit 1
fi

# 设置输出文件
if [[ -z "$OUTPUT" ]]; then
    BASENAME=$(basename "$INPUT" | sed 's/\.[^.]*$//')
    OUTPUT="/tmp/xiaodi-media/${BASENAME}.srt"
fi

# 创建输出目录
mkdir -p "$(dirname "$OUTPUT")"

echo "📝 字幕生成开始"
echo "   输入: $INPUT"
echo "   输出: $OUTPUT"
echo "   语言: $LANGUAGE"
echo "   模型: $WHISPER_MODEL"

# 使用 whisper 生成字幕
whisper "$INPUT" \
    --model $WHISPER_MODEL \
    --language $LANGUAGE \
    --output_format srt \
    --output_dir "$(dirname "$OUTPUT")" \
    2>&1 | tail -10

# 检查输出
EXPECTED_OUTPUT="${INPUT%.*}.srt"
if [[ -f "$EXPECTED_OUTPUT" ]]; then
    mv "$EXPECTED_OUTPUT" "$OUTPUT"
fi

if [[ -f "$OUTPUT" ]]; then
    LINES=$(wc -l < "$OUTPUT")
    echo ""
    echo "✅ 字幕生成完成!"
    echo "   字幕行数: $LINES"
    echo "   输出文件: $OUTPUT"
else
    echo "❌ 字幕生成失败"
    exit 1
fi