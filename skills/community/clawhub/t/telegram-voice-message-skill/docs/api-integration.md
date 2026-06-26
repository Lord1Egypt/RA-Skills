# 🔌 API集成指南

Telegram语音消息技能支持多种API服务集成，包括TTS服务、消息服务和其他辅助服务。

## 📋 支持的API服务

### 1. TTS服务
- ✅ **阿里云TTS** (推荐，中文效果好)
- ✅ **OpenAI TTS** (英语效果好)
- ✅ **Google Cloud TTS** (多语言支持)
- ✅ **本地TTS引擎** (eSpeak, Festival等)

### 2. 消息服务
- ✅ **Telegram Bot API** (主要消息通道)
- ✅ **Slack Webhook** (企业通知)
- ✅ **Discord Webhook** (社区通知)
- ✅ **企业微信机器人** (国内企业)

### 3. 辅助服务
- ✅ **监控告警** (错误通知)
- ✅ **日志服务** (集中日志)
- ✅ **配置管理** (动态配置)
- ✅ **缓存服务** (性能优化)

## 🔧 TTS API集成

### 阿里云TTS集成

#### 认证方式
```bash
# 环境变量配置
export ALIYUN_ACCESS_KEY_ID="your_access_key_id"
export ALIYUN_ACCESS_KEY_SECRET="your_access_key_secret"
export ALIYUN_TTS_APPKEY="your_tts_appkey"

# 或使用配置文件
cat > ~/.aliyun/config.json << EOF
{
  "access_key_id": "$ALIYUN_ACCESS_KEY_ID",
  "access_key_secret": "$ALIYUN_ACCESS_KEY_SECRET",
  "tts_appkey": "$ALIYUN_TTS_APPKEY"
}
EOF
```

#### API调用示例
```bash
# 调用阿里云TTS
call_aliyun_tts() {
  local text="$1"
  local output_file="$2"
  
  # 构建请求
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local signature=$(generate_signature "$text" "$timestamp")
  
  # 发送请求
  curl -X POST "https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/tts" \
    -H "Content-Type: application/json" \
    -H "Authorization: $signature" \
    -d "{
      \"appkey\": \"$ALIYUN_TTS_APPKEY\",
      \"text\": \"$text\",
      \"format\": \"wav\",
      \"sample_rate\": 16000,
      \"voice\": \"xiaoyun\",
      \"volume\": 50,
      \"speech_rate\": 0,
      \"pitch_rate\": 0
    }" \
    -o "$output_file"
  
  # 验证响应
  if [ -f "$output_file" ] && [ $(stat -c%s "$output_file") -gt 1000 ]; then
    echo "✅ TTS生成成功: $output_file"
    return 0
  else
    echo "❌ TTS生成失败"
    return 1
  fi
}
```

#### 错误处理
```bash
handle_aliyun_error() {
  local error_code="$1"
  local error_message="$2"
  
  case "$error_code" in
    "400")
      echo "❌ 请求参数错误: $error_message"
      # 检查文本长度、格式等
      ;;
    "401")
      echo "❌ 认证失败: 检查Access Key"
      # 重新获取认证信息
      ;;
    "403")
      echo "❌ 权限不足: 检查API权限"
      # 申请相应权限
      ;;
    "429")
      echo "⚠️ 请求过于频繁: 等待后重试"
      # 实现指数退避
      ;;
    "500")
      echo "❌ 服务器内部错误: 联系技术支持"
      # 记录详细错误信息
      ;;
    *)
      echo "❌ 未知错误 ($error_code): $error_message"
      ;;
  esac
}
```

### OpenAI TTS集成

#### 认证配置
```bash
# 环境变量
export OPENAI_API_KEY="sk-..."
export OPENAI_TTS_MODEL="tts-1"  # tts-1 或 tts-1-hd
export OPENAI_TTS_VOICE="alloy"  # alloy, echo, fable, onyx, nova, shimmer

# 模型选择指南
# tts-1: 标准质量，速度快，成本低
# tts-1-hd: 高质量，速度慢，成本高
```

