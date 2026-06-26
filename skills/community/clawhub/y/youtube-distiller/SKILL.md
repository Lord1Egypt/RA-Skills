# YouTube Distiller - YouTube 知識蒸餾器

> 版本：2.0.0
> 用途：將 YouTube/Bilibili 影片轉化為結構化知識文章

## 功能

- **自動下載字幕**：從 YouTube/Bilibili 取得字幕
- **AI 智慧摘要**：使用 MiniMax API 總結內容
- **多風格輸出**：支援標準、學術、投資、新聞等格式

## 使用方式

```
python youtube_distiller.py "URL" --style standard
```

## 觸發方式（蘇茉）

```
蘇茉，執行知識蒸餾 https://youtu.be/xxx --style investment
```

## 風格選項

| 風格 | 說明 |
|------|------|
| standard | 標準摘要 |
| academic | 學術筆記格式 |
| actions | 行動清單 |
| news | 新聞快訊格式 |
| investment | 投資分析格式 |
| podcast | 播客訪談格式 |
| eli5 | 通俗易懂解釋 |
| bullets | 極簡子彈格式 |

## 檔案位置

`C:\butler_sumo\tools\youtube-distiller\`