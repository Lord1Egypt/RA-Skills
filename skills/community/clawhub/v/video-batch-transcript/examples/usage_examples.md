# 使用示例

## 示例 1: YouTube 教程系列

```bash
# 下载整个播放列表并转录
python scripts/batch_transcript.py \
  --url "https://www.youtube.com/playlist?list=PLxxx" \
  --output-dir "~/youtube-ml-course" \
  --device cuda \
  --model medium

# 使用 cookies 避免 403 错误
python scripts/batch_transcript.py \
  --url "https://www.youtube.com/playlist?list=PLxxx" \
  --cookies-from-browser chrome
```

## 示例 2: B 站 UP 主合集

```bash
# 下载整个合集
python scripts/batch_transcript.py \
  --url "https://space.bilibili.com/123/channel/collectiondetail?sid=456" \
  --output-dir "~/bilibili-ai-series" \
  --episodes "1-20"

# 下载 UP 主频道所有视频
python scripts/batch_transcript.py \
  --url "https://space.bilibili.com/123/video" \
  --output-dir "~/bilibili-uploader"
```

## 示例 3: 抖音合集

```bash
# 抖音合集（需要 cookies）
python scripts/batch_transcript.py \
  --url "https://www.douyin.com/collection/xxx" \
  --output-dir "~/douyin-notes" \
  --cookies-from-browser chrome
```

## 示例 4: Twitch 频道视频

```bash
# 下载 Twitch 频道所有视频
python scripts/batch_transcript.py \
  --url "https://www.twitch.tv/xxx/videos" \
  --output-dir "~/twitch-vods" \
  --language en

# 指定集数
python scripts/batch_transcript.py \
  --url "https://www.twitch.tv/xxx/videos" \
  --episodes "1-10"
```

## 示例 5: Vimeo 合集

```bash
# Vimeo 专辑
python scripts/batch_transcript.py \
  --url "https://vimeo.com/album/xxx" \
  --output-dir "~/vimeo-collection"
```

## 示例 6: Twitter/X 视频

```bash
# 下载 Twitter 视频
python scripts/batch_transcript.py \
  --url "https://twitter.com/xxx/status/123" \
  --output-dir "~/twitter-videos"
```

## 示例 7: Instagram Reels

```bash
# Instagram Reels（需要 cookies）
python scripts/batch_transcript.py \
  --url "https://www.instagram.com/reel/xxx/" \
  --output-dir "~/instagram-reels" \
  --cookies-from-browser chrome
```

## 示例 8: 教育平台

```bash
# Coursera 课程（需要登录）
python scripts/batch_transcript.py \
  --url "https://www.coursera.org/learn/xxx" \
  --output-dir "~/coursera-notes" \
  --cookies "cookies/coursera.txt"

# TED 演讲
python scripts/batch_transcript.py \
  --url "https://www.ted.com/talks/xxx" \
  --output-dir "~/ted-talks" \
  --language en
```

## 示例 9: 音频平台

```bash
# SoundCloud 播放列表
python scripts/batch_transcript.py \
  --url "https://soundcloud.com/xxx/sets/yyy" \
  --output-dir "~/soundcloud-playlist"
```

## 示例 10: 多平台混合处理

```bash
#!/bin/bash
# process_all.sh - 批量处理多个平台的视频

# YouTube
python scripts/batch_transcript.py \
  --url "https://youtube.com/playlist?list=xxx" \
  --output-dir "~/notes/youtube" \
  --cookies-from-browser chrome

# B 站
python scripts/batch_transcript.py \
  --url "https://space.bilibili.com/xxx/collectiondetail?sid=xxx" \
  --output-dir "~/notes/bilibili"

# Vimeo
python scripts/batch_transcript.py \
  --url "https://vimeo.com/album/xxx" \
  --output-dir "~/notes/vimeo"

# Twitch
python scripts/batch_transcript.py \
  --url "https://twitch.tv/xxx/videos" \
  --output-dir "~/notes/twitch" \
  --language en

echo "所有视频处理完成！"
```

## 示例 11: GPU 加速 + 自定义术语

```bash
# 使用 GPU 加速 + 医学领域术语表
python scripts/batch_transcript.py \
  --url "https://youtube.com/playlist?list=xxx" \
  --output-dir "~/medical-course" \
  --device cuda \
  --model medium \
  --terminology "config/medical-terms.json" \
  --workers 2
```

## 示例 12: 断点续传

```bash
# 自动续传（默认行为）
python scripts/batch_transcript.py \
  --url "https://youtube.com/playlist?list=xxx"

# 强制重新处理所有视频
python scripts/batch_transcript.py \
  --url "https://youtube.com/playlist?list=xxx" \
  --no-resume
```

## 示例 13: 并行处理

```bash
# 使用 4 个进程并行处理（需要足够内存）
python scripts/batch_transcript.py \
  --url "https://youtube.com/playlist?list=xxx" \
  --workers 4

# 注意：每个进程约需 1-2GB 内存
```

## 示例 14: 低配置设备

```bash
# CPU 模式 + 最小模型（适合无 GPU 或显存<2GB）
python scripts/batch_transcript.py \
  --url "https://youtube.com/playlist?list=xxx" \
  --device cpu \
  --model tiny \
  --workers 1
```

## 示例 15: 指定语言

```bash
# 强制使用英文转录
python scripts/batch_transcript.py \
  --url "https://youtube.com/playlist?list=xxx" \
  --language en

# 强制使用中文
python scripts/batch_transcript.py \
  --url "https://bilibili.com/video/xxx" \
  --language zh

# 自动检测（默认）
python scripts/batch_transcript.py \
  --url "xxx" \
  --language auto
```

## 输出示例

处理完成后，目录结构如下：

```
~/video-notes/
├── youtube_机器学习教程/
│   ├── 001_什么是机器学习/
│   │   ├── audio.mp3          # 音频文件
│   │   ├── transcript.txt     # 原始转录
│   │   ├── notes.md          # 结构化笔记
│   │   └── metadata.json      # 元数据
│   ├── 002_神经网络基础/
│   │   └── ...
│   ├── 合集汇总.md            # 完整汇总
│   └── metadata.json          # 合集元数据
├── bilibili_AI 入门/
│   └── ...
└── twitch_游戏直播/
    └── ...
```

## 常见问题

### Q: YouTube 下载 403 错误？
A: 使用 `--cookies-from-browser chrome` 参数。

### Q: 抖音无法下载？
A: 需要提供 cookies，使用 `--cookies-from-browser chrome`。

### Q: 如何处理 Netflix 视频？
A: 1. 登录 Netflix
     2. 使用浏览器扩展导出 cookies
     3. 使用 `--cookies "netflix.txt"` 参数

### Q: 转录速度慢？
A: 使用 GPU 加速 (`--device cuda`) 或更小的模型 (`--model tiny`)。

### Q: 内存不足？
A: 使用更小的模型，或减少 `--workers` 数量。

### Q: 如何自定义笔记格式？
A: 修改 `scripts/batch_transcript.py` 中的 `generate_notes()` 方法。

### Q: 支持哪些音频格式输出？
A: 默认 MP3，可修改 `video_format` 参数支持其他格式。

### Q: 如何处理付费内容？
A: 需要提供对应网站的 cookies 文件，确保账号有访问权限。
