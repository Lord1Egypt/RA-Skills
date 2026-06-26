---
name: video-to-gif
description: Use when converting a video clip into a GIF with ffmpeg. Supports trimming by start time and duration, controlling frame rate and width, and returning the output file details. Includes bilingual Chinese-English guidance.
---

# Video to GIF / 视频转 GIF

## Purpose / 功能定位

### English

Use this skill when the task is to convert a video file into a GIF animation.

This skill is intended for requests such as:

- convert a video to GIF
- make a GIF from a clip
- export part of a video as a GIF
- create a smaller GIF by limiting width, frame rate, or duration

### 中文

当任务是把一个视频文件转换成 GIF 动图时，应使用这个 Skills。

这个 Skills 适合处理以下类型的请求：

- 把视频转成 GIF
- 从视频里截取一段做成 GIF
- 导出视频片段为 GIF
- 通过限制宽度、帧率、时长来生成更小的 GIF

## What This Skill Does / 这个 Skills 做什么

### English

This skill uses `ffmpeg` to convert video into GIF and supports:

- custom frame rate
- custom output width
- custom start time
- custom duration
- output file summary after conversion

### 中文

这个 Skills 使用 `ffmpeg` 将视频转换为 GIF，并支持：

- 自定义帧率
- 自定义输出宽度
- 自定义开始时间
- 自定义截取时长
- 转换完成后输出结果摘要

## Prerequisites / 前置依赖

### English

This skill requires:

- `ffmpeg`
- `ffprobe`

Before running the script, check:

```bash
command -v ffmpeg
command -v ffprobe
```

If either command is missing, ask the user to install ffmpeg first instead of trying to auto-install it silently.

### 中文

这个 Skills 依赖：

- `ffmpeg`
- `ffprobe`

运行脚本前先检查：

```bash
command -v ffmpeg
command -v ffprobe
```

如果缺少其中任意一个命令，应先提示用户安装 `ffmpeg`，而不是静默自动安装。

## Quick Start / 快速开始

### English

```bash
python3 scripts/convert.py input.mp4 output.gif
python3 scripts/convert.py input.mp4 output.gif --fps 12 --width 360
python3 scripts/convert.py input.mp4 output.gif --start 00:00:03 --duration 5
```

### 中文

```bash
python3 scripts/convert.py input.mp4 output.gif
python3 scripts/convert.py input.mp4 output.gif --fps 12 --width 360
python3 scripts/convert.py input.mp4 output.gif --start 00:00:03 --duration 5
```

## Parameters / 参数

| Parameter / 参数 | Type / 类型 | Required / 必填 | Default / 默认值 | Description / 说明 |
|---|---|---|---|---|
| `input` | string | yes | - | input video path / 输入视频路径 |
| `output` | string | yes | - | output GIF path / 输出 GIF 路径 |
| `fps` | number | no | 15 | output frame rate / 输出帧率 |
| `width` | number | no | 480 | output width in pixels / 输出宽度像素 |
| `start` | string | no | `0` | clip start time / 开始时间 |
| `duration` | string | no | - | clip duration / 持续时间 |

## Workflow / 工作流程

### English

1. Confirm the input file exists.
2. Confirm `ffmpeg` and `ffprobe` are installed.
3. Choose optional parameters such as `fps`, `width`, `start`, and `duration`.
4. Run the conversion script.
5. Return the output path, size, dimensions, and frame rate.

### 中文

1. 确认输入文件存在。
2. 确认 `ffmpeg` 和 `ffprobe` 已安装。
3. 选择需要的可选参数，例如 `fps`、`width`、`start`、`duration`。
4. 执行转换脚本。
5. 返回输出路径、文件大小、尺寸和帧率。

## When To Use / 适用场景

### English

Use this skill when the user wants a GIF generated from a local video file.

### 中文

当用户希望从本地视频文件生成 GIF 时，应使用这个 Skills。

## When Not To Use / 不适用场景

### English

Do not use this skill for:

- editing video timelines in a full editor
- downloading online videos
- generating animated stickers in platform-specific formats
- converting images into GIF slideshows

### 中文

以下场景不应使用这个 Skills：

- 完整的视频时间线编辑
- 下载在线视频
- 生成特定平台格式的动态贴纸
- 把多张图片拼接成 GIF 轮播

## Script / 脚本

### English

Use:

```bash
python3 scripts/convert.py <input> <output> [--fps N] [--width N] [--start T] [--duration T]
```

### 中文

使用方式：

```bash
python3 scripts/convert.py <input> <output> [--fps N] [--width N] [--start T] [--duration T]
```
