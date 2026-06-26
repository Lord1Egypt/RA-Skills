# 三層記憶系統架構 v1.0

**創建時間：** 2026-04-05 06:52  
**CEO 要求：** 2026-04-04 18:26  
**狀態：** ✅ 已交付使用  
**負責人：** monitor（主導）+ skill-dev（支援）+ main（驗收）

---

## 📂 目錄結構

```
workspace/
├── memory-l1-daily/          # Layer 1：日常對話記憶
│   ├── 2026-04-05.md         # 每日對話記錄
│   └── ...
├── memory-l2-events/         # Layer 2：重大事件記憶
│   ├── ceo-decisions.md      # CEO 決策記錄
│   ├── errors-lessons.md     # 錯誤與教訓
│   └── project-milestones.md # 項目里程碑
├── memory-l3-longterm/       # Layer 3：長期記憶
│   ├── ceo-preferences.md    # CEO 習慣與偏好
│   ├── agent-protocols.md    # Agent 協作協議
│   └── knowledge-graph.md    # 知識圖譜
├── SESSION-STATE.md          # WAL 協議（活躍工作記憶）
├── MEMORY.md                 # 長期記憶歸檔（主文件）
└── .learnings/               # 學習記錄
    ├── ERRORS.md
    ├── LEARNINGS.md
    └── FEATURE_REQUESTS.md
```

---

## 🎯 三層定義

### Layer 1：日常對話記憶（memory-l1-daily/）

**用途：** 記錄每日對話、任務、上下文  
**保留期：** 7 日（之後歸檔到 L3 或刪除）  
**負責人：** 所有 Agent（自動記錄）  
**格式：**

```markdown
# YYYY-MM-DD 對話記錄

## 對話摘要
- 時間：HH:MM
- 參與者：CEO + Agent
- 主題：XXX

## 關鍵內容
- 任務分配：T137 三層記憶系統
- CEO 指令：即刻交付使用
- 決策：無

## 待跟進
- [ ] T137 第三階段配置
```

---

### Layer 2：重大事件記憶（memory-l2-events/）

**用途：** CEO 決策、錯誤教訓、項目里程碑  
**保留期：** 永久（重要事件）  
**負責人：** monitor（分類存入）  
**格式：**

```markdown
## 事件類型：ceo_decision / error_lesson / milestone

**時間：** YYYY-MM-DD HH:MM  
**相關任務：** T137  
**描述：** CEO 要求三層記憶系統即刻交付使用  
**影響：** 系統架構變更  
**教訓：** 任務記錄後必須執行，唔係只係寫低
```

---

### Layer 3：長期記憶（memory-l3-longterm/）

**用途：** CEO 習慣、Agent 協議、知識圖譜  
**保留期：** 永久  
**負責人：** monitor（每週歸檔）  
**格式：**

```markdown
# CEO 習慣與偏好

## 工作習慣
- 喜歡：任務分配畀子 Agent
- 不喜歡：main 獨自做所有嘢
- 要求：行動前必須搜索記憶

## 溝通風格
- 語言：廣東話
- 語氣：直接、高效
- 反饋：即時批評 + 具體建議
```

---

## 🔄 數據流動

```
對話發生 → L1 記錄（所有 Agent）
         ↓
每日 23:00 → monitor 分類 → L2（重大事件）
         ↓
每週日 23:59 → monitor 歸檔 → L3（長期記憶）
         ↓
行動前 → 所有 Agent 搜索 L1+L2+L3
```

---

## ✅ 使用前檢查清單

**每次行動前必須執行：**

```bash
# 1. 搜索記憶
./scripts/memory-check.sh "<關鍵詞>"

# 2. 檢查 SESSION-STATE.md
cat SESSION-STATE.md | grep "<關鍵詞>"

# 3. 檢查錯誤記錄
cat .learnings/ERRORS.md | grep "<關鍵詞>"

# 4. 檢查學習記錄
cat .learnings/LEARNINGS.md | grep "<關鍵詞>"
```

---

## 📊 使用率監控

**monitor 負責：**
- 每日檢查 Agent 有無使用 memory-check.sh
- 每週統計記憶搜索次數
- 每月報告記憶系統健康度

**指標：**
- 記憶搜索率（行動前搜索 %）
- 錯誤重複率（Recurrence-Count）
- 記憶歸檔率（L1→L2→L3）

---

## 🚀 即刻使用指南

### Agent 工作流程

1. **收到任務** → 執行 `memory-check.sh <任務關鍵詞>`
2. **搜索記憶** → 讀取 L1+L2+L3 相關記錄
3. **提取教訓** → 避免重複錯誤
4. **執行任務** → 記錄 WAL 到 SESSION-STATE.md
5. **完成任务** → 寫入 L1 日常記憶

### CEO 工作流程

1. **提出任務** → Agent 自動搜索記憶
2. **收到回覆** → 包含記憶引用（如有）
3. **發現錯誤** → Agent 自動記錄到 L2
4. **每週覆盤** → monitor 提供 L3 歸檔報告

---

## 📝 本次交付記錄

**時間：** 2026-04-05 06:52  
**交付內容：**
- ✅ 三層記憶目錄創建
- ✅ 配置文件創建
- ✅ 使用指南創建
- ⏳ 語義搜索配置（第三階段）
- ⏳ Heartbeat 集成（第三階段）

**狀態：** 已交付使用（第一、二階段完成）  
**待完成：** 第三階段（語義搜索、Heartbeat 集成）

**本次對話記錄：** 已寫入 `memory-l1-daily/2026-04-05.md`