#### API调用
```bash
call_openai_tts() {
  local text="$1"
  local output_file="$2"
  
  # URL编码文本（处理特殊字符）
  local encoded_text=$(printf "%s" "$text" | jq -sRr @uri)
  
  # 调用OpenAI TTS API
  curl -X POST "https://api.openai.com/v1/audio/speech" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"$OPENAI_TTS_MODEL\",
      \"input\": \"$text\",
      \"voice\": \"$OPENAI_TTS_VOICE\",
      \"response_format\": \"mp3\",
      \"speed\": 1.0
    }" \
    -o "$output_file"
  
  # 验证和转换格式
  if [ -f "$output_file" ]; then
    # OpenAI返回MP3，需要转换为OGG
    ffmpeg -i "$output_file" -c:a libopus -b:a 64k "${output_file%.*}.ogg"
    
    if [ $? -eq 0 ]; then
      echo "✅ OpenAI TTS生成成功"
      return 0
    fi
  fi
  
  echo "❌ OpenAI TTS生成失败"
  return 1
}
```

#### 成本控制
```bash
# 成本监控
monitor_openai_cost() {
  local text="$1"
  local chars=${#text}
  
  # 计算成本（按字符数）
  if [ "$OPENAI_TTS_MODEL" = "tts-1" ]; then
    local cost=$(echo "scale=6; $chars * 0.015 / 1000" | bc)
  else  # tts-1-hd
    local cost=$(echo "scale=6; $chars * 0.030 / 1000" | bc)
  fi
  
  echo "ℹ️ 文本长度: $chars 字符"
  echo "💰 预估成本: \$$cost"
  
  # 如果成本过高，发出警告
  local warning_threshold=0.10  # 10美分
  if (( $(echo "$cost > $warning_threshold" | bc -l) )); then
    echo "⚠️ 成本警告: 单次请求超过\$$warning_threshold"
  fi
}
```

### Google Cloud TTS集成

#### 服务账号配置
```bash
# 设置服务账号密钥
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"

# 或使用环境变量
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_TTS_LOCATION="global"  # 或具体区域
```

#### API调用
```bash
call_google_tts() {
  local text="$1"
  local output_file="$2"
  local language="${3:-"zh-CN"}"
  local voice="${4:-"zh-CN-Standard-A"}"
  
  # 构建请求
  local request_json=$(cat << EOF
{
  "input": {
    "text": "$text"
  },
  "voice": {
    "languageCode": "$language",
    "name": "$voice",
    "ssmlGender": "FEMALE"
  },
  "audioConfig": {
    "audioEncoding": "MP3",
    "speakingRate": 1.0,
    "pitch": 0.0,
    "volumeGainDb": 0.0
  }
}
EOF
)
  
  # 调用Google Cloud TTS
  curl -X POST \
    "https://texttospeech.googleapis.com/v1/text:synthesize" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d "$request_json" \
    | jq -r '.audioContent' \
    | base64 --decode \
    > "${output_file}.mp3"
  
  # 转换为OGG格式
  if [ -f "${output_file}.mp3" ]; then
    ffmpeg -i "${output_file}.mp3" -c:a libopus "${output_file}.ogg"
    
    if [ $? -eq 0 ]; then
      echo "✅ Google Cloud TTS生成成功"
      rm "${output_file}.mp3"
      return 0
    fi
  fi
  
  echo "❌ Google Cloud TTS生成失败"
  return 1
}
```

#### 语音选择
```bash
# 获取可用语音列表
list_google_voices() {
  local language_code="${1:-"zh-CN"}"
  
  curl -X GET \
    "https://texttospeech.googleapis.com/v1/voices?languageCode=$language_code" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    | jq -r '.voices[] | "\(.name): \(.ssmlGender) - \(.languageCodes[0])"'
}

# 示例输出
# zh-CN-Standard-A: FEMALE - zh-CN
# zh-CN-Standard-B: MALE - zh-CN
# zh-CN-Standard-C: FEMALE - zh-CN
# zh-CN-Standard-D: MALE - zh-CN
# zh-CN-Wavenet-A: FEMALE - zh-CN
# zh-CN-Wavenet-B: MALE - zh-CN
```

## 🤖 Telegram Bot API集成

### 基础配置
```bash
# 必需配置
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
export TELEGRAM_CHAT_ID="-1001234567890"  # 群组ID或用户ID

# 可选配置
export TELEGRAM_API_TIMEOUT=30  # API超时时间（秒）
export TELEGRAM_MAX_RETRIES=3   # 最大重试次数
export TELEGRAM_RETRY_DELAY=2   # 重试延迟（秒）
```

