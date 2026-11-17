---
name: reading-habit-tracker
description: 閱讀習慣追蹤系統：目標設定（年目標/書單/頁數/時長）、進度追蹤、每週/每月分析報告、落後預警、視覺化統計。與 reading_progress.py（專注打卡）差異化：目標導向、計劃管理、深度數據分析。
---

# 📊 Reading Habit Tracker — 閱讀習慣追蹤系統

## 概述

**目標導向** vs 打卡記錄——這套系統幫你：
- 📌 設定年度/月度閱讀目標（書本數/頁數/時長）
- 📋 建立書單追蹤（想讀/在讀/已讀）
- ⏱️ 記錄每次閱讀 session（頁數/時長/章節）
- 📈 每週/月自動分析：完成率、落後預警、趨勢洞察
- 🏆 達成里程碑時主動祝賀

**觸發關鍵字：** 閱讀目標、讀書計劃、每月閱讀、追蹤進度、閱讀統計、讀書報告、落後了嗎、本月讀完、設立目標、讀了多少

---

## 與 reading_progress.py 的差異

| 維度 | reading_progress.py | reading-habit-tracker |
|------|---------------------|-----------------------|
| 核心概念 | 每日打卡事件 | 目標 + 計劃管理 |
| 目標設定 | 無 | 年/月/單書目標 |
| 數據顆粒 | 單次 session | session + 書本 + 總目標 |
| 報告頻率 | 手動 stats | 每週自動報告 + 落後預警 |
| 適用場景 | 維持習慣 | 達成閱讀目標 |

---

## 腳本清單

| 腳本 | 用途 |
|------|------|
| `scripts/goal_manager.py` | 目標管理（設定/查看/刪除年度/月度/單書目標） |
| `scripts/session_logger.py` | Session 記錄（每次閱讀的頁數/時長/備註） |
| `scripts/analytics.py` | 數據分析（完成率/落後預警/每週報告） |
| `scripts/visualizer.py` | 視覺化（ASCII 進度條/終端彩色圖表） |
| `scripts/booklist_manager.py` | 書單管理（想讀/在讀/已讀/放棄） |

---

## 使用範例

```bash
# 設定年度目標
python3 scripts/goal_manager.py set --type yearly --books 30 --pages 5000 --hours 200

# 記錄一次閱讀 session
python3 scripts/session_logger.py log \
  --book "原子習慣" \
  --pages 30 \
  --minutes 45 \
  --note "第3章完"

# 查看進度儀表板
python3 scripts/analytics.py dashboard

# 生成週報
python3 scripts/analytics.py weekly

# 管理書單
python3 scripts/booklist_manager.py add --title "深度工作" --status to-read
python3 scripts/booklist_manager.py list --status reading
```

---

## 數據儲存

所有數據儲存在 `~/.bookshelf-plus/habit_tracker/` 目錄：
- `goals.json` — 目標設定
- `sessions.json` — 閱讀 session 記錄
- `booklist.json` — 書單狀態
- `reports/` — 生成的報告

---

## Cron Job（建議）

```bash
# 每日 22:00 落後預警
openclaw cron add \
  --name "reading-habit-alert" \
  --schedule "0 22 * * *" \
  --tz "Asia/Taipei" \
  --payload-kind agentTurn \
  --message "執行閱讀習慣追蹤預警：python3 ~/.qclaw/skills/reading-habit-tracker/scripts/analytics.py alert --format text。若目標落後，主動發送提醒訊息。"
```
