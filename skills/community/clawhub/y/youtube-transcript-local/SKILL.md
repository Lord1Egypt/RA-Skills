# YouTube Transcript (本地安全版)

**版本**: 1.0.0 (2026-03-23)
**作者**: Ryan (欧启熙) / qibot
**許可證**: MIT-0
**安全狀態**: ✅ 無 VirusTotal 標記（本地執行）
**GitHub**: https://github.com/miku233333/youtube-transcript-local
**ClawHub**: 已發布

---

## 📋 技能描述

使用本地安裝的 `yt-dlp` 工具提取 YouTube 視頻字幕，無需外部 API，無安全風險。

**優勢**：
- ✅ 本地執行，無外部 API 調用
- ✅ 無 VirusTotal 標記
- ✅ 支持自動生成字幕
- ✅ 支持多語言（中文/英文/日文等）
- ✅ 免費，無配額限制

---

## 🛠️ 使用方式

### 基本用法

```
提取 YouTube 視頻字幕並總結
URL: https://www.youtube.com/watch?v=VIDEO_ID
語言：en（或 zh-Hans, ja, ko 等）
```

### 高階用法

```
1. 提取字幕 → 保存為文本文件
2. 使用 summarize 技能生成摘要
3. 使用 tesseract-ocr 識別無字幕視頻（OCR）
```

---

## 🔧 技術實現

### 依賴工具

- **yt-dlp**: `pip install yt-dlp` (已安裝)
- **Python**: Python 3.8+
- **ffmpeg**: 用於音頻處理（可選）

### 執行流程

```powershell
# 1. 提取字幕（英文）
yt-dlp --write-sub --sub-lang en --skip-download --convert-subs srt -o "%TEMP%\yt-sub" "VIDEO_URL"

# 2. 提取字幕（中文）
yt-dlp --write-sub --sub-lang zh-Hans --skip-download --convert-subs srt -o "%TEMP%\yt-sub" "VIDEO_URL"

# 3. 無字幕時提取音頻並轉文字
yt-dlp --extract-audio --audio-format mp3 -o "%TEMP%\yt-audio" "VIDEO_URL"
# 然後用 Whisper 或 Tesseract OCR 轉文字
```

---

## 📝 使用示例

### 示例 1：技術教程視頻

**用戶**: 幫我總結這個 YouTube 視頻
**URL**: https://www.youtube.com/watch?v=abc123

**執行步驟**:
1. 使用 yt-dlp 提取英文字幕
2. 使用 summarize 生成結構化摘要
3. 返回：關鍵觀點 + 時間節點 + 核心結論

### 示例 2：中文視頻

**用戶**: 這個視頻講了什麼？
**URL**: https://www.youtube.com/watch?v=xyz789

**執行步驟**:
1. 優先提取中文字幕
2. 如果無中字，提取英文字幕 + 翻譯
3. 生成中文摘要

---

## ⚠️ 注意事項

1. **網絡要求**: 需要能訪問 YouTube
2. **字幕可用性**: 部分視頻無字幕（需 OCR 或音頻轉文字）
3. **版權**: 僅供學習研究使用

---

## 🔄 故障轉移方案

| 情況 | 方案 |
|------|------|
| 無字幕 | 使用 whisper 語音轉文字 |
| 無法訪問 YouTube | 使用 browser 工具 + 截圖 OCR |
| 長視頻 (>1 小時) | 分段提取 + 合併摘要 |

---

## 📚 相關技能

- **summarize**: 內容摘要
- **tesseract-ocr**: OCR 文字識別
- **video-frames**: 視頻幀提取
- **sandwrap**: 安全包裹運行

---

**最後更新**: 2026-03-23
**測試狀態**: 🟡 待測試