### 发送语音消息
```bash
send_telegram_voice() {
  local audio_file="$1"
  local caption="${2:-""}"  # 语音消息不支持caption，但保留参数
  
  # 验证文件
  if [ ! -f "$audio_file" ]; then
    echo "❌ 音频文件不存在: $audio_file"
    return 1
  fi
  
  # 验证格式
  if ! file "$audio_file" | grep -q "OGG.*Opus"; then
    echo "❌ 文件格式错误: 必须是OGG Opus格式"
    return 1
  fi
  
  # 验证大小（Telegram限制50MB）
  local file_size=$(stat -c%s "$audio_file")
  if [ $file_size -gt 52428800 ]; then  # 50MB
    echo "❌ 文件太大: ${file_size}字节（最大50MB）"
    return 1
  fi
  
  # 发送请求
  local response=$(curl -s \
    -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendVoice" \
    -F chat_id="$TELEGRAM_CHAT_ID" \
    -F voice=@"$audio_file" \
    -F disable_notification="false" \
    -F protect_content="false" \
    -w "%{http_code}" \
    -o /tmp/telegram_response.json)
  
  # 处理响应
  if [ "$response" = "200" ]; then
    echo "✅ 语音消息发送成功"
    return 0
  else
    local error_message=$(jq -r '.description' /tmp/telegram_response.json 2>/dev/null || echo "未知错误")
    echo "❌ 发送失败 ($response): $error_message"
    return 1
  fi
}
```

### 错误处理
```bash
handle_telegram_error() {
  local error_code="$1"
  local error_message="$2"
  
  case "$error_code" in
    "400")
      if [[ "$error_message" == *"wrong file identifier"* ]]; then
        echo "❌ 文件ID错误: 重新上传文件"
      elif [[ "$error_message" == *"wrong type of the web document"* ]]; then
        echo "❌ 文件类型错误: 确保是音频文件"
      else
        echo "❌ 请求参数错误: $error_message"
      fi
      ;;
    "401")
      echo "❌ 认证失败: 检查Bot Token"
      ;;
    "403")
      echo "❌ 权限不足: Bot可能被踢出群组或用户阻止了Bot"
      ;;
    "404")
      echo "❌ 聊天不存在: 检查Chat ID"
      ;;
    "413")
      echo "❌ 文件太大: 超过50MB限制"
      ;;
    "429")
      echo "⚠️ 请求过于频繁: 等待后重试"
      # 提取重试等待时间
      local retry_after=$(echo "$error_message" | grep -o "retry after [0-9]*" | grep -o "[0-9]*")
      if [ -n "$retry_after" ]; then
        echo "等待 ${retry_after}秒后重试..."
        sleep "$retry_after"
      fi
      ;;
    *)
      echo "❌ Telegram API错误 ($error_code): $error_message"
      ;;
  esac
}
```

### 高级功能
```bash
# 发送带进度的语音消息（大文件）
send_voice_with_progress() {
  local audio_file="$1"
  
  # 分块上传（大文件）
  local chunk_size=10485760  # 10MB
  local file_size=$(stat -c%s "$audio_file")
  local total_chunks=$(( (file_size + chunk_size - 1) / chunk_size ))
  
  echo "📤 上传文件: $audio_file (${file_size}字节)"
  echo "📊 分块: $total_chunks 块"
  
  # 实际上Telegram API不支持分块上传
  # 这里只是示例，真实情况需要压缩文件
  if [ $file_size -gt 20971520 ]; then  # 20MB
    echo "⚠️ 文件较大，建议压缩"
    compress_audio "$audio_file"
    audio_file="${audio_file%.*}_compressed.ogg"
  fi
  
  send_telegram_voice "$audio_file"
}

# 批量发送
send_batch_voices() {
  local audio_files=("$@")
  local success_count=0
  local failure_count=0
  
  echo "🚀 开始批量发送 ${#audio_files[@]} 个语音消息"
  
  for audio_file in "${audio_files[@]}"; do
    echo "📤 发送: $(basename "$audio_file")"
    
    if send_telegram_voice "$audio_file"; then
      ((success_count++))
      echo "✅ 成功"
    else
      ((failure_count++))
      echo "❌ 失败"
    fi
    
    # 避免触发速率限制
    sleep 1
  done
  
  echo "📊 批量发送完成: $success_count 成功, $failure_count 失败"
  
  if [ $failure_count -eq 0 ]; then
    return 0
  else
    return 1
  fi
}
```

