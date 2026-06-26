#!/bin/bash
# 千问 TTS 语音生成（仅生成本地音频文件，不发送飞书）
# 用法: ./speak.sh "要说话的文本" [音色名]
# 默认音色: Nofish
# 注意: 此脚本只需要 DASHSCOPE_API_KEY，不需要飞书凭证

TEXT="$1"
VOICE="${2:-Nofish}"  # 默认用 Nofish 音色
LANG="${3:-Chinese}"

if [ -z "$TEXT" ]; then
    echo "用法: $0 \"文本\" [音色] [语言]"
    exit 1
fi

API_KEY="${DASHSCOPE_API_KEY}"
if [ -z "$API_KEY" ]; then
    echo "错误: DASHSCOPE_API_KEY 未设置"
    exit 1
fi

TMP_WAV="/tmp/qwen_tts_$$.wav"
TMP_OGG="/tmp/qwen_tts_$$.ogg"

# 调用千问 API
RESPONSE=$(curl -s -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
    -H "Authorization: Bearer $API_KEY" \
    -H 'Content-Type: application/json' \
    -d "$(jq -n --arg text "$TEXT" --arg voice "$VOICE" --arg lang "$LANG" '{
        model: "qwen3-tts-flash",
        input: {
            text: $text,
            voice: $voice,
            language_type: $lang
        }
    }')")

# 解析音频 URL
AUDIO_URL=$(echo "$RESPONSE" | jq -r '.data.audio.url // .audio.url // empty')

if [ -z "$AUDIO_URL" ] || [ "$AUDIO_URL" == "null" ]; then
    echo "错误: 无法获取音频 URL"
    echo "响应: $RESPONSE"
    exit 1
fi

# 下载音频
curl -s -o "$TMP_WAV" "$AUDIO_URL"

# 转换为飞书支持的 ogg 格式
ffmpeg -i "$TMP_WAV" -c:a libopus -b:a 64k -ar 48000 "$TMP_OGG" -y 2>/dev/null

# 清理
rm -f "$TMP_WAV"

echo "$TMP_OGG"