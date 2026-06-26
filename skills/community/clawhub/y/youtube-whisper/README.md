# YouTube Whisper / YouTube Whisper 語音轉文字

**Version 版本**: 1.2.2

### 新功能 (1.2.1)
- 超過 100 字元自動提示用戶查看檔案

### 使用情境

| 情境 | Agent 怎麼做 |
|------|-------------|
| 用戶說「給我文字」 | 直接傳文字給用戶 |
| 用戶說「給我總結」 | 先轉文字，再自動總結給用戶 |

> 腳本只負責轉文字，是否要總結由 Agent 決定

[English](#english) | [繁體中文](#繁體中文)

---

## English

### Description

Download YouTube videos and transcribe audio using local Whisper. Best for videos without subtitles.

### New Feature (1.2.0)
- If text > 100 characters, prompt user to view attachment

### Usage Scenarios

| Scenario | What Agent Does |
|----------|-----------------|
| User says "give me text" | Send text directly |
| User says "summarize" | Transcribe first, then summarize |

> Script only handles transcription. Whether to summarize is decided by Agent.
- **Smart subtitle detection**: Extract if available, otherwise use Whisper
- Local Whisper transcription (no API needed)
- Default: Traditional Chinese output
- Multiple Whisper models support

### Smart Logic

1. **Check for subtitles** first
2. **Has subtitles** → Extract directly (fast!)
3. **No subtitles** → Use Whisper (slower but works)

### Hardware Requirements

| Item | Minimum | Recommended |
|------|---------|-------------|
| RAM | 4 GB | 8 GB+ |
| Storage | 1 GB | 5 GB+ |
| CPU | Any | Apple Silicon M series |
| GPU | None | Yes (faster transcription) |

**Note**: Transcription is resource-intensive. Faster hardware = faster transcription.

### Test Environment

| Item | Specification |
|------|---------------|
| Host | Mac mini M4 |
| RAM | 16 GB |
| Model | Whisper small |
| Video Duration | 5:55 |
| Transcription Time | ~3-5 minutes |
| Output | Traditional Chinese text |

### Requirements

```bash
# Install dependencies
brew install yt-dlp ffmpeg

# Install Whisper
pip3 install openai-whisper

# Or use openai-whisper skill
clawhub install openai-whisper
```

### Usage

```bash
# Basic transcription
./scripts/youtube-whisper.sh "https://www.youtube.com/watch?v=VIDEO_ID"

# With output file
./scripts/youtube-whisper.sh "URL" "output.txt"

# With specific model
./scripts/youtube-whisper.sh "URL" "output.txt" "small"
```

### Model Options

| Model | Speed | Accuracy |
|-------|-------|----------|
| tiny | Fastest | Lower |
| base | Fast | Medium |
| **small** | Medium | Good |
| medium | Slow | Better |
| large | Slowest | Best |

### Video Limits

| Limit | Value |
|-------|-------|
| Max Duration | 30 minutes |
| Max File Size | 1 GB |
| Auto Check | Yes |

> Note: Will ask if you want to continue when exceeding limits

### Author

Kuanlin

---

## 繁體中文

### 說明

下載 YouTube 影片並使用本地 Whisper 進行語音轉文字。最適合沒有字幕的影片。

### 功能

- 下載 YouTube 影片音訊
- **智慧偵測字幕**：有字幕直接擷取，無字幕才用 Whisper
- 本地 Whisper 轉錄 (無需 API)
- 預設：繁體中文輸出
- 支援多種 Whisper 模型

### 智慧邏輯

1. **先檢查字幕**
2. **有字幕** → 直接擷取 (快!)
3. **無字幕** → 用 Whisper (慢但可行)

### 硬體需求

| 項目 | 最低需求 | 建議需求 |
|------|----------|----------|
| 記憶體 | 4 GB | 8 GB+ |
| 儲存空間 | 1 GB | 5 GB+ |
| CPU | 任意 | Apple Silicon M 系列 |
| GPU | 無 | 有 (加速轉錄) |

**注意**：轉錄是非常耗費資源的任務，硬體越強速度越快。

### 測試環境

| 項目 | 規格 |
|------|------|
| 主機 | Mac mini M4 |
| 記憶體 | 16 GB |
| 模型 | Whisper small |
| 影片時長 | 5:55 |
| 轉錄時間 | 約 3-5 分鐘 |
| 輸出 | 繁體中文文字檔 |

### 需求

```bash
# 安裝依賴
brew install yt-dlp ffmpeg

# 安裝 Whisper
pip3 install openai-whisper

# 或使用 openai-whisper 技能
clawhub install openai-whisper
```

### 使用方式

```bash
# 基本轉錄
./scripts/youtube-whisper.sh "https://www.youtube.com/watch?v=VIDEO_ID"

# 指定輸出檔案
./scripts/youtube-whisper.sh "網址" "輸出.txt"

# 指定模型
./scripts/youtube-whisper.sh "網址" "輸出.txt" "small"
```

### 模型選項

| 模型 | 速度 | 準確度 |
|------|------|--------|
| tiny | 最快 | 較低 |
| base | 快 | 中等 |
| **small** | 中等 | 良好 |
| medium | 慢 | 較高 |
| large | 最慢 | 最高 |

### 影片限制

| 限制 | 值 |
|------|-----|
| 最長時長 | 30 分鐘 |
| 最大檔案 | 1 GB |
| 自動檢測 | 是 |

> 注意：超過限制會詢問是否繼續

### 作者

Kuanlin

---

## License / 授權

MIT
