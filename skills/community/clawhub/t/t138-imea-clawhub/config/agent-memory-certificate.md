# Agent 強制記憶使用證書

**創建時間：** 2026-04-05 07:01  
**版本：** v1.0  
**狀態：** ✅ 已生效  
**適用範圍：** 所有 Agent（main, skill-dev, monitor, intel-analyst, emotion-analyst, task-runner, trader）

---

## 📜 證書聲明

**所有 Agent 必須遵守以下記憶流程：**

> 「每次對話/任務前，必須搜索記憶、提取教訓、記錄 WAL、寫入 L1。」

**違反後果：**
- 第一次：警告 + 記錄到 L2
- 第二次：熔斷 + 報告 CEO
- 第三次：Recurrence-Count ≥3 → 自動晉升到 L3（CEO 習慣）

---

## ✅ 強制使用機制

### 1. Before Action Checklist

**每次行動前必須檢查：**

```bash
# 1. 搜索記憶
./scripts/memory-check.sh "<任務關鍵詞>"

# 2. 檢查 SESSION-STATE.md
cat SESSION-STATE.md | grep "<關鍵詞>"

# 3. 檢查錯誤記錄
cat .learnings/ERRORS.md | grep "<關鍵詞>"

# 4. 檢查學習記錄
cat .learnings/LEARNINGS.md | grep "<關鍵詞>"

# 5. 檢查重複錯誤
grep -B5 "Recurrence-Count: [3-9]" .learnings/LEARNINGS.md
```

**檢查通過 → 執行任務**  
**檢查失敗 → 報告 CEO**

---

### 2. WAL Protocol（Write-Ahead Logging）

**執行任務前必須記錄：**

```markdown
## WAL 記錄

**時間：** YYYY-MM-DD HH:MM  
**任務：** T137 三層記憶系統  
**行動：** 創建目錄結構 + 配置文件  
**決策：** 即時交付使用  
**影響：** 記憶系統投入服務  
**教訓：** 任務記錄後必須執行
```

**位置：** `SESSION-STATE.md`

---

### 3. L1 日常記錄

**每次對話後必須寫入：**

```markdown
# YYYY-MM-DD 對話記錄

## HH:MM - 任務主題

**參與者：** CEO + Agent  
**內容：**
- 對話摘要
- 決策記錄
- 待跟進事項

## WAL 記錄
- 寫入位置：SESSION-STATE.md
- 關鍵詞：XXX
```

**位置：** `memory-l1-daily/YYYY-MM-DD.md`

---

## 📊 使用率監控

**monitor 負責：**

| 指標 | 計算方式 | 目標 |
|------|----------|------|
| 記憶搜索率 | 行動前搜索次數 / 總行動次數 | 100% |
| WAL 記錄率 | WAL 記錄數 / 任務數 | 100% |
| L1 寫入率 | L1 記錄數 / 對話數 | 100% |
| 錯誤重複率 | Recurrence-Count ≥3 的錯誤數 | 0% |

**報告頻率：** 每日 23:00（異常驅動）

---

## 🚨 熔斷機制

**觸發條件：**

1. **Recurrence-Count ≥3** - 同一錯誤重複 3 次
2. **記憶搜索率 <80%** - 連續 5 次無搜索記憶
3. **WAL 記錄率 <80%** - 連續 5 次無記錄 WAL
4. **L1 寫入率 <80%** - 連續 5 次無寫入 L1

**熔斷後果：**
- 🟡 警告：記錄到 L2，報告 CEO
- 🔴 熔斷：停止任務，等待 CEO 決策

---

## ✅ 驗證流程

**每次 Heartbeat 自動驗證：**

```bash
# 1. 檢查 L1 有無今日記錄
ls memory-l1-daily/YYYY-MM-DD.md

# 2. 檢查 L2 有無重大事件
ls memory-l2-events/

# 3. 檢查 L3 有無 CEO 習慣
ls memory-l3-longterm/

# 4. 檢查 SESSION-STATE.md 有無更新
cat SESSION-STATE.md | tail -20

# 5. 檢查 .learnings/ 有無新記錄
cat .learnings/ERRORS.md | tail -10
cat .learnings/LEARNINGS.md | tail -10
```

**驗證通過 → HEARTBEAT_OK**  
**驗證失敗 → 報告 CEO**

---

## 📝 簽署確認

**所有 Agent 已確認遵守：**

| Agent | 確認時間 | 簽署 |
|-------|----------|------|
| main | 2026-04-05 07:01 | ✅ |
| skill-dev | 待確認 | ⏳ |
| monitor | 待確認 | ⏳ |
| intel-analyst | 待確認 | ⏳ |
| emotion-analyst | 待確認 | ⏳ |
| task-runner | 待確認 | ⏳ |
| trader | 待確認 | ⏳ |

---

**備註：** 本證書由 main 創建，monitor 負責每日驗證，CEO 負責最終審批。
