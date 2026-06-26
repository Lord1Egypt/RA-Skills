# notebook-rag skill

version: 1.0.0

查詢 SumoNoteBook 知識庫並返回相關內容作為 context。

## 觸發條件

當需要查詢蘇茉家族知識庫時使用，例如：
- 老爺問關於蘇茉家族架構的問題
- 需要引用 SumoNoteBook 中的內容
- 需要檢索蘇茉的學習記錄

## 使用方式

### 查詢語法
```
/notebook-rag <查詢文字>
```

### 參數
- `<查詢文字>`: 要搜尋的問題或主題

### 範例
```
/notebook-rag 蘇茉家族多代理架構
/notebook-rag 工程師蘇茉的職責
/notebook-rag workspace 是什麼
```

## 運作流程

1. 接收查詢文字
2. 對查詢做 embedding（透過 Ollama `nomic-embed-text`）
3. 在 LanceDB `sumo_notebook` 表中做 cosine similarity 搜索
4. 返回 top-3 最相關的內容

## 輸出格式

```
🔍 查詢: "<用戶查詢>"

📚 相關內容:

[1] <檔案名稱> (相關度: 0.XXX)
---
<內容預覽（前 300 字）>
---

[2] <檔案名稱> (相關度: 0.XXX)
---
<內容預覽>
---
```

## 技術規格

- **Embedding 模型**: `nomic-embed-text` (768-dim)
- **向量資料庫**: LanceDB (`~/.openclaw/memory/lancedb-pro`)
- **表名**: `sumo_notebook`
- **索引內容**: SumoNoteBook 下所有 `.md` 檔案（117 個檔案，260 個 chunk）
- **搜尋方式**: Cosine distance
- **Top-K**: 預設 3 條結果

## 腳本位置

- 查詢腳本: `C:\butler_sumo\library\SumoNoteBook\scripts\query_notebook.mjs`
- 攝取腳本: `C:\butler_sumo\library\SumoNoteBook\scripts\ingest_notebook.mjs`

## 維護

### 更新索引
```bash
cd C:\butler_sumo\library\SumoNoteBook\scripts
node ingest_notebook.mjs --rebuild  # 全量重建
node ingest_notebook.mjs             # 增量更新
```

### 檢查狀態
```bash
# 確認 Ollama 運行
curl http://localhost:11434

# 確認 LanceDB 表
node -e "import('@lancedb/lancedb').then(async m => { const db = await m.connect('C:\\\\Users\\\\rayray\\\\.openclaw\\\\memory\\\\lancedb-pro'); console.log(await db.tableNames()); })"
```

## 限制

- 只能搜尋 SumoNoteBook 中的 `.md` 檔案
- 不包含 binary 檔案或非文字內容
- 結果預覽限制在 300 字（完整內容需手動開啟檔案）
- 查詢延遲約 2-5 秒（取決於網路和 Ollama 負載）