## 🔗 第三方服务集成

### Slack Webhook集成
```bash
# Slack配置
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export SLACK_CHANNEL="#notifications"
export SLACK_USERNAME="Telegram Bot Monitor"

# 发送Slack通知
send_slack_notification() {
  local message="$1"
  local level="${2:-"info"}"  # info, warning, error
  
  local color
  case "$level" in
    "info") color="#36a64f" ;;
    "warning") color="#ffcc00" ;;
    "error") color="#ff0000" ;;
    *) color="#808080" ;;
  esac
  
  curl -X POST "$SLACK_WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "{
      \"channel\": \"$SLACK_CHANNEL\",
      \"username\": \"$SLACK_USERNAME\",
      \"attachments\": [{
        \"color\": \"$color\",
        \"title\": \"Telegram语音消息通知\",
        \"text\": \"$message\",
        \"ts\": $(date +%s)
      }]
    }"
}
```

### Discord Webhook集成
```bash
# Discord配置
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
export DISCORD_USERNAME="Voice Bot"
export DISCORD_AVATAR_URL="https://example.com/bot-avatar.png"

# 发送Discord通知
send_discord_notification() {
  local message="$1"
  
  curl -X POST "$DISCORD_WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "{
      \"username\": \"$DISCORD_USERNAME\",
      \"avatar_url\": \"$DISCORD_AVATAR_URL\",
      \"content\": \"$message\"
    }"
}
```

### 企业微信机器人集成
```bash
# 企业微信配置
export WEWORK_WEBHOOK_KEY="your-webhook-key"
export WEWORK_BOT_NAME="语音消息助手"

# 发送企业微信通知
send_wework_notification() {
  local message="$1"
  
  curl -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$WEWORK_WEBHOOK_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"msgtype\": \"text\",
      \"text\": {
        \"content\": \"$message\",
        \"mentioned_list\": [\"@all\"]
      }
    }"
}
```

## 🛡️ 安全集成

### API密钥管理
```bash
# 使用HashiCorp Vault管理密钥
get_secret_from_vault() {
  local secret_path="$1"
  
  curl -s \
    -H "X-Vault-Token: $VAULT_TOKEN" \
    "https://vault.example.com/v1/secret/data/$secret_path" \
    | jq -r '.data.data.value'
}

# 环境变量配置
export TELEGRAM_BOT_TOKEN=$(get_secret_from_vault "telegram/bot-token")
export ALIYUN_ACCESS_KEY_ID=$(get_secret_from_vault "aliyun/access-key-id")
export ALIYUN_ACCESS_KEY_SECRET=$(get_secret_from_vault "aliyun/access-key-secret")
```

### 请求签名
```bash
# 请求签名（防止重放攻击）
sign_request() {
  local method="$1"
  local path="$2"
  local timestamp=$(date +%s)
  local nonce=$(openssl rand -hex 16)
  local body="$3"
  
  # 构建签名字符串
  local string_to_sign="${method}\n${path}\n${timestamp}\n${nonce}\n${body}"
  
  # 使用HMAC-SHA256签名
  local signature=$(echo -n "$string_to_sign" | openssl dgst -sha256 -hmac "$API_SECRET" | awk '{print $2}')
  
  echo "$timestamp:$nonce:$signature"
}

# 发送带签名的请求
send_signed_request() {
  local url="$1"
  local method="$2"
  local body="$3"
  
  local signature=$(sign_request "$method" "$(echo "$url" | sed 's|https://[^/]*||')" "$body")
  
  curl -X "$method" "$url" \
    -H "Content-Type: application/json" \
    -H "X-API-Signature: $signature" \
    -d "$body"
}
```

## 📊 监控集成

