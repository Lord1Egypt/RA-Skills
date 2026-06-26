#!/bin/bash
# 通过飞书发送语音消息（语音气泡格式）
#
# 用法:
#   ./send_voice_feishu.sh input.wav TARGET_OPEN_ID
#
# 必须设置的环境变量：
#   FEISHU_APP_ID      飞书自建应用的 App ID
#   FEISHU_APP_SECRET  飞书自建应用的 App Secret
#
# 可选环境变量：
#   （无，凭证仅通过环境变量传入，不读取本地配置文件）
#
# 示例:
#   export FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
#   export FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#   ./send_voice_feishu.sh output.wav ou_xxxxxxxxxxxxxxxxxxxxxxxx

set -e

WAV_FILE="${1}"
TARGET_USER_ID="${2}"

# --- 参数检查 ---
if [ -z "$WAV_FILE" ] || [ -z "$TARGET_USER_ID" ]; then
    echo "用法: $0 <input.wav> <target_open_id>"
    echo ""
    echo "环境变量:"
    echo "  FEISHU_APP_ID      飞书应用 App ID"
    echo "  FEISHU_APP_SECRET  飞书应用 App Secret"
    exit 1
fi

if [ ! -f "$WAV_FILE" ]; then
    echo "错误: 文件不存在: $WAV_FILE"
    exit 1
fi

# --- 读取飞书凭证（仅从环境变量读取，不读取本地配置文件）---
if [ -z "$FEISHU_APP_ID" ] || [ -z "$FEISHU_APP_SECRET" ]; then
    echo "错误: 请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET"
    echo ""
    echo "示例:"
    echo "  export FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx"
    echo "  export FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    exit 1
fi
APP_ID="$FEISHU_APP_ID"
APP_SECRET="$FEISHU_APP_SECRET"

# --- 转码 ---
OPUS_FILE="${WAV_FILE%.wav}.opus"
echo "1/4 转码 WAV → Opus..."
# 计算音频时长（毫秒），用于后续发送消息时传入 duration 字段
DURATION_MS=$(python3 -c "
import wave, os
try:
    with wave.open('$WAV_FILE') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        print(int(frames / rate * 1000))
except Exception as e:
    print(0)
")
echo "    时长: ${DURATION_MS}ms"

# 用 opusenc 编码（granule position 更准确），如不存在则退回 ffmpeg
if command -v sox &>/dev/null && command -v opusenc &>/dev/null; then
    PCM_TMP="${WAV_FILE%.wav}_tmp48k.wav"
    sox "$WAV_FILE" -r 48000 -c 1 -e signed -b 16 "$PCM_TMP"
    opusenc --bitrate 24 "$PCM_TMP" "$OPUS_FILE" 2>/dev/null
    rm -f "$PCM_TMP"
else
    ffmpeg -i "$WAV_FILE" -ar 24000 -ac 1 -c:a libopus -b:a 24k \
        -application voip -frame_duration 20 \
        "$OPUS_FILE" -y -loglevel quiet
fi
echo "    ✓ $OPUS_FILE"

# --- 获取 Token ---
echo "2/4 获取 access token..."
TOKEN_RESP=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}")
TOKEN=$(echo "$TOKEN_RESP" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tenant_access_token',''))")
if [ -z "$TOKEN" ]; then
    echo "错误: 获取 token 失败: $TOKEN_RESP"
    exit 1
fi
echo "    ✓ token 获取成功"

# --- 上传文件 ---
echo "3/4 上传 opus 文件..."
UPLOAD_RESP=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=opus" \
  -F "file_name=$(basename $OPUS_FILE)" \
  -F "file=@$OPUS_FILE")
FILE_KEY=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('data',{}).get('file_key',''))")
if [ -z "$FILE_KEY" ]; then
    echo "错误: 上传失败: $UPLOAD_RESP"
    exit 1
fi
echo "    ✓ file_key: $FILE_KEY"

# --- 发送语音消息 ---
echo "4/4 发送语音消息到 $TARGET_USER_ID..."
SEND_RESP=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"$TARGET_USER_ID\",
    \"msg_type\": \"audio\",
    \"content\": \"{\\\"file_key\\\":\\\"$FILE_KEY\\\",\\\"duration\\\":${DURATION_MS:-0}}\"
  }")

CODE=$(echo "$SEND_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('code', -1))")
if [ "$CODE" = "0" ]; then
    echo "    ✓ 发送成功！"
else
    echo "    发送结果: $SEND_RESP"
fi

# 清理临时 opus 文件
rm -f "$OPUS_FILE"
echo "完成 ✓"
