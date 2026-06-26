#!/bin/bash
# voice2feishu 主入口
# 用法: voice2feishu <模式> <文字> <接收者> [选项]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 显示帮助
show_help() {
  cat << EOF
Voice2Feishu - 文字转语音发送到飞书

用法:
  voice2feishu <模式> <文字内容> <接收者ID> [选项]

模式:
  api            使用第三方 TTS API（智谱/OpenAI）
  local          使用本地 ChatTTS
  start-chattts  启动 ChatTTS 服务
  stop-chattts   停止 ChatTTS 服务

选项:
  --voice <名称>   指定 API 音色（默认: alloy）
  --seed <数字>    指定本地音色种子（默认: 500）
  --chat           接收者是群聊（使用 chat_id 类型）
  -h, --help       显示帮助

示例:
  voice2feishu api "你好" ou_xxx
  voice2feishu local "你好" ou_xxx --seed 100
  voice2feishu api "大家好" oc_xxx --chat

环境变量:
  FEISHU_APP_ID       飞书应用 ID（必需）
  FEISHU_APP_SECRET   飞书应用密钥（必需）
  TTS_API_KEY         TTS API 密钥（API 模式必需）
  TTS_API_URL         TTS API 地址
  CHATTTS_URL         ChatTTS 服务地址（默认: http://localhost:8080）
EOF
}

# 参数检查
if [ $# -lt 1 ]; then
  show_help
  exit 1
fi

MODE="$1"
shift

case "$MODE" in
  -h|--help)
    show_help
    exit 0
    ;;
  api)
    bash "$SCRIPT_DIR/api-tts.sh" "$@"
    ;;
  local)
    bash "$SCRIPT_DIR/local-tts.sh" "$@"
    ;;
  start-chattts)
    bash "$SCRIPT_DIR/chattts-server.sh" start
    ;;
  stop-chattts)
    bash "$SCRIPT_DIR/chattts-server.sh" stop
    ;;
  *)
    echo "❌ 未知模式: $MODE"
    echo "支持的模式: api, local, start-chattts, stop-chattts"
    exit 1
    ;;
esac
