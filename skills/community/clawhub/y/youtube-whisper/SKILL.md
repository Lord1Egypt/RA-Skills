---
name: youtube-whisper
description: YouTube影片一鍵轉文字！自動下載影片並用AI轉成中文/英文字幕，沒有字幕的影片也能用。
---

# YouTube 影片轉文字神器 🎬→📝

## 這能做什麼？

✅ 任何 YouTube 影片轉成文字  
✅ 沒有字幕的影片也可以  
✅ 自動偵測語言 (中/英/日/韓)  
✅ 支援長影片  
✅ 支援 `--force` 參數跳過記憶體檢查

## 使用情境

- 學習國外教學影片
- 保存喜歡的演講
- 做成文字筆記
- 製作字幕檔

## 回覆格式

回覆會包含以下資訊：

```
📺 影片標題
⏱️ 處理時間: X分X秒
📝 來源: [字幕檔/Whisper轉錄]
---
[轉錄文字內容]
```

## 硬體需求

| 項目 | 最低需求 | 建議需求 |
|------|----------|----------|
| 記憶體 | 4 GB | 8 GB+ |
| 儲存空間 | 1 GB | 5 GB+ |
| CPU | 任意 | Apple Silicon M 系列 |

## 測試環境

| 項目 | 規格 |
|------|------|
| 主機 | Mac mini M4 |
| 記憶體 | 16 GB |
| 模型 | Whisper small |
| 影片時長 | 5:55 |
| 轉錄時間 | 約 3-5 分鐘 |

## 使用方式

```bash
# 基本轉錄
youtube-whisper "https://www.youtube.com/watch?v=VIDEO_ID"

# 指定輸出檔案
youtube-whisper "URL" "output.txt"

# 指定模型 (tiny, base, small, medium, large)
youtube-whisper "URL" "output.txt" "small"

# 強制執行（跳過記憶體檢查）
youtube-whisper "URL" "output.txt" "tiny" --force
```

## 可用模型

| 模型 | 記憶體需求 | 說明 |
|------|------------|------|
| tiny | ~39 MB | 最輕量，適合記憶體不足時 |
| base | ~74 MB | 輕量 |
| small | ~244 MB | 平衡（預設）|
| medium | ~768 MB | 較準確 |
| large | ~1550 MB | 最高準確度 |

## 需求

- yt-dlp: `brew install yt-dlp`
- Whisper: `pip3 install openai-whisper`
- ffmpeg: `brew install ffmpeg`

## 輸出

轉錄文字檔案 (Transcript text file).

## 備註

- 影片會下載到 /tmp 並在轉錄後刪除
- 預設模型: small (速度與準確度的最佳平衡)
- 較大的模型 (medium, large) 較慢但更準確
- 使用 `--force` 參數可跳過記憶體檢查，適合記憶體不足時使用 tiny 模型

## 作者

Kuanlin
