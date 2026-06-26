#!/bin/bash
# Micro Sync — 每天 5 次（10/13/16/19/22 點）
# 整合版：三層記憶 + LanceDB Pro
# 1. 掃 session 記決策（三層記憶）
# 2. 審核 autoCapture 抓的記憶（LanceDB 審核）

HEARTBEAT="$HOME/.openclaw/workspace/HEARTBEAT.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# 檢查是否在靜默時段（23:00-08:00）
HOUR=$(date '+%H')
if [ "$HOUR" -ge 23 ] || [ "$HOUR" -lt 8 ]; then
    exit 0
fi

# 寫入 HEARTBEAT 任務
cat >> "$HEARTBEAT" << EOF

# MICRO_SYNC @ $TIMESTAMP
- [ ] 掃描最近 3 小時的 session（用 sessions_list + sessions_history）
- [ ] 只記錄：確定的決策、新規則、架構變更、明確的「記住 XXX」指令
- [ ] 不記錄：日常問答、閒聊、懸而未決的討論
- [ ] 去重：memory_recall 查重，相似 >70% 則 memory_update 不新建
- [ ] Scope：按內容分配 agent:finance/content/ecommerce/tech，跨 agent 用 global
- [ ] 格式：原因→發現→結論
- [ ] 寫入 memory/$(date '+%Y-%m-%d').md（APPEND，不覆蓋）
- [ ] LanceDB 審核：檢查 autoCapture 最近抓的記憶，刪除明顯的垃圾/閒聊
- [ ] 完成後刪除此 MICRO_SYNC 段落
EOF

echo "[$TIMESTAMP] Micro sync task written to HEARTBEAT.md"
