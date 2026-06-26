# YouTube 知識蒸餾器開發日誌

## 更新時間：2026-03-10

---

## 開發目標
將 YouTube/Bilibili 影片轉化為結構化知識文章

---

## 流程 1：下載字幕 ✅ 已完成

### 使用工具
- **yt-dlp** - YouTube/Bilibili 影片下載工具
- 路徑：`C:\butler_sumo\tools\youtube-knowledge\yt-dlp.exe`

### 命令
```bash
yt-dlp --write-subs --write-auto-subs --sub-lang en --skip-download -o C:\temp\test_video "URL"
```

### 結果
- 字幕下載成功
- 輸出格式：VTT (WebVTT)

---

## 流程 2：語音轉文字 ✅ 已完成

### 使用工具
- **faster-whisper** - 已在 sumo_voice 中使用

### 安裝狀態
```
Name: faster-whisper
Version: 1.2.1
```

### 模型選擇
- **tiny** - 最快，適合測試
- **small** - 較精準
- **medium** - 最精準，但較慢

### 運作邏輯
1. 有字幕 → 直接提取字幕文字
2. 無字幕 → 下載音頻 + Whisper 轉寫

---

## 流程 3：AI 摘要 ✅ 已完成

### 使用工具
- **MiniMax M2.5 API**
- API Key：`sk-cp-kL-C0rYerwRmd7yrI52akm6WfDLabsz3HfO7tQB2K1488-cwzmJ4rQNn-VcndSwEEy9EBxRlEFbZ8DhbYl_rOZ3uHuI3WI0vFysdtLfxi3sW2eLY`
-VFHciOd API 網址：`https://api.minimax.io/v1/text/chatcompletion_v2`

### 支援的風格

| 風格 | 說明 |
|------|------|
| `standard` | 標準摘要 |
| `academic` | 學術筆記格式 |
| `actions` | 行動清單 |
| `news` | 新聞快訊格式 |
| `investment` | 投資分析格式 |
| `podcast` | 播客訪談格式 |
| `eli5` | 通俗易懂解釋 |
| `bullets` | 極簡子彈格式 |

---

## 觸發方式

### 關鍵字觸發
當老爺說「**執行知識蒸餾**」加上 YouTube 網址時，蘇茉會自動執行。

### 範例
```
蘇茉，執行知識蒸餾 https://youtu.be/xxx --style investment
```

### 支援的參數
- `URL` - YouTube/Bilibili 影片網址（必要）
- `--style` - 摘要風格（預設：standard）
- `--no-whisper` - 只用字幕，不使用 Whisper 轉寫
- `--model` - Whisper 模型大小（預設：tiny）

---

## 腳本位置

| 檔案 | 位置 |
|------|------|
| 主腳本 | `C:\tools\butler_sumou_tools\youtube-knowledge.py` |
| 輸出目錄 | `C:\temp\` |

---

## 使用方式

```bash
# 基本用法
python C:\tools\butler_sumou_tools\youtube-knowledge.py "URL"

# 指定風格（股市財金分析）
python C:\tools\butler_sumou_tools\youtube-knowledge.py "URL" --style investment

# 只用字幕，不使用 Whisper
python C:\tools\butler_sumou_tools\youtube-knowledge.py "URL" --no-whisper

# 指定 Whisper 模型
python C:\tools\butler_sumou_tools\youtube-knowledge.py "URL" --model small

# 指定輸出檔案
python C:\tools\butler_sumou_tools\youtube-knowledge.py "URL" -o my_output.txt
```

---

## 測試結果

### 測試影片
- **影片**：Rick Astley - Never Gonna Give You Up
- **網址**：https://www.youtube.com/watch?v=dQw4w9WgXcQ
- **風格**：standard
- **結果**：✅ 成功

### 測試影片 2（股市財金分析）
- **影片**：中東衝突分析
- **網址**：https://youtu.be/GqBtxVrY_SM
- **風格**：investment
- **結果**：✅ 成功
- **輸出**：C:\temp\youtube_output_summary.txt

---

## 問題與解決

### 問題 1：API Key 無效
- **原因**：使用了舊的 API Key
- **解決**：更新為正確的 Key

### 問題 2：API 網址錯誤
- **原因**：使用了 api.minimax.chat（錯誤）
- **解決**：改用 api.minimax.io

---

## 未來改進

- [ ] 設定關鍵字觸發（蘇茉，執行知識蒸餾）
- [ ] 支援更多 AI Provider（OpenAI、Google Gemini）
- [ ] 自動清理 C:\temp 輸出檔案

---

*持續開發中...*
