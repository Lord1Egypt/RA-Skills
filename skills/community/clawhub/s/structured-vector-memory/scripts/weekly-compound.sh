#!/bin/bash
# Weekly Compound — 每週日凌晨 3:00
# 記憶減脂 + 知識蒸餾 + Archive 過時內容
# 整合 micro sync + daily wrapup 的數據，更新 MEMORY.md

HEARTBEAT="$HOME/.openclaw/workspace/HEARTBEAT.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
MEMORY_FILE="$HOME/.openclaw/workspace/MEMORY.md"
ARCHIVE_DIR="$HOME/.openclaw/workspace/memory/archive"
MEMORY_SIZE=$(wc -c < "$MEMORY_FILE" 2>/dev/null || echo 0)

mkdir -p "$ARCHIVE_DIR"

cat >> "$HEARTBEAT" << EOF

# WEEKLY_COMPOUND @ $TIMESTAMP
- [ ] MEMORY.md 當前大小：${MEMORY_SIZE} bytes
- [ ] 數據來源：memory/*.md（micro sync）+ second-brain/summaries/（daily wrapup）
- [ ] 步驟：
  1. 備份 MEMORY.md → memory/archive/MEMORY-backup-$(date '+%Y%m%d').md
  2. 交叉比對本週 memory/ 和 second-brain/summaries/ 的內容
  3. 蒸餾：值得長期保留的 → 寫入 MEMORY.md
  4. 減脂：已完成的項目、過時的設定、太細節的內容 → 搬到 memory/archive/
  5. 搬走的內容不是刪除，memory_search 仍可查到
  6. **檢查本週有無架構性變更（如新增 agent/workflow），如有，更新 SYSTEM_GUIDE.md**
  7. 確保 MEMORY.md ≤ 8KB（安全線，索引化而非流水賬）
  8. SOUL.md 絕對不動
  9. 記錄更新前後 size 對比
- [ ] 完成後刪除此 WEEKLY_COMPOUND 段落
EOF

echo "[$TIMESTAMP] Weekly compound task written to HEARTBEAT.md (memory: ${MEMORY_SIZE} bytes)"
