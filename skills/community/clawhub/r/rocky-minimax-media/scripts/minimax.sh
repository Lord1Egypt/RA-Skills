#!/bin/bash
# MiniMax API 媒体生成插件 v1.3.0
# 
# 环境变量配置:
#   MINIMAX_OUTPUT_DIR - 输出目录（默认: ~/.openclaw/output）
#
# 用法: ./minimax.sh [test|image|tts|video|music]
#

# ============ 配置 ============
MINIMAX_OUTPUT_DIR="${MINIMAX_OUTPUT_DIR:-$HOME/.openclaw/output}"
BASE_URL="https://api.minimaxi.com"

# 确保输出目录存在
mkdir -p "$MINIMAX_OUTPUT_DIR"

# 颜色
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

log() { echo -e "${GREEN}[✓]${NC} $1"; }
err() { echo -e "${RED}[✗]${NC} $1"; }
info() { echo -e "${YELLOW}[i]${NC} $1"; }

# ============ 从 openclaw.json 读取 MiniMax API Key ============
read_minimax_key() {
  local openclaw_json="$HOME/.openclaw/openclaw.json"
  
  # 尝试从 openclaw.json 读取 minimax apiKey
  if [ -f "$openclaw_json" ]; then
    # 使用 python3 解析 JSON（macOS 自带）
    MINIMAX_API_KEY=$(python3 -c "
import json, sys
try:
    with open('$openclaw_json') as f:
        config = json.load(f)
    # 尝试多种路径
    key = None
    
    # 路径1: models.providers.minimax-portal.apiKey
    try:
        key = config.get('models', {}).get('providers', {}).get('minimax-portal', {}).get('apiKey')
    except: pass
    
    # 路径2: providers.minimax.apiKey
    if not key:
        try:
            key = config.get('providers', {}).get('minimax', {}).get('apiKey')
        except: pass
    
    # 路径3: env 中的 MINIMAX_API_KEY (展开后的)
    if not key:
        try:
            env_vars = config.get('env', {})
            if isinstance(env_vars, dict):
                key = env_vars.get('MINIMAX_API_KEY')
            elif isinstance(env_vars, list):
                for item in env_vars:
                    if isinstance(item, dict) and item.get('key') == 'MINIMAX_API_KEY':
                        key = item.get('value')
                        break
        except: pass
    
    if key:
        print(key)
    else:
        print('')
except Exception as e:
    print('')
" 2>/dev/null)
    
    if [ -n "$MINIMAX_API_KEY" ]; then
      export MINIMAX_API_KEY
      return 0
    fi
  fi
  
  # 回退：从环境变量读取
  if [ -n "$MINIMAX_API_KEY" ]; then
    return 0
  fi
  
  return 1
}

# ============ 检查配置 ============
check_config() {
  # 尝试读取 openclaw.json 中的 key
  if ! read_minimax_key; then
    err "❌ MiniMax API 未配置！"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ⚠️  使用本插件前必须先配置 MiniMax 模型"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📝 配置步骤:"
    echo ""
    echo "1. 确保已在 OpenClaw 中配置 MiniMax 模型"
    echo "   (在 openclaw.json 的 models.providers.minimax-portal)"
    echo ""
    echo "2. 如果是手动配置，添加 API Key:"
    echo "   {"
    echo "     \"models\": {"
    echo "       \"providers\": {"
    echo "         \"minimax-portal\": {"
    echo "           \"apiKey\": \"你的MiniMax API Key\""
    echo "         }"
    echo "       }"
    echo "     }"
    echo "   }"
    echo ""
    echo "3. 或设置环境变量:"
    echo "   export MINIMAX_API_KEY=你的API_Key"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 1
  fi
}

# ============ 测试所有功能 ============
test_all() {
  check_config
  echo "=========================================="
  echo "  MiniMax API 媒体生成测试"
  echo "=========================================="
  echo "输出目录: $MINIMAX_OUTPUT_DIR"
  echo ""
  
  echo "1. 图片生成..."
  resp=$(curl -s --max-time 15 -X POST "$BASE_URL/v1/image_generation" \
    -H "Authorization: Bearer $MINIMAX_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"image-01","prompt":"test","extra_params":{"image_size":"1:1"}}')
  code=$(echo "$resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('base_resp',{}).get('status_code',999))" 2>/dev/null)
  [ "$code" = "0" ] && log "图片生成 ✅" || err "图片生成 ❌ ($code)"
  
  echo "2. TTS语音..."
  resp=$(curl -s --max-time 10 -X POST "$BASE_URL/v1/t2a_v2" \
    -H "Authorization: Bearer $MINIMAX_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"speech-2.8-hd","text":"test","stream":false,"voice_setting":{"voice_id":"male-qn-qingse"}}')
  code=$(echo "$resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('base_resp',{}).get('status_code',999))" 2>/dev/null)
  [ "$code" = "0" ] && log "TTS语音 ✅" || err "TTS语音 ❌ ($code)"
  
  echo "3. 视频生成 (MiniMax-Hailuo-2.3)..."
  resp=$(curl -s --max-time 10 -X POST "$BASE_URL/v1/video_generation" \
    -H "Authorization: Bearer $MINIMAX_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"MiniMax-Hailuo-2.3","prompt":"test"}')
  code=$(echo "$resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('base_resp',{}).get('status_code',999))" 2>/dev/null)
  [ "$code" = "0" ] && log "视频生成 ✅" || err "视频生成 ❌ ($code)"
  
  echo "4. 视频生成 (MiniMax-Hailuo-2.3-Fast)..."
  resp=$(curl -s --max-time 10 -X POST "$BASE_URL/v1/video_generation" \
    -H "Authorization: Bearer $MINIMAX_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"MiniMax-Hailuo-2.3-Fast","prompt":"test"}')
  code=$(echo "$resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('base_resp',{}).get('status_code',999))" 2>/dev/null)
  [ "$code" = "0" ] && log "视频生成-Fast ✅" || err "视频生成-Fast ❌ ($code)"
  
  echo "5. 音乐生成 (music-2.6)..."
  resp=$(curl -s --max-time 10 -X POST "$BASE_URL/v1/music_generation" \
    -H "Authorization: Bearer $MINIMAX_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"music-2.6","prompt":"test","lyrics":"test"}')
  code=$(echo "$resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('base_resp',{}).get('status_code',999))" 2>/dev/null)
  [ "$code" = "0" ] && log "音乐生成 ✅" || err "音乐生成 ❌ ($code)"
  
  echo ""
  echo "测试完成！"
}

# ============ 生成图片 ============
do_image() {
  check_config
  info "图片生成..."
  read -p "请输入图片描述 [默认: 科技感大脑]: " PROMPT
  PROMPT=${PROMPT:-科技感大脑}
  
  resp=$(curl -s --max-time 30 -X POST "$BASE_URL/v1/image_generation" \
    -H "Authorization: Bearer $MINIMAX_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"image-01\",\"prompt\":\"$PROMPT\",\"extra_params\":{\"image_size\":\"16:9\"}}")
  url=$(echo "$resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('image_urls',[''])[0])" 2>/dev/null)
  if [ -n "$url" ]; then
    filename="minimax-image-$(date +%Y%m%d-%H%M%S).jpg"
    curl -s -L "$url" -o "$MINIMAX_OUTPUT_DIR/$filename"
    log "图片已保存: $MINIMAX_OUTPUT_DIR/$filename"
  else
    err "生成失败: $(echo $resp | head -c 100)"
  fi
}

# ============ TTS语音 ============
do_tts() {
  check_config
  info "TTS语音合成..."
  read -p "请输入要朗读的文本: " TEXT
  if [ -z "$TEXT" ]; then
    err "文本不能为空"
    exit 1
  fi
  
  echo "选择音色:"
  echo "  1) male-qn-qingse   - 男声-青年-青涩"
  echo "  2) female-tianmei   - 女声-甜妹"
  echo "  3) female-yujie     - 女声-御姐"
  read -p "请输入选项 [1-3，默认1]: " voice_choice
  voice_choice=${voice_choice:-1}
  case $voice_choice in
    2) VOICE_ID="female-tianmei" ;;
    3) VOICE_ID="female-yujie" ;;
    *) VOICE_ID="male-qn-qingse" ;;
  esac
  
  resp=$(curl -s --max-time 15 -X POST "$BASE_URL/v1/t2a_v2" \
    -H "Authorization: Bearer $MINIMAX_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"speech-2.8-hd\",\"text\":\"$TEXT\",\"stream\":false,\"voice_setting\":{\"voice_id\":\"$VOICE_ID\"}}")
  
  filename="minimax-tts-$(date +%Y%m%d-%H%M%S).mp3"
  echo "$resp" | python3 -c "
import sys,json
content = sys.stdin.read()
try:
    idx = content.find('{')
    if idx >= 0:
        d = json.loads(content[idx:])
        audio_hex = d.get('data',{}).get('audio','')
        if audio_hex:
            audio = bytes.fromhex(audio_hex)
            with open('$MINIMAX_OUTPUT_DIR/$filename','wb') as f:
                f.write(audio)
            print('已保存: $MINIMAX_OUTPUT_DIR/$filename')
        else:
            print('失败:', d.get('base_resp',{}))
except Exception as e:
    print('解析失败:', e)
"
}

# ============ 视频生成 ============
do_video() {
  check_config
  echo "🎬 视频生成"
  echo ""
  echo "请选择视频模型："
  echo "  1) MiniMax-Hailuo-2.3        - 文生视频，肢体动作/物理表现全面升级"
  echo "  2) MiniMax-Hailuo-2.3-Fast  - 图生视频，生成速度更快"
  echo ""
  read -p "请输入选项 [1/2，默认1]: " choice
  choice=${choice:-1}
  
  if [ "$choice" = "2" ]; then
    MODEL="MiniMax-Hailuo-2.3-Fast"
  else
    MODEL="MiniMax-Hailuo-2.3"
  fi
  info "已选择: $MODEL"
  echo ""
  
  read -p "请输入视频描述 [默认: 神经元活动动画]: " PROMPT
  PROMPT=${PROMPT:-神经元活动动画}
  
  info "正在创建视频任务..."
  resp=$(curl -s --max-time 10 -X POST "$BASE_URL/v1/video_generation" \
    -H "Authorization: Bearer $MINIMAX_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"$MODEL\",\"prompt\":\"$PROMPT\"}")
  
  code=$(echo "$resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('base_resp',{}).get('status_code',999))" 2>/dev/null)
  if [ "$code" != "0" ]; then
    err "创建失败: $(echo $resp | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("base_resp",{}).get("status_msg",d))' 2>/dev/null)"
    exit 1
  fi
  
  task_id=$(echo "$resp" | python3 -c "import sys,json; print(json.load(sys.stdin).get('task_id',''))" 2>/dev/null)
  log "task_id: $task_id"
  info "等待视频生成（约60秒）..."
  for i in {1..12}; do
    sleep 5
    status=$(curl -s "$BASE_URL/v1/query/video_generation?task_id=$task_id" \
      -H "Authorization: Bearer $MINIMAX_API_KEY" \
      | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))" 2>/dev/null)
    echo -n "."
    [ "$status" = "Success" ] && break
  done
  echo ""
  if [ "$status" = "Success" ]; then
    file_id=$(curl -s "$BASE_URL/v1/query/video_generation?task_id=$task_id" \
      -H "Authorization: Bearer $MINIMAX_API_KEY" \
      | python3 -c "import sys,json; print(json.load(sys.stdin).get('file_id',''))" 2>/dev/null)
    url=$(curl -s "$BASE_URL/v1/files/retrieve?file_id=$file_id" \
      -H "Authorization: Bearer $MINIMAX_API_KEY" \
      | python3 -c "import sys,json; print(json.load(sys.stdin).get('file',{}).get('download_url',''))" 2>/dev/null)
    filename="minimax-video-$(date +%Y%m%d-%H%M%S).mp4"
    curl -s -L "$url" -o "$MINIMAX_OUTPUT_DIR/$filename"
    log "视频已保存: $MINIMAX_OUTPUT_DIR/$filename"
  else
    err "视频生成失败或超时"
  fi
}

# ============ 音乐生成 ============
do_music() {
  check_config
  echo "🎵 音乐生成"
  echo ""
  echo "请选择音乐模型："
  echo "  1) music-2.6  - 最新版本，音质更好"
  echo "  2) music-2.5  - 经典版本"
  echo ""
  read -p "请输入选项 [1/2，默认1]: " choice
  choice=${choice:-1}
  
  if [ "$choice" = "2" ]; then
    MUSIC_MODEL="music-2.5"
  else
    MUSIC_MODEL="music-2.6"
  fi
  info "已选择: $MUSIC_MODEL"
  echo ""
  
  read -p "请输入音乐描述 [默认: 欢快轻松的背景音乐]: " PROMPT
  PROMPT=${PROMPT:-欢快轻松的背景音乐}
  
  read -p "请输入歌词（可选）: " LYRICS
  LYRICS=${LYRICS:-}
  
  info "正在生成音乐（可能需要30-120秒）..."
  if [ -n "$LYRICS" ]; then
    resp=$(curl -s --max-time 120 -X POST "$BASE_URL/v1/music_generation" \
      -H "Authorization: Bearer $MINIMAX_API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"model\":\"$MUSIC_MODEL\",\"prompt\":\"$PROMPT\",\"lyrics\":\"$LYRICS\"}")
  else
    resp=$(curl -s --max-time 120 -X POST "$BASE_URL/v1/music_generation" \
      -H "Authorization: Bearer $MINIMAX_API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"model\":\"$MUSIC_MODEL\",\"prompt\":\"$PROMPT\"}")
  fi
  
  filename="minimax-music-$(date +%Y%m%d-%H%M%S).mp3"
  echo "$resp" | python3 -c "
import sys,json
content = sys.stdin.read()
try:
    idx = content.find('{')
    if idx >= 0:
        d = json.loads(content[idx:])
        audio_hex = d.get('data',{}).get('audio','')
        if audio_hex:
            audio = bytes.fromhex(audio_hex)
            with open('$MINIMAX_OUTPUT_DIR/$filename','wb') as f:
                f.write(audio)
            print('已保存: $MINIMAX_OUTPUT_DIR/$filename')
        else:
            print('失败:', d.get('base_resp',{}))
except Exception as e:
    print('解析失败:', e)
"
}

# ============ 主入口 ============
CMD=$1

case "$CMD" in
  test)   test_all ;;
  image)  do_image ;;
  tts)    do_tts ;;
  video)  do_video ;;
  music)  do_music ;;
  *)
    echo "MiniMax API 媒体生成工具 v1.3.0"
    echo ""
    echo "用法: $0 <命令>"
    echo ""
    echo "命令:"
    echo "  test   - 测试所有API"
    echo "  image  - 生成图片（交互式）"
    echo "  tts    - TTS语音合成（交互式）"
    echo "  video  - 视频生成（交互式选择模型）"
    echo "  music  - 音乐生成（交互式选择模型）"
    echo ""
    echo "环境变量:"
    echo "  MINIMAX_OUTPUT_DIR - 输出目录（默认: ~/.openclaw/output）"
    echo ""
    echo "前置要求:"
    echo "  - 必须在 OpenClaw 中配置 MiniMax 模型"
    echo "  - API Key 从 ~/.openclaw/openclaw.json 自动读取"
    echo ""
    echo "示例:"
    echo "  MINIMAX_OUTPUT_DIR=~/output $0 image"
    ;;
esac
