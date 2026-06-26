---
name: youtube-transcribe
description: 自动转录 YouTube 视频，生成带时间戳的文字稿
version: 1.0.0
author: Alex Bloomberg
tags: [youtube, transcribe, whisper, ai, subtitle]
---

# YouTube Transcriber Skill

自动转录 YouTube 视频，生成带时间戳的文字稿和结构化总结。

## 使用方法

```bash
# OpenClaw 中使用
/youtube-transcribe <URL> [language]

# 例子
/youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID"
/youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID" zh
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| URL | YouTube 视频链接 | 必填 |
| language | 语言代码 (zh/en/ja/ko/auto) | auto |

## 依赖

- Python >= 3.8.0
- yt-dlp
- faster-whisper

## 例子

```bash
# 自动检测语言
/youtube-transcribe "https://youtube.com/watch?v=jNQXAC9IVRw"

# 指定中文
/youtube-transcribe "https://youtube.com/watch?v=9uDH8z-HZKs" zh

# 指定英文
/youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID" en
```

## 输出示例

```
📺 URL: https://youtube.com/watch?v=VIDEO_ID
🌐 Language: zh

[1/3] 下载音频...
✅ 下载成功

[2/3] 转录中...
✅ 转录完成！

[3/3] 生成总结...
============================================================
# 视频转录总结

**URL:** https://youtube.com/watch?v=VIDEO_ID
**语言:** zh

## 转录内容
[0.00s -> 3.00s] 大家好...
[3.00s -> 5.00s] 今天我们来...
============================================================
```
