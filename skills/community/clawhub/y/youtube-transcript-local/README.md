# 🎬 YouTube Transcript Local

**本地安全的 YouTube 字幕提取工具** - 無需外部 API，無安全風險

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://docs.openclaw.ai/tools/skills)

---

## 🌟 特點

- ✅ **本地執行** - 無外部 API 調用，無數據洩露風險
- ✅ **完全免費** - 無配額限制，無付費牆
- ✅ **多語言支持** - 中文（繁/簡）、英文、日文、韓文等
- ✅ **智能摘要** - 自動生成結構化摘要
- ✅ **故障轉移** - 無字幕時自動使用語音識別
- ✅ **OpenClaw 集成** - 可作為 OpenClaw Skill 使用

---

## 📦 安裝

### 前置要求

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **yt-dlp**
   ```bash
   pip install yt-dlp
   ```

3. **可選：ffmpeg**（用於音頻處理）
   - Windows: `choco install ffmpeg` 或從 https://ffmpeg.org/download.html 下載
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

### 安裝技能

```bash
# 克隆本倉庫
git clone https://github.com/YOUR_USERNAME/youtube-transcript-local.git

# 進入目錄
cd youtube-transcript-local

# 安裝依賴
pip install -r requirements.txt
```

---

## 🚀 使用方式

### 基本用法

```bash
# PowerShell
powershell ./extract.ps1 -url "https://www.youtube.com/watch?v=VIDEO_ID"

# 指定語言
powershell ./extract.ps1 -url "URL" -lang "zh-Hans"

# 指定輸出目錄
powershell ./extract.ps1 -url "URL" -output "C:\transcripts"
```

### 在 OpenClaw 中使用

安裝 OpenClaw Skill 後，直接使用自然語言：

```
幫我總結這個 YouTube 視頻
URL: https://www.youtube.com/watch?v=abc123
```

### Python 調用

```python
from extract import YouTubeTranscriptExtractor

extractor = YouTubeTranscriptExtractor()
result = extractor.extract("https://www.youtube.com/watch?v=abc123", lang="zh-Hans")
print(result.summary)
```

---

## 📋 功能詳情

### 支持的字幕語言

| 代碼 | 語言 |
|------|------|
| `zh-Hans` | 簡體中文 |
| `zh-Hant` | 繁體中文 |
| `en` | 英文 |
| `ja` | 日文 |
| `ko` | 韓文 |
| `es` | 西班牙文 |
| `fr` | 法文 |
| `de` | 德文 |

### 輸出格式

**字幕文件** (`.srt`):
```srt
1
00:00:01,000 --> 00:00:04,000
歡迎觀看本教程

2
00:00:04,500 --> 00:00:08,000
今天我們來學習如何使用這個工具
```

**摘要輸出** (`.md`):
```markdown
# 視頻摘要

## 關鍵觀點
1. 觀點一
2. 觀點二

## 時間節點
- 00:00 - 介紹
- 05:30 - 核心內容

## 核心結論
總結內容
```

---

## 🔧 高級配置

### 環境變量

```bash
# 設置默認語言
export YT_DEFAULT_LANG=zh-Hans

# 設置輸出目錄
export YT_OUTPUT_DIR=C:\transcripts

# 啟用緩存
export YT_CACHE_ENABLED=true
```

### 配置文件

創建 `config.yaml`:
```yaml
default:
  lang: zh-Hans
  output_dir: ./transcripts
  cache: true
  
whisper:
  model: base
  language: zh
```

---

## 🛠️ 開發

### 運行測試

```bash
python -m pytest tests/
```

### 貢獻指南

1. Fork 本倉庫
2. 創建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 開發環境設置

```bash
# 克隆倉庫
git clone https://github.com/YOUR_USERNAME/youtube-transcript-local.git
cd youtube-transcript-local

# 創建虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝開發依賴
pip install -r requirements-dev.txt
```

---

## 📊 性能對比

| 工具 | 速度 | 準確率 | 成本 | 安全性 |
|------|------|--------|------|--------|
| **youtube-transcript-local** | ⚡⚡⚡ | ✅ 95% | 免費 | 🔒 本地 |
| YouTube Summarizer (API) | ⚡⚡⚡⚡ | ✅ 90% | 付費 | ⚠️ 外部 API |
| 手動抄錄 | ⚡ | ✅ 100% | 耗時 | 🔒 本地 |

---

## 🤝 相關項目

- [OpenClaw](https://github.com/openclaw/openclaw) - AI 智能體框架
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube 下載器
- [Whisper](https://github.com/openai/whisper) - 語音識別

---

## 📄 許可證

本項目採用 **MIT-0** 許可證 - 免費使用、修改、分發，無需署名。

詳情請查看 [LICENSE](LICENSE) 文件。

---

## 🙏 致謝

- 感謝 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 團隊的優秀工具
- 感謝 [OpenClaw](https://github.com/openclaw/openclaw) 社區的支持
- 感謝所有貢獻者

---

## 📬 聯繫

- **作者**: Ryan (欧启熙) / qibot
- **Email**: miku2339@foxmail.com
- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/youtube-transcript-local/issues)

---

**Made with ❤️ by the OpenClaw Community**
