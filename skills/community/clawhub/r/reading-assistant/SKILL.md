---
name: reading-assistant
description: "個人閱讀助理：管理 epub 電子書圖書館、分章節摘要、追蹤閱讀進度。匯入 epub、查看閱讀清單、生成章節摘要、記錄進度。觸發詞：讀書、閱讀、書、小說、epub、圖書館、書單、閱讀清單、讀到哪、摘要、下一章、匯入書籍、繼續上次、推薦我讀什麼、reading list、book summary、chapter、library、import book。"
version: 1.0.0
user-invocable: true
metadata: {"openclaw": {"requires": {"bins": ["python3", "pip3"]}}, "emoji": "📚"}
---

# 📚 個人閱讀助理 (Reading Assistant)

管理 epub 電子書圖書館，分章節產生摘要，追蹤閱讀進度，提供閱讀建議。

---

## 系統架構

### 資料存放

本 Skill 使用兩層儲存：

**1. 本地檔案系統（主要）**
- 書庫根目錄：`~/.openclaw/workspace/reading-library/`
- 每本書一個子資料夾，內含 `manifest.json` + `chapters/` 目錄
- 閱讀進度檔：`~/.openclaw/workspace/reading-library/progress.json`

**2. Notion（可選，用於雲端同步）**
- 如果使用者有連接 Notion，可同步書籍資訊與摘要到 Notion 資料庫
- 未連接 Notion 時所有功能仍正常運作

### 進度追蹤檔 (progress.json) 格式

```json
{
  "books": {
    "<book_id>": {
      "title": "書名",
      "author": "作者",
      "total_chapters": 40,
      "current_chapter": 12,
      "status": "reading",
      "last_read_date": "2026-03-23",
      "added_date": "2026-03-20",
      "rating": null,
      "summaries": {
        "0": { "date": "2026-03-20", "summary": "..." },
        "1": { "date": "2026-03-21", "summary": "..." }
      }
    }
  }
}
```

---

## 功能模組

### 模組 1：匯入書籍 (Import Book)

**觸發**：使用者提供 epub 檔案路徑或說「匯入」「import」

**步驟**：

1. 確認 epub 檔案路徑存在
2. 安裝必要 Python 套件（如尚未安裝）：
   ```bash
   pip3 install ebooklib beautifulsoup4 lxml
   ```
3. 執行處理腳本：
   ```bash
   python3 ~/.openclaw/workspace/skills/reading-assistant/scripts/process_epub.py \
     "<epub檔案路徑>" \
     "~/.openclaw/workspace/reading-library/<book_id>"
   ```
   腳本會自動產生 `manifest.json` 和 `chapters/ch_000.txt ~ ch_NNN.txt`
4. 讀取 `manifest.json`，將書籍資訊寫入 `progress.json`
5. 回報匯入結果

**回報格式**：
```
✅ 匯入成功！

📕 書名：世界盡頭與冷酷仙境
👤 作者：村上春樹
📄 共 40 章（約 180,000 字）
⏱️ 預估總閱讀時間：6 小時
📊 狀態：未開始

輸入 /reading-assistant 或說「我的書單」查看圖書館。
```

### 模組 2：閱讀清單 (Reading List)

**觸發**：「書單」「閱讀清單」「我有哪些書」「reading list」

**步驟**：

1. 讀取 `~/.openclaw/workspace/reading-library/progress.json`
2. 列出所有書籍的進度

**回報格式**：
```
📚 你的閱讀圖書館

| # | 書名 | 作者 | 進度 | 狀態 |
|---|------|------|------|------|
| 1 | 世界盡頭與冷酷仙境 | 村上春樹 | 12/40 (30%) | 📖 閱讀中 |
| 2 | 挪威的森林 | 村上春樹 | 0/16 | 📋 未開始 |
| 3 | 人間失格 | 太宰治 | 4/4 (100%) | ✅ 已完成 |

💡 建議：你上次讀「世界盡頭與冷酷仙境」到第 12 章，要繼續嗎？
```

### 模組 3：閱讀章節摘要 (Chapter Summary)

**觸發**：「讀第 N 章」「摘要」「下一章」「繼續」「summary」

**步驟**：

1. 確定目標書籍和章節序號
   - 「下一章」或「繼續」→ 從 progress.json 找到 current_chapter + 1
   - 「讀第 5 章」→ 指定章節
   - 若只有一本在讀中的書，自動選擇；否則詢問
2. 讀取對應的章節文字檔：
   ```bash
   cat ~/.openclaw/workspace/reading-library/<book_id>/chapters/ch_<NNN>.txt
   ```
3. 將章節文字交給 LLM（即你自己），以下方結構產生摘要：

**摘要結構（嚴格遵循）**：

```
📖 《書名》— 第 N 章：章節標題

【章節摘要】
150-250 字概述本章主要內容和情節發展。

【關鍵人物】
• 角色名 — 本章中的行為與變化

【金句節錄】
1. 「原文句子」
2. 「原文句子」
（挑選 2-3 句值得記住的段落）

【延伸思考】
提出 1-2 個值得反思的問題。

【與前章連結】
簡述本章與前面章節的關聯。
```

4. 更新 progress.json：
   - `current_chapter` = 本次閱讀的章節序號
   - `last_read_date` = 今天日期
   - `status` = "reading"（如果讀完最後一章則改為 "completed"）
   - 將摘要存入 `summaries` 物件
5. 回報進度：
   ```
   📊 進度更新：13/40 章 (32.5%) | ⏱️ 本章約 8 分鐘
   💾 摘要已儲存
   ```

### 模組 4：進度查詢 (Progress Check)

**觸發**：「讀到哪」「進度」「上次讀到」「progress」

**步驟**：

1. 讀取 progress.json
2. 找出 status = "reading" 的書籍
3. 顯示最近閱讀紀錄

### 模組 5：定時推送（搭配 Cron）

本 Skill 可搭配 OpenClaw 的 cron job 實現每日自動閱讀提醒。

在 `~/.openclaw/cron/jobs.json` 中加入：
```json
{
  "reading-reminder": {
    "schedule": "0 8 * * *",
    "prompt": "查看我的閱讀進度，如果有正在讀的書，幫我摘要下一章。"
  }
}
```

這會在每天早上 8 點自動觸發，讀取下一章並推送摘要到你的通訊平台（WhatsApp / Telegram / LINE 等）。

---

## Notion 同步（可選）

如果使用者要求將資料同步到 Notion，建立以下資料庫：

### 閱讀圖書館
```sql
CREATE TABLE (
  "書名" TITLE,
  "作者" RICH_TEXT,
  "語言" SELECT('中文':blue, '英文':green, '日文':red),
  "總章數" NUMBER,
  "目前章節" NUMBER,
  "閱讀狀態" SELECT('📋 未開始':gray, '📖 閱讀中':blue, '✅ 已完成':green),
  "Book ID" RICH_TEXT,
  "加入日期" DATE
)
```

每次更新 progress.json 時，同步更新 Notion 記錄。

---

## 注意事項

- **章節辨識**：腳本以 epub 內的 HTML document 為單位切分，不一定完全對應原書章節。匯入後可查看 manifest.json 手動調整標題
- **DRM 限制**：受 DRM 保護的 epub 無法解析，需先移除 DRM
- **長章節**：超過 100,000 字的章節，摘要時會截取前 50,000 字處理
- **版權**：本工具用於個人閱讀管理，使用者應確保擁有合法取得的電子書

---

**Version**: 1.0.0  
**Last Updated**: 2026-03-23
