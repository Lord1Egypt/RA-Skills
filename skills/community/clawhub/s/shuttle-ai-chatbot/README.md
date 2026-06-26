# Shuttle AI Chatbot v2.0.1

直接調用本地 AI 服務的 `/chat_direct` API，無需瀏覽器自動化。支援單次查詢與批次執行。

## 安裝

```bash
clawhub install shuttle-ai-chatbot
```

## 使用

### 單次查詢
```bash
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

## 參數

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `query` | 單次查詢文字 | - |
| `batch` | 批次查詢檔案路徑（每行一筆） | - |
| `--url` | 本地 AI 服務 URL | `http://192.168.100.98:8888` |
| `--output` | 輸出格式：`json` 或 `text` | `json` |
| `--lang` | 回覆語言：`zh` 或 `en` | `zh` |

## 新功能（v2.0.1）

✅ **技能slug更名：** 從 `shuttle-qc-ai-chatbot` 改名為 `shuttle-ai-chatbot`
✅ **Session ID 優化：** 使用格式 `shuttle-cli-{隨機碼16}_{YYYYMMDD}`，方便追蹤當日所有查詢
✅ **API 直接調用：** 移除不穩定的瀏覽器自動化，查詢速度更快
✅ **更穩定：** 不依赖瀏覽器狀態，錯誤率大幅降低

## 注意事項

- 確保本地服務 `192.168.100.98:8888` 已啟動且可訪問
- `--timeout` 參數保留但無效（API 會自行控制超時）
- 回覆格式由後端決定，可能包含 markdown 表格

詳見 [SKILL.md](SKILL.md)。
