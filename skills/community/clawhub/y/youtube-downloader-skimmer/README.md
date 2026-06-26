# YouTube Video Downloader & Skimmer

[README](README.md)

**技能**：`youtube-downloader-skimmer`

## 快速开始

### 基础用法
```bash
openclaw skill youtube-downloader-skimmer "https://www.youtube.com/watch?v=-vwHldNaGPI"
```

### 高级用法
```bash
# 下载为 MP3
openclaw skill youtube-downloader-skimmer "URL" --output-format mp3

# 指定质量
openclaw skill youtube-downloader-skimmer "URL" --quality 720p

# 不删除原始文件
openclaw skill youtube-downloader-skimmer "URL" --delete-raw false

# 发送到 Telegram
openclaw skill youtube-downloader-skimmer "URL" --send-to telegram
```

## 功能特性

- ✅ 自动下载 YouTube 视频
- ✅ 智能章节分割
- ✅ 快速剪辑（不重新编码）
- ✅ 支持 MP4/MP3 格式
- ✅ 多质量选项
- ✅ 自动发送到 QQ/Telegram
- ✅ 可选删除原始文件

## 依赖

- Python 3.x
- yt-dlp (`pip install yt-dlp`)
- ffmpeg

## 输出示例

```
clip_01_Introduction.mp4 (2.9MB)
clip_02_Sora_2.mp4 (6.2MB)
clip_03_Kling_2.6.mp4 (5.6MB)
clip_04_Wan_2.6.mp4 (6.0MB)
clip_05_Seedance_1.5_Pro.mp4 (5.9MB)
clip_06_Google_Veo_3.mp4 (5.6MB)
clip_07_Best_All-in-One_Platform.mp4 (5.8MB)
clip_08_Conclusion.mp4 (7.9MB)
```

---

*版本：1.0.0 | 创建日期：2026-04-04*