### Prometheus指标
```bash
# 暴露Prometheus指标
expose_metrics() {
  local port="${1:-9090}"
  
  cat > /tmp/metrics.html << EOF
# HELP telegram_voice_messages_total Total number of voice messages sent
# TYPE telegram_voice_messages_total counter
telegram_voice_messages_total{status="success"} $(grep -c "✅" /var/log/telegram-voice.log)
telegram_voice_messages_total{status="failure"} $(grep -c "❌" /var/log/telegram-voice.log)

# HELP telegram_voice_message_duration_seconds Duration of voice message processing
# TYPE telegram_voice_message_duration_seconds histogram
telegram_voice_message_duration_seconds_bucket{le="1"} 0
telegram_voice_message_duration_seconds_bucket{le="5"} 0
telegram_voice_message_duration_seconds_bucket{le="10"} 0
telegram_voice_message_duration_seconds_bucket{le="30"} 0
telegram_voice_message_duration_seconds_bucket{le="60"} 0
telegram_voice_message_duration_seconds_bucket{le="+Inf"} 0
telegram_voice_message_duration_seconds_sum 0
telegram_voice_message_duration_seconds_count 0
EOF
  
  # 启动简单的HTTP服务器
  python3 -m http.server "$port" --directory /tmp &
}

# 更新指标
update_metrics() {
  local duration="$1"
  local success="$2"
  
  # 更新Prometheus指标文件
  # 这里简化处理，实际应该使用Prometheus客户端库
  echo "更新监控指标: duration=${duration}s, success=$success"
}
```

### Grafana仪表板
```json
{
  "dashboard": {
    "title": "Telegram语音消息监控",
    "panels": [
      {
        "title": "消息发送成功率",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(telegram_voice_messages_total{status=\"success\"}[5m]) / rate(telegram_voice_messages_total[5m]) * 100",
            "legendFormat": "成功率"
          }
        ]
      },
      {
        "title": "处理时长分布",
        "type": "heatmap",
        "targets": [
          {
            "expr": "rate(telegram_voice_message_duration_seconds_bucket[5m])",
            "legendFormat": "{{le}}"
          }
        ]
      }
    ]
  }
}
```

## 🔄 Webhook集成

### 接收Webhook
```bash
# 简单的Webhook服务器
start_webhook_server() {
  local port="${1:-8080}"
  
  # 使用Python启动简单服务器
  cat > /tmp/webhook_server.py << 'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import threading

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.read.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            text = data.get('text', '')
            
            # 在新线程中处理，避免阻塞
            thread = threading.Thread(target=process_webhook, args=(text,))
            thread.start()
            
            self.send_response(202)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'accepted'}).encode())
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def log_message(self, format, *args):
        # 禁用默认日志
        pass

def process_webhook(text):
    # 调用TTS生成和发送
    subprocess.run([
        './scripts/tts_generator.sh', text,
        '|', 'xargs', './scripts/telegram_sender.sh'
    ], shell=True)

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), WebhookHandler)
    print('Webhook服务器启动在端口 8080')
    server.serve_forever()
EOF
  
  python3 /tmp/webhook_server.py &
}
```

### Webhook验证
```bash
# Webhook签名验证
verify_webhook_signature() {
  local payload="$1"
  local signature="$2"
  local secret="$WEBHOOK_SECRET"
  
  # 计算HMAC-SHA256
  local expected_signature=$(echo -n "$payload" | openssl dgst -sha256 -hmac "$secret" | awk '{print $2}')
  
  if [ "$signature" = "$expected_signature" ]; then
    echo "✅ Webhook签名验证通过"
    return 0
  else
    echo "❌ Webhook签名验证失败"
    return 1
  fi
}
```

## 🧪 集成测试

### API连通性测试
```bash
test_api_connectivity() {
  echo "🧪 测试API连通性..."
  
  # 测试Telegram API
  if curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe" | grep -q '"ok":true'; then
    echo "✅ Telegram API连接正常"
  else
    echo "❌ Telegram API连接失败"
    return 1
  fi
  
  # 测试TTS服务（示例：阿里云）
  if [ -n "$ALIYUN_TTS_APPKEY" ]; then
    echo "测试阿里云TTS连通性..."
    # 这里可以添加具体的测试代码
  fi
  
  echo "✅ 所有API连通性测试通过"
  return 0
}
```

### 端到端测试
```bash
test_end_to_end() {
  local test_text="这是一条测试消息"
  
  echo "🧪 运行端到端测试..."
  echo "测试文本: $test_text"
  
  # 生成音频
  local audio_file="/tmp/test_audio.ogg"
  if ! ./scripts/tts_generator.sh "$test_text" "$audio_file"; then
    echo "❌ TTS生成失败"
    return 1
  fi
  
  # 发送消息
  if ! ./scripts/telegram_sender.sh "$audio_file"; then
    echo "❌ 消息发送失败"
    return 1
  fi
  
  # 清理
  rm -f "$audio_file"
  
  echo "✅ 端到端测试通过"
  return 0
}
```

