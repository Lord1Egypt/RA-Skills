# 🏆 最佳实践示例

基于实际使用经验的最佳实践示例，展示如何正确使用Telegram语音消息技能。

## 📋 示例目录

### 1. 基础使用示例
- [简单消息发送](#简单消息发送)
- [批量消息发送](#批量消息发送)
- [错误处理示例](#错误处理示例)

### 2. 高级功能示例
- [多TTS服务切换](#多tts服务切换)
- [监控和告警集成](#监控和告警集成)
- [性能优化示例](#性能优化示例)

### 3. 实际场景示例
- [每日提醒系统](#每日提醒系统)
- [客服机器人集成](#客服机器人集成)
- [多语言支持](#多语言支持)

## 🚀 简单消息发送

### 场景描述
发送一条简单的问候消息到Telegram。

### 代码示例
```bash
#!/bin/bash
# 简单消息发送示例

# 设置环境变量
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
export ALIYUN_TTS_API_KEY="your_aliyun_key"

# 要发送的消息
MESSAGE="你好，这是一条测试消息！"

# 生成音频
echo "🎤 生成音频..."
./scripts/tts_generator.sh "$MESSAGE" /tmp/test_audio.wav

# 转换为Telegram兼容格式
echo "🔄 转换格式..."
./scripts/audio_converter.sh /tmp/test_audio.wav /tmp/test_audio.ogg

# 发送到Telegram
echo "📤 发送消息..."
./scripts/telegram_sender.sh /tmp/test_audio.ogg

# 清理临时文件
echo "🧹 清理文件..."
rm -f /tmp/test_audio.wav /tmp/test_audio.ogg

echo "✅ 消息发送完成！"
```

### 最佳实践要点
1. **环境变量管理**: 使用环境变量而不是硬编码
2. **临时文件清理**: 发送后及时清理临时文件
3. **状态反馈**: 每个步骤都有清晰的输出

## 📦 批量消息发送

### 场景描述
批量发送多条消息，如每日提醒或通知列表。

### 代码示例
```bash
#!/bin/bash
# 批量消息发送示例

# 消息列表
MESSAGES=(
    "早上好！今天是美好的一天。"
    "记得喝足够的水。"
    "午休时间到了，休息一下吧。"
    "下午工作加油！"
    "今天的工作完成了吗？"
)

echo "🚀 开始批量发送 ${#MESSAGES[@]} 条消息"

# 创建临时目录
TEMP_DIR="/tmp/telegram_batch_$(date +%s)"
mkdir -p "$TEMP_DIR"

# 计数器
SUCCESS_COUNT=0
FAILURE_COUNT=0

# 批量处理
for i in "${!MESSAGES[@]}"; do
    MESSAGE="${MESSAGES[$i]}"
    INDEX=$((i + 1))
    
    echo ""
    echo "📤 发送第 $INDEX 条消息: $MESSAGE"
    
    # 生成唯一文件名
    AUDIO_WAV="$TEMP_DIR/message_$INDEX.wav"
    AUDIO_OGG="$TEMP_DIR/message_$INDEX.ogg"
    
    # 生成音频
    if ./scripts/tts_generator.sh "$MESSAGE" "$AUDIO_WAV"; then
        echo "✅ 音频生成成功"
    else
        echo "❌ 音频生成失败"
        ((FAILURE_COUNT++))
        continue
    fi
    
    # 转换格式
    if ./scripts/audio_converter.sh "$AUDIO_WAV" "$AUDIO_OGG"; then
        echo "✅ 格式转换成功"
    else
        echo "❌ 格式转换失败"
        ((FAILURE_COUNT++))
        continue
    fi
    
    # 发送消息
    if ./scripts/telegram_sender.sh "$AUDIO_OGG"; then
        echo "✅ 消息发送成功"
        ((SUCCESS_COUNT++))
    else
        echo "❌ 消息发送失败"
        ((FAILURE_COUNT++))
    fi
    
    # 避免触发速率限制
    sleep 2
done

# 清理
rm -rf "$TEMP_DIR"

# 输出统计
echo ""
echo "📊 批量发送完成"
echo "✅ 成功: $SUCCESS_COUNT"
echo "❌ 失败: $FAILURE_COUNT"
echo "📈 成功率: $((SUCCESS_COUNT * 100 / (SUCCESS_COUNT + FAILURE_COUNT)))%"
```

### 最佳实践要点
1. **唯一临时目录**: 使用时间戳创建唯一目录
2. **进度反馈**: 显示每条消息的处理状态
3. **速率控制**: 添加延迟避免触发API限制
4. **统计报告**: 提供详细的成功/失败统计

## 🛡️ 错误处理示例

### 场景描述
处理各种可能出现的错误情况。

### 代码示例
```bash
#!/bin/bash
# 错误处理示例

# 错误处理函数
handle_error() {
    local error_code="$1"
    local error_message="$2"
    local context="$3"
    
    echo "❌ 错误 ($context): $error_message"
    
    case "$error_code" in
        "TTS_GENERATION_FAILED")
            echo "💡 建议: 检查TTS服务配置和网络连接"
            # 尝试备用TTS服务
            ;;
        "AUDIO_CONVERSION_FAILED")
            echo "💡 建议: 检查ffmpeg安装和文件权限"
            # 尝试其他转换参数
            ;;
        "TELEGRAM_SEND_FAILED")
            echo "💡 建议: 检查Bot Token和Chat ID"
            # 实现重试机制
            ;;
        "FILE_NOT_FOUND")
            echo "💡 建议: 检查文件路径和权限"
            ;;
        "API_RATE_LIMIT")
            echo "💡 建议: 等待后重试，或减少请求频率"
            ;;
        *)
            echo "💡 建议: 查看详细日志，联系技术支持"
            ;;
    esac
    
    # 记录错误日志
    log_error "$context" "$error_code" "$error_message"
    
    # 发送错误通知（可选）
    send_error_notification "$context" "$error_message"
}

# 日志函数
log_error() {
    local context="$1"
    local code="$2"
    local message="$3"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "$timestamp [ERROR] $context - $code: $message" >> /var/log/telegram-voice-errors.log
}

# 错误通知函数
send_error_notification() {
    local context="$1"
    local message="$2"
    
    # 发送到Slack（示例）
    if [ -n "$SLACK_WEBHOOK_URL" ]; then
        curl -X POST "$SLACK_WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "{
                \"text\": \"🚨 Telegram语音消息错误\\n上下文: $context\\n错误: $message\"
            }" >/dev/null 2>&1
    fi
}

# 带错误处理的消息发送
send_message_safely() {
    local message="$1"
    
    echo "🔧 尝试发送消息: $message"
    
    # 生成音频（带错误处理）
    local audio_wav="/tmp/$(date +%s).wav"
    if ! ./scripts/tts_generator.sh "$message" "$audio_wav"; then
        handle_error "TTS_GENERATION_FAILED" "TTS生成失败" "$message"
        return 1
    fi
    
    # 转换格式（带错误处理）
    local audio_ogg="${audio_wav%.wav}.ogg"
    if ! ./scripts/audio_converter.sh "$audio_wav" "$audio_ogg"; then
        handle_error "AUDIO_CONVERSION_FAILED" "音频转换失败" "$audio_wav"
        rm -f "$audio_wav"
        return 1
    fi
    
    # 发送消息（带重试）
    local max_retries=3
    local retry_delay=2
    
    for attempt in $(seq 1 $max_retries); do
        if ./scripts/telegram_sender.sh "$audio_ogg"; then
            echo "✅ 消息发送成功 (第${attempt}次尝试)"
            rm -f "$audio_wav" "$audio_ogg"
            return 0
        fi
        
        if [ $attempt -lt $max_retries ]; then
            echo "⚠️ 第${attempt}次发送失败，${retry_delay}秒后重试..."
            sleep $retry_delay
            retry_delay=$((retry_delay * 2))  # 指数退避
        fi
    done
    
    # 所有重试都失败
    handle_error "TELEGRAM_SEND_FAILED" "消息发送失败（已尝试${max_retries}次）" "$message"
    rm -f "$audio_wav" "$audio_ogg"
    return 1
}

# 使用示例
echo "🧪 测试错误处理机制"

# 测试正常情况
send_message_safely "这是一条测试消息"

# 测试错误情况（模拟TTS失败）
echo ""
echo "🧪 模拟TTS失败场景"
# 这里可以故意设置错误的TTS配置来测试

echo ""
echo "✅ 错误处理示例完成"
```

### 最佳实践要点
1. **错误分类**: 根据错误类型采取不同策略
2. **重试机制**: 实现指数退避重试
3. **错误日志**: 记录详细错误信息
4. **通知告警**: 重要错误发送通知
5. **资源清理**: 确保临时文件被清理

## 🔄 多TTS服务切换

### 场景描述
在主TTS服务失败时自动切换到备用服务。

### 代码示例
```bash
#!/bin/bash
# 多TTS服务切换示例

# TTS服务配置
TTS_SERVICES=(
    "aliyun"    # 主服务
    "openai"    # 备用服务1
    "google"    # 备用服务2
    "local"     # 备用服务3（本地TTS）
)

# 当前使用的服务
CURRENT_TTS_SERVICE="aliyun"

# 根据服务选择TTS生成函数
generate_audio_with_tts() {
    local text="$1"
    local output_file="$2"
    
    echo "🎤 使用 $CURRENT_TTS_SERVICE TTS 生成音频..."
    
    case "$CURRENT_TTS_SERVICE" in
        "aliyun")
            generate_with_aliyun "$text" "$output_file"
            ;;
        "openai")
            generate_with_openai "$text" "$output_file"
            ;;
        "google")
            generate_with_google "$text" "$output_file"
            ;;
        "local")
            generate_with_local "$text" "$output_file"
            ;;
        *)
            echo "❌ 未知TTS服务: $CURRENT_TTS_SERVICE"
            return 1
            ;;
    esac
}

# 阿里云TTS生成
generate_with_aliyun() {
    local text="$1"
    local output_file="$2"
    
    # 调用阿里云TTS API
    # 这里简化处理，实际应该调用相应的脚本或API
    echo "  调用阿里云TTS..."
    
    # 模拟成功/失败
    if [ $((RANDOM % 10)) -lt 8 ]; then  # 80%成功率
        echo "  阿里云TTS生成成功"
        return 0
    else
        echo "  阿里云TTS生成失败"
        return 1
    fi
}

# OpenAI TTS生成
generate_with_openai() {
    local text="$1"
    local output_file="$2"
    
    echo "  调用OpenAI TTS..."
    
    # 模拟成功/失败
    if [ $((RANDOM % 10)) -lt 7 ]; then  # 70%成功率
        echo "  OpenAI TTS生成成功"
        return 0
    else
        echo "  OpenAI TTS生成失败"
        return 1
    fi
}

# Google TTS生成
generate_with_google() {
    local text="$1"
    local output_file="$2"
    
    echo "  调用Google TTS..."
    
    # 模拟成功/失败
    if [ $((RANDOM % 10)) -lt 6 ]; then  # 60%成功率
        echo "  Google TTS生成成功"
        return 0
    else
        echo "  Google TTS生成失败"
        return 1
    fi
}

# 本地TTS生成
generate_with_local() {
    local text="$1"
    local output_file="$2"
    
    echo "  调用本地TTS..."
    
    # 模拟成功/失败
    if [ $((RANDOM % 10)) -lt 9 ]; then  # 90%成功率（本地通常更可靠）
        echo "  本地TTS生成成功"
        return 0
    else
        echo "  本地TTS生成失败"
        return 1
    fi
}

# 故障转移函数
failover_tts_service() {
    local current_service="$1"
    
    echo "⚠️  $current_service 服务失败，尝试故障转移..."
    
    # 找到当前服务的索引
    local current_index=-1
    for i in "${!TTS_SERVICES[@]}"; do
        if [ "${TTS_SERVICES[$i]}" = "$current_service" ]; then
            current_index=$i
            break
        fi
    done
    
    # 尝试下一个服务
    if [ $current_index -ge 0 ] && [ $((current_index + 1)) -lt ${#TTS_SERVICES[@]} ]; then
        local next_service="${TTS_SERVICES[$((current_index + 1))]}"
        echo "🔄 切换到备用服务: $next_service"
        CURRENT_TTS_SERVICE="$next_service"
        return 0
    else
        echo "❌ 所有TTS服务都尝试失败"
        return 1
    fi
}

# 主函数：发送消息（带故障转移）
send_message_with_failover() {
    local message="$1"
    local max_attempts=${#TTS_SERVICES[@]}
    
    echo "🚀 发送消息: $message"
    echo "🔄 最多尝试 $max_attempts 个TTS服务"
    
    for attempt in $(seq 1 $max_attempts); do
        echo ""
        echo "🔄 第 $attempt 次尝试 (使用 $CURRENT_TTS_SERVICE)"
        
        # 生成音频
        local audio_file="/tmp/audio_$(date +%s).wav"
        if generate_audio_with_tts "$message" "$audio_file"; then
            echo "✅ TTS生成成功"
            
            # 转换格式
            local ogg_file="${audio_file%.wav}.ogg"
            if ./scripts/audio_converter.sh "$audio_file" "$ogg_file"; then
                # 发送消息
                if ./scripts/telegram_sender.sh "$ogg_file"; then
                    echo "✅ 消息发送成功"
                    rm -f "$audio_file" "$ogg_file"
                    return 0
                else
                    echo "❌ 消息发送失败"
                fi
            else
                echo "❌ 格式转换失败"
            fi
            
            rm -f "$audio_file" "$ogg_file"
        else
            echo "❌ TTS生成失败"
        fi
        
        # 如果还有备用服务，尝试故障转移
        if [ $attempt -lt $max_attempts ]; then
            if ! failover_tts_service "$CURRENT_TTS_SERVICE"; then
                break
            fi
        fi
    done
    
    echo "❌ 所有尝试都失败"
    return 1
}

# 使用示例
echo "🧪 测试多TTS服务切换"
send_message_with_failover "测试多TTS服务故障转移功能"

echo ""
echo "✅ 多TTS服务切换示例完成"
```

### 最佳实践要点
1. **服务优先级**: 定义清晰的服务优先级
2. **故障检测**: 及时检测服务失败
3. **自动切换**: 失败时自动切换到备用服务
4. **状态恢复**: 主服务恢复后可以切换回来
5. **服务监控**: 监控各个服务的可用性

## 📊 监控和告警集成

### 场景描述
集成监控系统，实时监控消息发送状态。

### 代码示例
```bash
#!/bin/bash
# 监控和告警集成示例

# Prometheus指标文件
PROMETHEUS_METRICS_FILE="/var/lib/prometheus/telegram_voice_metrics.prom"

# 初始化指标
init_metrics() {
    cat > "$PROMETHEUS_METRICS_FILE" << EOF
# HELP telegram_voice_messages_total Total number of voice messages sent
# TYPE telegram_voice_messages_total counter
telegram_voice_messages_total{status="success"} 0
telegram_voice_messages_total{status="failure"} 0

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

# HELP telegram_voice_message_size_bytes Size of voice messages
# TYPE telegram_voice_message_size_bytes histogram
telegram_voice_message_size_bytes_bucket{le="10240"} 0    # 10KB
telegram_voice_message_size_bytes_bucket{le="51200"} 0    # 50KB
telegram_voice_message_size_bytes_bucket{le="102400"} 0   # 100KB
telegram_voice_message_size_bytes_bucket{le="512000"} 0   # 500KB
telegram_voice_message_size_bytes_bucket{le="1048576"} 0  # 1MB
telegram_voice_message_size_bytes_bucket{le="+Inf"} 0
telegram_voice_message_size_bytes_sum 0
telegram_voice_message_size_bytes_count 0
EOF
}

# 更新指标
update_metric() {
    local metric_name="$1"
    local labels="$2"
    local value="$3"
    
    # 更新Prometheus指标文件
    sed -i "s/${metric_name}{${labels}} [0-9]*/${metric_name}{${labels}} ${value}/" "$PROMETHEUS_METRICS_FILE"
}

# 记录消息发送
record_message_sent() {
    local status="$1"  # success 或 failure
    local duration="$2"
    local size="$3"
    
    # 更新成功/失败计数器
    local current_count=$(grep "telegram_voice_messages_total{status=\"$status\"}" "$PROMETHEUS_METRICS_FILE" | grep -o '[0-9]*')
    local new_count=$((current_count + 1))
    update_metric "telegram_voice_messages_total" "status=\"$status\"" "$new_count"
    
    # 更新处理时长
    if [ "$status" = "success" ]; then
        # 找到对应的bucket
        local bucket="+Inf"
        if (( $(echo "$duration <= 1" | bc -l) )); then
            bucket="1"
        elif (( $(echo "$duration <= 5" | bc -l) )); then
            bucket="5"
        elif (( $(echo "$duration <= 10" | bc -l) )); then
            bucket="10"
        elif (( $(echo "$duration <= 30" | bc -l) )); then
            bucket="30"
        elif (( $(echo "$duration <= 60" | bc -l) )); then
            bucket="60"
        fi
        
        # 更新bucket
        local bucket_count=$(grep "telegram_voice_message_duration_seconds_bucket{le=\"$bucket\"}" "$PROMETHEUS_METRICS_FILE" | grep -o '[0-9]*')
        local new_bucket_count=$((bucket_count + 1))
        update_metric "telegram_voice_message_duration_seconds_bucket" "le=\"$bucket\"" "$new_bucket_count"
        
        # 更新sum和count
        local current_sum=$(grep "telegram_voice_message_duration_seconds_sum" "$PROMETHEUS_METRICS_FILE" | grep -o '[0-9.]*')
        local new_sum=$(echo "$current_sum + $duration" | bc)
        update_metric "telegram_voice_message_duration_seconds_sum" "" "$new_sum"
        
        local current_count=$(grep "telegram_voice_message_duration_seconds_count" "$PROMETHEUS_METRICS_FILE" | grep -o '[0-9]*')
        local new_count=$((current_count + 1))
        update_metric "telegram_voice_message_duration_seconds_count" "" "$new_count"
    fi
    
    # 更新文件大小指标
    if [ -n "$size" ]; then
        local bucket="+Inf"
        if [ "$size" -le 10240 ]; then
            bucket="10240"
        elif [ "$size" -le 51200 ]; then
            bucket="51200"
        elif [ "$size" -le 102400 ]; then
            bucket="102400"
        elif [ "$size" -le 512000 ]; then
            bucket="512000"
        elif [ "$size" -le 1048576 ]; then
            bucket="1048576"
        fi
        
        local bucket_count=$(grep "telegram_voice_message_size_bytes_bucket{le=\"$bucket\"}" "$PROMETHEUS_METRICS_FILE" | grep -o '[0-9]*')
        local new_bucket_count=$((bucket_count + 1))
        update_metric "telegram_voice_message_size_bytes_bucket" "le=\"$bucket\"" "$new_bucket_count"
        
        local current_sum=$(grep "telegram_voice_message_size_bytes_sum" "$PROMETHEUS_METRICS_FILE" | grep -o '[0-9]*')
        local new_sum=$((current_sum + size))
        update_metric "telegram_voice_message_size_bytes_sum" "" "$new_sum"
        
        local current_count=$(grep "telegram_voice_message_size_bytes_count" "$PROMETHEUS_METRICS_FILE" | grep -o '[0-9]*')
        local new_count=$((current_count + 1))
        update_metric "telegram_voice_message_size_bytes_count" "" "$new_count"
    fi
}

# 发送消息（带监控）
send_message_with_monitoring() {
    local message="$1"
    local start_time=$(date +%s.%N)
    
    echo "📊 发送消息（带监控）: $message"
    
    # 生成音频
    local audio_wav="/tmp/monitored_$(date +%s).wav"
    if ! ./scripts/tts_generator.sh "$message" "$audio_wav"; then
        local end_time=$(date +%s.%N)
        local duration=$(echo "$end_time - $start_time" | bc)
        record_message_sent "failure" "$duration" ""
        echo "❌ 消息发送失败（已记录监控指标）"
        return 1
    fi
    
    # 获取文件大小
    local file_size=$(stat -c%s "$audio_wav" 2>/dev/null || echo "0")
    
    # 转换格式
    local audio_ogg="${audio_wav%.wav}.ogg"
    if ! ./scripts/audio_converter.sh "$audio_wav" "$audio_ogg"; then
        local end_time=$(date +%s.%N)
        local duration=$(echo "$end_time - $start_time" | bc)
        record_message_sent "failure" "$duration" "$file_size"
        rm -f "$audio_wav"
        echo "❌ 格式转换失败（已记录监控指标）"
        return 1
    fi
    
    # 发送消息
    if ./scripts/telegram_sender.sh "$audio_ogg"; then
        local end_time=$(date +%s.%N)
        local duration=$(echo "$end_time - $start_time" | bc)
        record_message_sent "success" "$duration" "$file_size"
        echo "✅ 消息发送成功（已记录监控指标）"
        echo "  处理时长: ${duration}秒"
        echo "  文件大小: ${file_size}字节"
        rm -f "$audio_wav" "$audio_ogg"
        return 0
    else
        local end_time=$(date +%s.%N)
        local duration=$(echo "$end_time - $start_time" | bc)
        record_message_sent "failure" "$duration" "$file_size"
        echo "❌ 消息发送失败（已记录监控指标）"
        rm -f "$audio_wav" "$audio_ogg"
        return 1
    fi
}

# 告警检查
check_alerts() {
    echo "🔔 检查告警条件..."
    
    # 读取当前指标
    local success_count=$(grep 'telegram_voice_messages_total{status="success"}' "$PROMETHEUS_METRICS_FILE" | grep -o '[0-9]*')
    local failure_count=$(grep 'telegram_voice_messages_total{status="failure"}' "$PROMETHEUS_METRICS_FILE" | grep -o '[0-9]*')
    local total_count=$((success_count + failure_count))
    
    if [ $total_count -gt 0 ]; then
        local success_rate=$((success_count * 100 / total_count))
        echo "  成功率: ${success_rate}% (${success_count}/${total_count})"
        
        # 检查告警条件
        if [ $success_rate -lt 90 ]; then
            echo "🚨 告警: 成功率低于90%！"
            send_alert "成功率低于90% (当前: ${success_rate}%)"
        fi
        
        if [ $failure_count -gt 10 ]; then
            echo "🚨 告警: 失败次数超过10次！"
            send_alert "失败次数超过10次 (当前: ${failure_count}次)"
        fi
    else
        echo "  暂无数据"
    fi
}

# 发送告警
send_alert() {
    local message="$1"
    
    echo "📢 发送告警: $message"
    
    # 发送到Slack
    if [ -n "$SLACK_WEBHOOK_URL" ]; then
        curl -X POST "$SLACK_WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "{
                \"text\": \"🚨 Telegram语音消息告警\\n$message\\n时间: $(date)\"
            }" >/dev/null 2>&1
    fi
    
    # 发送到Telegram（可选）
    if [ -n "$TELEGRAM_ALERT_CHAT_ID" ]; then
        ./scripts/tts_generator.sh "告警：$message" /tmp/alert.wav
        ./scripts/audio_converter.sh /tmp/alert.wav /tmp/alert.ogg
        TELEGRAM_CHAT_ID="$TELEGRAM_ALERT_CHAT_ID" ./scripts/telegram_sender.sh /tmp/alert.ogg
        rm -f /tmp/alert.wav /tmp/alert.ogg
    fi
}

# 使用示例
echo "📊 监控和告警集成示例"

# 初始化指标
init_metrics

# 发送几条测试消息
echo ""
echo "🧪 发送测试消息..."
send_message_with_monitoring "第一条测试消息"
send_message_with_monitoring "第二条测试消息"
send_message_with_monitoring "第三条测试消息"

# 检查告警
echo ""
check_alerts

# 显示当前指标
echo ""
echo "📈 当前监控指标:"
cat "$PROMETHEUS_METRICS_FILE"

echo ""
echo "✅ 监控和告警集成示例完成"
```

### 最佳实践要点
1. **指标收集**: 收集关键性能指标
2. **实时监控**: 实时跟踪系统状态
3. **告警机制**: 设置合理的告警阈值
4. **多通道告警**: 通过多个渠道发送告警
5. **历史数据分析**: 分析趋势，预测问题

## ⚡ 性能优化示例

### 场景描述
优化消息发送性能，提高处理速度。

### 代码示例
```bash
#!/bin/bash
# 性能优化示例

# 并发处理函数
process_concurrently() {
    local messages=("$@")
    local max_concurrent=3  # 最大并发数
    
    echo "⚡ 并发处理 ${#messages[@]} 条消息 (最大并发: $max_concurrent)"
    
    # 创建临时目录
    local temp_dir="/tmp/concurrent_$(date +%s)"
    mkdir -p "$temp_dir"
    
    # 进程ID数组
    local pids=()
    local results=()
    
    # 并发处理
    for i in "${!messages[@]}"; do
        local message="${messages[$i]}"
        local index=$((i + 1))
        
        (
            echo "  🚀 启动任务 $index: $message"
            
            # 生成唯一文件名
            local audio_wav="$temp_dir/message_$index.wav"
            local audio_ogg="$temp_dir/message_$index.ogg"
            
            # 处理消息
            if ./scripts/tts_generator.sh "$message" "$audio_wav" && \
               ./scripts/audio_converter.sh "$audio_wav" "$audio_ogg" && \
               ./scripts/telegram_sender.sh "$audio_ogg"; then
                echo "  ✅ 任务 $index 完成"
                exit 0  # 成功
            else
                echo "  ❌ 任务 $index 失败"
                exit 1  # 失败
            fi
        ) &
        
        pids+=($!)
        results+=("running")
        
        # 控制并发数
        if [ ${#pids[@]} -ge $max_concurrent ]; then
            # 等待任意一个进程完成
            wait -n
            # 更新完成状态
            update_results
        fi
    done
    
    # 等待所有剩余进程
    echo "⏳ 等待所有任务完成..."
    for pid in "${pids[@]}"; do
        wait "$pid"
    done
    
    update_results
    
    # 统计结果
    local success_count=0
    local failure_count=0
    for result in "${results[@]}"; do
        if [ "$result" = "success" ]; then
            ((success_count++))
        else
            ((failure_count++))
        fi
    done
    
    # 清理
    rm -rf "$temp_dir"
    
    echo ""
    echo "📊 并发处理完成"
    echo "✅ 成功: $success_count"
    echo "❌ 失败: $failure_count"
    
    return $failure_count
}

# 更新结果状态
update_results() {
    for i in "${!pids[@]}"; do
        local pid="${pids[$i]}"
        if [ "${results[$i]}" = "running" ] && ! kill -0 "$pid" 2>/dev/null; then
            # 进程已结束，检查退出状态
            if wait "$pid"; then
                results[$i]="success"
            else
                results[$i]="failure"
            fi
        fi
    done
}

# 缓存优化
setup_cache() {
    local cache_dir="/var/cache/telegram-voice"
    
    echo "💾 设置缓存系统..."
    
    # 创建缓存目录
    mkdir -p "$cache_dir"
    
    # 检查缓存
    check_cache() {
        local message="$1"
        local cache_key=$(echo -n "$message" | md5sum | cut -d' ' -f1)
        local cache_file="$cache_dir/$cache_key.ogg"
        
        if [ -f "$cache_file" ]; then
            echo "  💾 使用缓存: $cache_file"
            echo "$cache_file"
            return 0
        else
            return 1
        fi
    }
    
    # 添加到缓存
    add_to_cache() {
        local message="$1"
        local audio_file="$2"
        local cache_key=$(echo -n "$message" | md5sum | cut -d' ' -f1)
        local cache_file="$cache_dir/$cache_key.ogg"
        
        cp "$audio_file" "$cache_file"
        echo "  💾 添加到缓存: $cache_file"
    }
    
    # 清理旧缓存
    cleanup_old_cache() {
        local max_age_days=30
        echo "  🧹 清理超过 ${max_age_days} 天的缓存..."
        find "$cache_dir" -name "*.ogg" -mtime +$max_age_days -delete
    }
    
    # 导出函数
    export -f check_cache add_to_cache cleanup_old_cache
    export cache_dir
}

# 使用缓存发送消息
send_message_with_cache() {
    local message="$1"
    
    echo "🔍 检查缓存: $message"
    
    # 检查缓存
    if cache_file=$(check_cache "$message"); then
        echo "✅ 缓存命中"
    else
        echo "❌ 缓存未命中，生成新音频"
        
        # 生成音频
        local temp_wav="/tmp/$(date +%s).wav"
        local temp_ogg="/tmp/$(date +%s).ogg"
        
        if ./scripts/tts_generator.sh "$message" "$temp_wav" && \
           ./scripts/audio_converter.sh "$temp_wav" "$temp_ogg"; then
            # 添加到缓存
            add_to_cache "$message" "$temp_ogg"
            cache_file="$temp_ogg"
        else
            echo "❌ 音频生成失败"
            return 1
        fi
    fi
    
    # 发送消息
    if ./scripts/telegram_sender.sh "$cache_file"; then
        echo "✅ 消息发送成功"
        
        # 如果是临时文件，清理
        if [[ "$cache_file" == /tmp/* ]]; then
            rm -f "$temp_wav" 2>/dev/null
        fi
        
        return 0
    else
        echo "❌ 消息发送失败"
        return 1
    fi
}

# 使用示例
echo "⚡ 性能优化示例"

# 测试消息
TEST_MESSAGES=(
    "早上好"
    "中午好" 
    "下午好"
    "晚上好"
    "晚安"
    "谢谢"
    "不客气"
    "请稍等"
    "正在处理"
    "已完成"
)

echo ""
echo "1. 测试并发处理"
echo "================="
process_concurrently "${TEST_MESSAGES[@]:0:5}"

echo ""
echo "2. 测试缓存优化"
echo "================="
setup_cache

# 第一次发送（应该缓存未命中）
echo ""
echo "第一次发送（应该缓存未命中）"
send_message_with_cache "测试缓存功能"

# 第二次发送（应该缓存命中）
echo ""
echo "第二次发送（应该缓存命中）"
send_message_with_cache "测试缓存功能"

# 清理旧缓存
cleanup_old_cache

echo ""
echo "✅ 性能