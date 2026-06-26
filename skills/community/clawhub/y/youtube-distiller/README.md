# YouTube 知識蒸餾器

## 功能
將 YouTube/Bilibili 影片轉化為結構化知識文章

## 位置
`C:\butler_sumo\developing_tools\youtube-distiller\youtube_distiller.py`

## 使用方式

### 基本用法
```bash
python youtube_distiller.py "URL"
```

### 指定風格
```bash
python youtube_distiller.py "URL" --style investment
```

### 觸發方式（蘇茉）
```
蘇茉，執行知識蒸餾 https://youtu.be/xxx --style investment
```

## 支援的風格

| 風格 | 說明 |
|------|------|
| `standard` | 標準摘要 |
| `academic` | 學術筆記格式 |
| `actions` | 行動清單 |
| `news` | 新聞快訊格式 |
| **`investment`** | **投資分析格式** |
| `podcast` | 播客訪談格式 |
| `eli5` | 通俗易懂解釋 |
| `bullets` | 極簡子彈格式 |

## 依賴
- yt-dlp.exe（已存在於 `C:\butler_sumo\tools\youtube-knowledge\`）
- MiniMax API Key（從環境變數 MINIMAX_API_KEY 讀取）

## 輸出
- 預設輸出目錄：`C:\butler_sumo\temp\youtube-distiller\`
- 格式：UTF-8 純文字檔

## 狀態
- 目前版本：v2
- 狀態：開發中
- 下一步：等待品管蘇茉檢查後移至正式 tools 目錄
