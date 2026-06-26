#!/bin/bash
# Daily Wrap Up — 每天凌晨 1:00
# 全天對話完整回顧，生成結構化摘要到 second-brain
# 寫入 HEARTBEAT.md 觸發 agent 執行

HEARTBEAT="$HOME/.openclaw/workspace/HEARTBEAT.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
YESTERDAY=$(date -v-1d '+%Y-%m-%d' 2>/dev/null || date -d 'yesterday' '+%Y-%m-%d')
SUMMARY_DIR="$HOME/.openclaw/workspace/second-brain/summaries"

mkdir -p "$SUMMARY_DIR"

cat >> "$HEARTBEAT" << EOF

# DAILY_WRAPUP @ $TIMESTAMP
- [ ] 回顧昨天（$YESTERDAY）所有對話 session
- [ ] 過濾掉排程/cron 觸發的 session，只看人機對話
- [ ] 生成結構化摘要，寫入 second-brain/summaries/$YESTERDAY.md
- [ ] 摘要格式：
  - ## Decisions（確定的決策）
  - ## Action Items（待辦事項）
  - ## Key Conversations（關鍵對話摘要）
  - ## Technical Notes（技術筆記/踩坑）
  - ## Pending（未完成/待續）
  - ## Tomorrow（明天要做的事）
- [ ] 檢查 memory/$YESTERDAY.md 是否存在，不存在則同時建立
- [ ] 完成後刪除此 DAILY_WRAPUP 段落
EOF

echo "[$TIMESTAMP] Daily wrapup task written to HEARTBEAT.md"
