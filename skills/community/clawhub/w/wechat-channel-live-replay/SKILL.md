---
name: wechat-channel-live-replay
description: (已验证) 根据视频号名称搜索用户并下载指定日期的直播回放视频，支持自动转写直播稿。
metadata:
  version: 1.0.0
  source: https://github.com/your-repo/wechat-channel-live-replay
  author: an
  tags: [wechat, video-channel, live-streaming, replay, download, transcription, tikhub]
  license: MIT
  requirements:
    - python
    - "pip:requests"
    - "pip:openai-whisper"
    - "exec:ffmpeg"
    - "skill:douyin-video-transcriber"
---

# SKILL.md for wechat-channel-live-replay

## Description

这是一个专业的微信视频号直播回放下载工具。它通过调用 TikHub API 搜索视频号用户，获取其直播历史记录，并按指定日期筛选和下载回放视频。

该技能支持自动将下载的直播视频转写为文字稿，并保存到 `live-replay-analyzer` 技能的输入目录中，作为直播复盘的前置数据准备工具。

## ⚠️ Prerequisites (前置条件)

**在使用本技能前，您必须在您的系统上完成以下配置：**

1.  **配置 TikHub Token**: 请在 `~/.openclaw/config.json` 中添加 `tikhub_api_token`。
    ```json
    {
      "tikhub_api_token": "YOUR_TIKHUB_API_TOKEN"
    }
    ```

2.  **安装 ffmpeg**: 本技能需要使用 `ffmpeg` 从视频中提取音频。
    -   请从 [ffmpeg 官网](https://ffmpeg.org/download.html) 下载。
    -   安装后，**必须将 `ffmpeg` 的可执行文件路径添加到系统的 `PATH` 环境变量中**。

## How to Use

### Parameters

*   **`--keywords`** (必填): 视频号名称（搜索关键词）。
*   **`--date`** (可选): 指定日期，格式 `YYYY-MM-DD`。不指定则下载最新一次直播回放。
*   **`--output-dir`** (可选): 输出目录，默认为 `workspace/data`。
*   **`--no-transcribe`** (可选): 跳过语音转文字步骤，只下载视频。

### Example Invocation

**下载最新回放并转写:**
```powershell
# AI 应动态查找 python 路径
python path/to/export.py --keywords "视频号名称"
```

**下载指定日期的回放:**
```powershell
# AI 应动态查找 python 路径
python path/to/export.py --keywords "视频号名称" --date "2026-03-19"
```

**只下载视频，不转写:**
```powershell
# AI 应动态查找 python 路径
python path/to/export.py --keywords "视频号名称" --no-transcribe
```

## Output

*   **视频文件**: `{昵称}_{日期}_{时间戳}.mp4`，保存在输出目录中。
*   **文字稿**: `script.txt`，保存在 `skills/live-replay-analyzer/input/{视频号名称}/{日期}/` 目录中。
*   **汇总报告**: `wechat_replay_{关键词}_{时间戳}.json`，包含任务执行的所有详细信息。

## Integration

本技能与 `live-replay-analyzer` 技能紧密集成：
1.  本技能下载的直播视频会被转写为 `script.txt`。
2.  `script.txt` 会自动保存到 `live-replay-analyzer` 的输入目录中。
3.  用户可以直接调用 `live-replay-analyzer` 技能，使用本技能生成的文字稿来生成复盘报告。