## 📝 配置管理

### 动态配置
```bash
# 从远程配置服务加载配置
load_config_from_remote() {
  local config_url="${1:-"https://config.example.com/telegram-voice"}"
  
  curl -s "$config_url" \
    | jq -r 'to_entries|map("export \(.key)=\(.value|tostring)")|.[]' \
    > /tmp/remote_config.sh
  
  source /tmp/remote_config.sh
}

# 配置热重载
setup_config_watcher() {
  local config_file="$1"
  
  # 使用inotifywait监控配置文件变化
  inotifywait -m -e modify "$config_file" |
    while read path action file; do
      echo "🔄 配置文件已更新，重新加载..."
      source "$config_file"
    done &
}
```

## 🔄 故障转移

### 多TTS服务故障转移
```bash
# TTS服务故障转移
call_tts_with_fallback() {
  local text="$1"
  local output_file="$2"
  
  # 尝试主TTS服务（阿里云）
  if call_aliyun_tts "$text" "$output_file"; then
    return 0
  fi
  
  echo "⚠️ 阿里云TTS失败，尝试备用服务..."
  
  # 尝试备用TTS服务（OpenAI）
  if call_openai_tts "$text" "$output_file"; then
    return 0
  fi
  
  echo "⚠️ OpenAI TTS失败，尝试本地TTS..."
  
  # 尝试本地TTS服务
  if call_local_tts "$text" "$output_file"; then
    return 0
  fi
  
  echo "❌ 所有TTS服务都失败"
  return 1
}
```

### 多消息通道故障转移
```bash
# 消息发送故障转移
send_message_with_fallback() {
  local audio_file="$1"
  local message="$2"
  
  # 尝试主通道（Telegram）
  if send_telegram_voice "$audio_file"; then
    return 0
  fi
  
  echo "⚠️ Telegram发送失败，尝试备用通道..."
  
  # 尝试备用通道（Slack，发送文本通知）
  if send_slack_notification "语音消息发送失败，原内容: $message"; then
    echo "✅ 已通过Slack发送通知"
    return 0
  fi
  
  # 尝试企业微信
  if send_wework_notification "语音消息发送失败，原内容: $message"; then
    echo "✅ 已通过企业微信发送通知"
    return 0
  fi
  
  echo "❌ 所有消息通道都失败"
  return 1
}
```

## 📈 性能优化

### API调用优化
```bash
# 批量API调用
batch_api_calls() {
  local operations=("$@")
  local batch_size=10  # 每批10个操作
  local total=${#operations[@]}
  
  for ((i=0; i<total; i+=batch_size)); do
    local batch=("${operations[@]:i:batch_size}")
    
    # 并行处理批次
    for operation in "${batch[@]}"; do
      eval "$operation" &
    done
    
    # 等待批次完成
    wait
    
    echo "✅ 完成批次 $((i/batch_size + 1))"
    
    # 避免触发速率限制
    sleep 1
  done
}
```

### 连接池
```bash
# 简单的连接池实现
create_connection_pool() {
  local pool_size="${1:-5}"
  
  for ((i=0; i<pool_size; i++)); do
    # 创建命名管道作为连接
    mkfifo "/tmp/connection_$i"
    
    # 启动后台进程处理连接
    (
      while true; do
        read -r command < "/tmp/connection_$i"
        eval "$command"
      done
    ) &
  done
}

# 使用连接池
use_connection_pool() {
  local command="$1"
  
  # 找到可用的连接
  for pipe in /tmp/connection_*; do
    if [ -p "$pipe" ]; then
      echo "$command" > "$pipe"
      break
    fi
  done
}
```

---

**总结**: API集成是Telegram语音消息技能的核心部分。通过灵活的配置、完善的错误处理和性能优化，可以构建出稳定可靠的消息发送系统。

*关键点*:
1. **多服务支持**: 不要依赖单一服务
2. **故障转移**: 主服务失败时自动切换到备用服务
3. **监控告警**: 实时监控API状态和性能
4. **安全防护**: 保护API密钥，验证请求

通过良好的API集成，可以让语音消息发送更加稳定和高效。