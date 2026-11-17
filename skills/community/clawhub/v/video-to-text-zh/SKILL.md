---
name: video-to-text
description: 提取视频语音并转成中文文字稿。当用户给出抖音、B站（bilibili/b23.tv）、YouTube、快手、视频号等常见视频网站的链接，想要"提取视频里说话的内容""视频转文字""语音转文字""视频字幕提取"时，必须使用本技能。即使用户只发了一个视频链接没说要做什么，也应主动用本技能识别并转写其中的说话内容。
---

# 视频语音转文字

把常见视频网站的链接一键转成中文文字稿（带时间轴 + 纯文字两版）。

## 支持的站点与下载方式

| 站点 | 链接形式 | 下载方式 |
|---|---|---|
| 抖音 | v.douyin.com 短链 / douyin.com/video/ID | yt-dlp 会失败（需要新鲜 Cookie），**自动回退无头 Chromium 捕获** |
| B站 | b23.tv 短链 / bilibili.com/video/BV号 | yt-dlp 直接下载 |
| YouTube | youtu.be / youtube.com/watch | yt-dlp 直接下载 |
| 快手、其他 | 短链或长链 | 先 yt-dlp，失败后 Chromium 回退 |

## 用法

```bash
python <skill目录>/scripts/video_to_text.py "<视频链接>" [输出目录] [--model small] [--keep-media]
```

- 输出目录缺省为当前目录，产出 `文字稿.txt` 和 `meta.json`（含标题、站点信息）
- `--model`：whisper 模型大小，`base` 更快、`small`（默认）准确率更高、`medium` 更准但更慢
- `--keep-media`：保留下载的音视频中间文件（默认转写后清理）
- 直接管道输出文字稿，同时在回复中完整引用给用户

## 内部流程（脚本已自动完成，仅在排错时需要了解）

1. 展开短链接（跟随 302）
2. 站点识别与 URL 规范化（提取视频 ID，去掉跟踪参数）
3. `yt-dlp -x` 提取音频；失败且为抖音类站点时，用无头 Chromium 打开页面捕获媒体直链（优先纯音频轨，体积小得多）
4. 用 **imageio-ffmpeg 的完整版 ffmpeg**（不是 Playwright 自带的精简版——那个没有 mp4 解码器，会报 "Invalid data found when processing input"）统一转成 16kHz 单声道 WAV
5. faster-whisper 中文转写（CPU int8，VAD 过滤静音）

## 依赖检查

脚本依赖：requests、imageio-ffmpeg、faster-whisper、yt-dlp、playwright。
首次使用前确认：

```bash
python -c "import requests, imageio_ffmpeg, faster_whisper, yt_dlp, playwright"
```

缺什么装什么（`pip install <包名>`）。Chromium 在 `%LOCALAPPDATA%\ms-playwright\` 下自动发现；
没有的话 `python -m playwright install chromium`。

## 长视频处理

单次转写受执行环境超时限制（约 5 分钟）。音频超过约 8 分钟时，改用分段策略：

1. 下载音频后转 16kHz WAV
2. 用 ffmpeg 按 6~7 分钟切段（段间留 10 秒重叠，如 `-ss 0/-t 400`、`-ss 390/-t 400`……）
3. 逐段调用 faster-whisper，时间戳加上段的偏移量
4. 合并时丢弃每段开头约 12 秒（与上一段重叠的部分），再统一做术语校正

英文术语（DeFi、NFT、GameFi、DApps 等）在中文语音里极易被听错，后处理时务必按上下文校正。

## 结果后处理原则

- 国学、方言、专业术语多的视频，small 模型会听错同音字（如"运有变数"听成"孕有变数"、"言传身教"听成"言传深教"）。结合视频标题和上下文语义**校正明显的同音错字**，并在交付时向用户说明做了哪些校正
- 长视频（>10 分钟）转写耗时会明显变长，可先用 `--model base` 快速出稿
- 无语音或纯背景音乐的视频，转写结果为空，如实告知用户
- 始终用中文回复用户
