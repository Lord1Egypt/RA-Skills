# shuttle-ai-chatbot Skill v2.0.1

## 📖 概述

直接調用本地 AI 服務的 `/chat_direct` API，無需瀏覽器自動化。支援單次查詢與批次執行，速度更快、更穩定。

## ✨ 功能

- 🚀 **直接 API 調用**：無瀏覽器自動化，回應速度更快
- 📝 輸入任意查詢文字（產品型號、問題等）
- 📋 提取完整回應內容（結構化資料）
- 🚀 支援批次查詢（多個指令一次執行）
- 📊 輸出結果為 JSON 或純文字
- 🔄 支援產品比較（e.g., "DL30N vs DL40N"）
- 🆔 **Session ID 優化**：使用日期格式 `shuttle-cli-YYYYMMDD`，方便追蹤

## 🛠️ 使用方式

### CLI 指令

```bash
# 單次查詢
shuttle-ai-chatbot query "SB860R8 spec" --output text
shuttle-ai-chatbot query "DL30N vs DL40N"  # 產品比較
```

### 批次查詢
```bash
shuttle-ai-chatbot batch queries.txt --output json
```

### 查詢列表檔案內容（queries.txt）
```txt
DL30N
DL40N
SB860R8
P55U
```

## 📥 參數

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `query` | 單次查詢文字 | - |
| `batch` | 批次查詢檔案路徑（每行一筆） | - |
| `--url` | 本地 AI 服務 URL | `http://192.168.100.98:8888` |
| `--output` | 輸出格式：`json` 或 `text` | `json` |
| `--lang` | 回覆語言：`zh` 或 `en` | `zh` |

## 📤 輸出格式

### JSON（預設）
```json
{
  "query": "p55u?",
  "response": "產品規格表內容...",
  "url": "http://192.168.100.98:8888",
  "elapsed": "2.34s",
  "timestamp": "2026-03-18T11:30:00+08:00",
  "sessionId": "shuttle-cli-20260318"
}
```

### Text
```
🔍 查詢：p55u?
🆔 Session：shuttle-cli-20260318
⏱️  耗時：2.34s
📅 時間：2026-03-18T11:30:00+08:00

📋 回應內容：
產品規格表內容...
```

## 🔧 工作原理

1. 生成 session ID：`shuttle-cli-YYYYMMDD`（當天日期）
2. 構造 JSON 請求：`{ question, session_id, lang }`
3. 使用 `curl` 發送 POST 到 `{url}/chat_direct`
4. 解析 JSON 回應，提取 `result` 或 `response` 欄位
5. 輸出結果（JSON 或純文字）

## 🧩 相依性

- 本地 AI 服務 running on `192.168.100.98:8888`
- `curl` 命令（系統內建）
- Node.js 環境（執行 CLI）

## 📦 安裝

從 ClawHub 安裝：
```bash
clawhub install shuttle-ai-chatbot
```

或手動複製到 `~/.openclaw/workspace/skills/` 目錄。

## 📌 使用範例

### 基本產品查詢
```bash
shuttle-ai-chatbot query "DL30N spec"
shuttle-ai-chatbot query "P55U?"
```

### 產品系列比較
```bash
shuttle-ai-chatbot query "Compare DL30N and DL40N"
shuttle-ai-chatbot query "DL30N vs DL40N" --output text
```

### 批次查詢（從檔案）
建立 `queries.txt`：
```txt
DL30N
DL40N
SB860R8
P55U
```

執行：
```bash
shuttle-ai-chatbot batch queries.txt --output json > results.json
```

### 指定不同服務 URL
```bash
shuttle-ai-chatbot query "p25n" --url http://10.0.0.5:8888
```

### 英文回覆
```bash
shuttle-ai-chatbot query "NA20H specifications" --lang en
```

## ⚠️ 注意事項

- 確保本地服務（預設 `192.168.100.98:8888`）已啟動且可訪問
- 若服務關閉或网络不通，會返回錯誤訊息
- 每次查詢使用當天日期作為 session ID，便於後端日誌追蹤

## 📄 變更歷史

### v2.0.1 (2026-03-19)
- **技能slug更名：** 從 `shuttle-qc-ai-chatbot` 改名為 `shuttle-ai-chatbot`
- **發布至 ClawHub：** 新版技能已上架

### v2.0.0 (2026-03-18)
- **重大改動：** 移除瀏覽器自動化，改用直接 API 調用
- **Session ID 優化：** 使用 `shuttle-cli-YYYYMMDD` 格式
- **性能提升：** 查詢速度更快（無需啟動瀏覽器）
- **穩定性增強：** 不再依賴瀏覽器狀態，錯誤率大幅降低
- **參數簡化：** 移除 `--timeout`、`--headless` 等瀏覽器相關參數
- **新增 `--lang` 參數：** 可指定回覆語言（zh/en）
- **URL 預設值變更：** 從 `/v1` 改為根路徑 `/`

### v1.0.2 (2026-03-17)
- **安全性限制：** 新增 URL 驗證，僅允許本地端服務（localhost、私有 IP）
- **穩定性增強：** 改寫回應等待邏輯，確保答案產生後才返回結果
- **錯誤處理：** 統一錯誤訊息，禁止外部網路搜尋

### v1.0.1 (2026-03-17)
- **文件更新：** 新增產品比較使用範例
- **skill.json：** 新增 comparison tag，提升版本號
- **README：** 新增進階用法、產品比較範例、注意事項

### v1.0.0 (2026-03-17)
- 初版發佈（瀏覽器自動化版本）
- 支援單次與批次查詢
- 自動化瀏覽器操作
- JSON/Text 輸出格式

---

**作者：** Shuttle AI
**來源：** https://clawhub.com/skills/shuttle-ai-chatbot
