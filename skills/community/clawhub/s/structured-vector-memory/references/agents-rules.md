# AGENTS.md 记忆规则模板

以下内容应加入 workspace 的 AGENTS.md：

## 三層記憶系統

### 🔴 熱記憶（每次對話自動加載）
- `MEMORY.md` — 長期精華索引，≤8KB，當索引用不放流水賬
- `SOUL.md` / `USER.md` / `AGENTS.md` — 身份和規則

### 🟡 暖記憶（排程自動生成，memory_recall 可查）
- `memory/YYYY-MM-DD.md` — 每日記錄（Micro Sync 自動 + 手動補充）
- `second-brain/summaries/YYYY-MM-DD.md` — 每日結構化摘要（Daily Wrapup 自動）

### 🔵 冷記憶（按需查詢）
- `memory/archive/` — 從 MEMORY.md 退休的過時內容（不刪除，搬過去）
- `second-brain/` — 深度研究報告、存檔對話

### 決策深度規則（Micro Sync 用）
**要記：** 確定的決策、新規則、架構變更、「記住 XXX」指令
**不記：** 日常問答、閒聊、懸而未決的討論、排程 session

### 去重規則
存 `memory_store` 之前**必須**先 `memory_recall` 查重：
- 相似度 >70% → `memory_update` 更新，不新建
- 部分重疊 → 合併後 `memory_update`
- 無相似 → `memory_store` 新建

### 記憶 Scope 規則
存記憶時**必須**指定 scope，避免跨 agent 污染：
| 內容類型 | scope |
|----------|-------|
| 投資/財務/稅務 | `agent:finance` |
| 電商/選品/供應商 | `agent:ecommerce` |
| 內容/YouTube/小紅書 | `agent:content` |
| 系統/技術/Gateway | `agent:tech` |
| 跨 agent 共用 | global（不填 scope） |
