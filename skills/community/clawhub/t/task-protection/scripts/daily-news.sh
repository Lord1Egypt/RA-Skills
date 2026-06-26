#!/bin/bash
# 每日新闻推送脚本 - 已迁移到任务保障框架
# 每天 7:00 执行
# 推送内容：国际时事、财经热点、AI 新闻、北京天气

source /home/admin/.openclaw/workspace/scripts/task-utils.sh

# 设置 PATH
export PATH="$HOME/.local/share/pnpm:$HOME/.nvm/versions/node/v24.14.0/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

WORKSPACE="/home/admin/.openclaw/workspace"
TAVILY_API_KEY="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"
TASK_ID="news_$(date +%Y%m%d_%H%M%S)"

# 初始化任务
task_init "$TASK_ID" "每日新闻推送" "推送国际时事、财经热点、AI 新闻、北京天气"
task_start "$TASK_ID"

log() {
    task_log "$TASK_ID" "INFO" "$1"
}

warn() {
    task_log "$TASK_ID" "WARN" "$1"
}

error() {
    task_log "$TASK_ID" "ERROR" "$1"
}

log "=========================================="
log "📰 每日新闻推送开始"
log "=========================================="

# 阶段 1: 获取国际时事
task_stage "$TASK_ID" "获取国际时事" "running"
log "🌍 获取国际时事..."
INTERNATIONAL=$(curl -s "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d "{\"api_key\": \"$TAVILY_API_KEY\", \"query\": \"国际热点新闻 时事政治\", \"topic\": \"news\", \"time_range\": \"day\", \"max_results\": 5}" \
  | jq -r '.results[:3] | map("• " + .title) | join("\n")' 2>/dev/null)

if [ -n "$INTERNATIONAL" ] && [ "$INTERNATIONAL" != "null" ]; then
    task_stage "$TASK_ID" "获取国际时事" "done"
    log "✅ 国际时事获取成功"
else
    INTERNATIONAL="• 暂时无法获取国际新闻"
    task_stage "$TASK_ID" "获取国际时事" "warning"
    warn "⚠️ 国际新闻获取失败"
fi

# 阶段 2: 获取财经热点
task_stage "$TASK_ID" "获取财经热点" "running"
log "💰 获取财经热点..."
FINANCE=$(curl -s "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d "{\"api_key\": \"$TAVILY_API_KEY\", \"query\": \"财经新闻 股市 经济 2026\", \"topic\": \"news\", \"time_range\": \"day\", \"max_results\": 5}" \
  | jq -r '.results[:3] | map("• " + .title) | join("\n")' 2>/dev/null)

if [ -n "$FINANCE" ] && [ "$FINANCE" != "null" ]; then
    task_stage "$TASK_ID" "获取财经热点" "done"
    log "✅ 财经热点获取成功"
else
    FINANCE="• 暂时无法获取财经新闻"
    task_stage "$TASK_ID" "获取财经热点" "warning"
    warn "⚠️ 财经新闻获取失败"
fi

# 阶段 3: 获取 AI 新闻
task_stage "$TASK_ID" "获取 AI 新闻" "running"
log "🤖 获取 AI 新闻..."
AI_NEWS=$(curl -s "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d "{\"api_key\": \"$TAVILY_API_KEY\", \"query\": \"AI 人工智能 news March 2026\", \"topic\": \"news\", \"time_range\": \"day\", \"max_results\": 5}" \
  | jq -r '.results[:3] | map("• " + .title) | join("\n")' 2>/dev/null)

if [ -n "$AI_NEWS" ] && [ "$AI_NEWS" != "null" ]; then
    task_stage "$TASK_ID" "获取 AI 新闻" "done"
    log "✅ AI 新闻获取成功"
else
    AI_NEWS="• 暂时无法获取 AI 新闻"
    task_stage "$TASK_ID" "获取 AI 新闻" "warning"
    warn "⚠️ AI 新闻获取失败"
fi

# 阶段 4: 获取北京天气
task_stage "$TASK_ID" "获取北京天气" "running"
log "🌤️ 获取北京天气..."
WEATHER=$(curl -s "https://wttr.in/北京？format=3&lang=zh" 2>/dev/null || echo "天气数据暂不可用")

if [ -n "$WEATHER" ]; then
    task_stage "$TASK_ID" "获取北京天气" "done"
    log "✅ 北京天气获取成功"
else
    WEATHER="天气数据暂不可用"
    task_stage "$TASK_ID" "获取北京天气" "warning"
    warn "⚠️ 天气数据获取失败"
fi

# 阶段 5: 生成新闻简报
task_stage "$TASK_ID" "生成新闻简报" "running"
log "📝 生成新闻简报..."

DATE=$(date '+%Y年%m月%d日')
NEWSLETTER="# 📰 每日新闻简报

**日期**：$DATE

---

## 🌍 国际时事

$INTERNATIONAL

---

## 💰 财经热点

$FINANCE

---

## 🤖 AI 新闻

$AI_NEWS

---

## 🌤️ 北京天气

$WEATHER

---

_生成时间：$(date '+%H:%M') · 虾球 🦐_"

# 保存简报
NEWSLETTER_FILE="$WORKSPACE/newsletter-$(date +%Y%m%d).md"
echo "$NEWSLETTER" > "$NEWSLETTER_FILE"

task_stage "$TASK_ID" "生成新闻简报" "done"
log "✅ 新闻简报生成完成：$NEWSLETTER_FILE"

# 阶段 6: 推送到飞书
task_stage "$TASK_ID" "推送飞书" "running"
log "📤 推送到飞书..."

# 注意：openclaw message CLI 在脚本中无法工作，这里记录状态
# 实际推送由 AI 通过内置 message 工具完成
FEISHU_USER_ID="ou_0e29a2f5150f0ddb8dfe21db84113ad5"

# 尝试推送（会失败，但记录状态）
RESULT=$(/home/admin/.local/share/pnpm/openclaw message send --channel feishu --target "$FEISHU_USER_ID" --message "$NEWSLETTER" 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    task_stage "$TASK_ID" "推送飞书" "done"
    log "✅ 飞书推送成功"
    task_complete "$TASK_ID" "新闻推送完成，已发送到飞书"
    
    # 更新新闻推送专用状态文件（向后兼容）
    cat > "$WORKSPACE/memory/news-push-state.json" << EOF
{
  "lastPush": "$(date -Iseconds)",
  "status": "success",
  "failures": [],
  "consecutiveFailures": 0,
  "totalPushes": $(($(jq '.totalPushes // 0' "$WORKSPACE/memory/news-push-state.json" 2>/dev/null || echo 0) + 1)),
  "lastCheck": "$(date -Iseconds)",
  "nextScheduledPush": "$(date -d '+1 day' -Iseconds 2>/dev/null || date -Iseconds)"
}
EOF
else
    task_stage "$TASK_ID" "推送飞书" "failed"
    error "❌ 飞书推送失败"
    error "错误详情：$RESULT"
    
    # 分析失败原因
    if [[ "$RESULT" == *"command not found"* ]]; then
        task_fail "$TASK_ID" "推送失败：CLI 命令未找到" "command_not_found"
    elif [[ "$RESULT" == *"authentication"* ]] || [[ "$RESULT" == *"unauthorized"* ]]; then
        task_fail "$TASK_ID" "推送失败：认证错误" "authentication_failed"
    elif [[ "$RESULT" == *"network"* ]] || [[ "$RESULT" == *"timeout"* ]]; then
        task_fail "$TASK_ID" "推送失败：网络错误" "network_error"
    else
        task_fail "$TASK_ID" "推送失败：$RESULT" "unknown_error"
    fi
    
    # 更新新闻推送专用状态文件（向后兼容）
    local prev_failures=$(jq -c '.failures // []' "$WORKSPACE/memory/news-push-state.json" 2>/dev/null || echo '[]')
    local new_failure="{\"time\":\"$(date -Iseconds)\",\"reason\":\"$RESULT\"}"
    local updated_failures=$(echo "$prev_failures" | jq --argjson nf "$new_failure" '. + [$nf]')
    local consecutive=$(($(jq '.consecutiveFailures // 0' "$WORKSPACE/memory/news-push-state.json" 2>/dev/null || echo 0) + 1))
    
    cat > "$WORKSPACE/memory/news-push-state.json" << EOF
{
  "lastPush": "$(jq -r '.lastPush // "never"' "$WORKSPACE/memory/news-push-state.json" 2>/dev/null || echo "never")",
  "status": "failed",
  "failures": $updated_failures,
  "consecutiveFailures": $consecutive,
  "totalPushes": $(jq '.totalPushes // 0' "$WORKSPACE/memory/news-push-state.json" 2>/dev/null || echo 0),
  "lastCheck": "$(date -Iseconds)",
  "lastError": "$RESULT"
}
EOF
    
    log "⚠️ 状态已记录，请检查：$WORKSPACE/memory/news-push-state.json"
fi

log "=========================================="
log "📰 每日新闻推送结束"
log "=========================================="

# 输出摘要
echo ""
echo "===== 新闻推送摘要 ====="
task_status "$TASK_ID"
echo "========================"
