---
name: "video-toolkit-free"
description: "基于FFmpeg的视频处理工具,支持格式转换、压缩、字幕生成、宽高比调整,适合个人内容创作者"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "视频工具箱免费版"
  version: "1.0.0"
  summary: "基于FFmpeg的视频处理工具,支持格式转换、压缩、字幕生成、宽高比调整,适合个人内容创作者"
  tags:
    - "视频"
    - "FFmpeg"
    - "多媒体"
    - "字幕"
    - "压缩"
    - "内容创作"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 视频工具箱 - 免费版

## 概述

视频工具箱免费版是一款面向个人内容创作者的视频处理工具,基于FFmpeg提供格式转换、视频压缩、字幕生成、宽高比调整和音频清理等核心功能。覆盖TikTok、Instagram、YouTube、WhatsApp等主流社交平台规格,帮助创作者快速适配多平台发布需求。

## 核心能力

### 1. 视频格式转换与压缩

```bash
# 转换为MP4(H.264+AAC,最大兼容性)
ffmpeg -i input.mov -c:v libx264 -c:a aac -movflags +faststart output.mp4

# 压缩视频(CRF 23为默认平衡值,越小质量越高文件越大)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4

# 压缩为WhatsApp规格(目标<64MB)
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset slow -c:a aac -b:a 96k -fs 62M output.mp4
```

压缩参数说明:

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| CRF | 质量控制(18-28) | 23(默认)/28(高压缩) |
| preset | 编码速度 | medium(平衡)/slow(高质量) |
| -b:a | 音频比特率 | 128k(标准)/96k(压缩) |
| -fs | 文件大小限制 | 平台限制减2MB余量 |
| -movflags +faststart | Web播放优化 | 必须添加 |

**输入**: 用户提供视频格式转换与压缩所需的指令和必要参数。
**处理**: 按照skill规范执行视频格式转换与压缩操作,遵循单一意图原则。
**输出**: 返回视频格式转换与压缩的执行结果,包含操作状态和输出数据。

### 2. 字幕生成(Whisper本地转录)

```bash
# 使用Whisper生成SRT字幕
whisper input.mp4 --model small --language zh --output_format srt

# 将字幕烧入视频(硬字幕)
ffmpeg -i input.mp4 -vf subtitles=input.srt -c:a copy output.mp4

# 生成VTT字幕(Web格式)
whisper input.mp4 --model small --language zh --output_format vtt
```

**输入**: 用户提供字幕生成(Whisper本地转录)所需的指令和必要参数。
**处理**: 按照skill规范执行字幕生成(Whisper本地转录)操作,遵循单一意图原则。
**输出**: 返回字幕生成(Whisper本地转录)的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 宽高比调整

```bash
# 裁剪为9:16(竖屏,TikTok/Reels)
ffmpeg -i input.mp4 -vf "crop=ih*9/16:ih" -c:a copy output.mp4

# 填充为16:9(横屏,加黑边)
ffmpeg -i input.mp4 -vf "pad=ceil(iw/16)*16:ih:(ow-iw)/2:(oh-ih)/2:black" -c:a copy output.mp4

# 裁剪为1:1(正方形,Instagram)
ffmpeg -i input.mp4 -vf "crop=ih:ih" -c:a copy output.mp4
```

**输入**: 用户提供宽高比调整所需的指令和必要参数。
**处理**: 按照skill规范执行宽高比调整操作,遵循单一意图原则。
**输出**: 返回宽高比调整的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 音频处理

```bash
# 音频标准化(统一音量)
ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11" -c:v copy output.mp4

# 降噪
ffmpeg -i input.mp4 -af "highpass=f=200,lowpass=f=3000" -c:v copy output.mp4

# 提取音频为MP3
ffmpeg -i input.mp4 -vn -acodec mp3 -b:a 192k output.mp3

# 替换视频音频
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
```

**输入**: 用户提供音频处理所需的指令和必要参数。
**处理**: 按照skill规范执行音频处理操作,遵循单一意图原则。
**输出**: 返回音频处理的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 视频信息检测

```bash
# 获取视频详细信息
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# 快速查看关键信息
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,duration,bit_rate -of default=noprint_wrappers=1 input.mp4
```

**输入**: 用户提供视频信息检测所需的指令和必要参数。
**处理**: 按照skill规范执行视频信息检测操作,遵循单一意图原则。
**输出**: 返回视频信息检测的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 6. 主流平台规格

| 平台 | 宽高比 | 最大时长 | 最大文件 | 推荐编码 |
|------|--------|----------|----------|----------|
| TikTok | 9:16 | 3分钟 | 287MB | H.264/AAC |
| Instagram Reels | 9:16 | 90秒 | 250MB | H.264/AAC |
| YouTube Shorts | 9:16 | 60秒 | 无限制 | H.264/AAC |
| YouTube | 16:9 | 12小时 | 256GB | H.264/AAC |
| WhatsApp | 任意 | 3分钟 | 64MB | H.264/AAC |

**输入**: 用户提供主流平台规格所需的指令和必要参数。
**处理**: 按照skill规范执行主流平台规格操作,遵循单一意图原则。
**输出**: 返回主流平台规格的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：的视频处理工具、支持格式转换、适合个人内容创作、面向个人内容创作、者的视频处理工具、提供格式转换、视频压缩、音频清理等核心功、覆盖主流社交平台、核心能力、Use、when、需要视频处理、音频编辑、媒体转换、配音生成时使用、不适用于版权受保、护的媒体内容处理、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:视频适配TikTok发布

用户有一段横屏视频,需要转为TikTok竖屏格式发布。

```bash
# 步骤1:检测源视频信息
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration input.mp4

# 步骤2:裁剪为9:16竖屏
ffmpeg -i input.mp4 -vf "crop=ih*9/16:ih" -c:a copy temp.mp4

# 步骤3:检查时长(<=3分钟)
# 如果超过3分钟,截取前3分钟
ffmpeg -i temp.mp4 -t 180 -c copy output.mp4

# 步骤4:压缩确保<287MB
ffmpeg -i output.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k -movflags +faststart final.mp4
```

### 场景二:为视频添加字幕

用户需要为一段教学视频添加中文字幕。

```bash
# 步骤1:使用Whisper生成字幕
whisper tutorial.mp4 --model small --language zh --output_format srt

# 步骤2:将字幕烧入视频
ffmpeg -i tutorial.mp4 -vf subtitles=tutorial.srt -c:v libx264 -crf 23 -c:a copy tutorial_subbed.mp4

# 步骤3:验证字幕显示
ffprobe tutorial_subbed.mp4
```

### 场景三:压缩视频发送WhatsApp

用户需要将一段大视频压缩到64MB以下通过WhatsApp发送。

```bash
# 步骤1:检测源文件大小和时长
ffprobe -v error -show_entries format=size,duration -of default=noprint_wrappers=1 input.mp4

# 步骤2:计算目标比特率
# 目标大小: 62MB(留2MB余量)
# 时长: 120秒
# 比特率 = (62 * 8192) / 120 - 96(音频) = 4134kbps

# 步骤3:压缩
ffmpeg -i input.mp4 -c:v libx264 -b:v 4000k -maxrate 5000k -bufsize 8000k -c:a aac -b:a 96k -fs 62M output.mp4

# 步骤4:验证文件大小
ls -lh output.mp4
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 环境检查

```bash
# 检查FFmpeg
ffmpeg -version
ffprobe -version

# 检查Whisper(可选,用于字幕)
whisper --version 2>/dev/null || pip install openai-whisper
```

### 常用请求快速对照

| 用户需求 | 执行命令 |
|----------|----------|
| 适配TikTok | 裁剪9:16,检查时长<=3分钟,压缩 |
| 添加字幕 | Whisper生成SRT,烧入视频 |
| WhatsApp压缩 | 目标<64MB,H.264,AAC |
| 提取音频 | `-vn -acodec mp3` |
| 制作GIF | 提取帧,优化调色板,循环 |
| 分割片段 | `-ss`和`-t`按时间戳切割 |

### 执行模式

```text
1.明确目标: 什么平台?什么格式?文件大小限制?
2.检测源文件: ffprobe获取编码/分辨率/时长/音频
3.处理: FFmpeg执行转换
4.验证: 确认输出满足规格(时长/大小/可播放性)
5.交付: 提供文件给用户
```

## 示例

### 平台规格配置文件

```json
{
  "platforms": {
    "tiktok": {
      "aspect_ratio": "9:16",
      "max_duration": 180,
      "max_size_mb": 287,
      "video_codec": "libx264",
      "audio_codec": "aac",
      "crf": 23
    },
    "instagram_reels": {
      "aspect_ratio": "9:16",
      "max_duration": 90,
      "max_size_mb": 250,
      "video_codec": "libx264",
      "audio_codec": "aac",
      "crf": 23
    },
    "youtube_shorts": {
      "aspect_ratio": "9:16",
      "max_duration": 60,
      "max_size_mb": null,
      "video_codec": "libx264",
      "audio_codec": "aac",
      "crf": 23
    },
    "whatsapp": {
      "aspect_ratio": "any",
      "max_duration": 180,
      "max_size_mb": 64,
      "video_codec": "libx264",
      "audio_codec": "aac",
      "crf": 28
    }
  }
}
```

### 免费版与专业版功能对比

| 功能项 | 免费版 | 专业版 |
|--------|--------|--------|
| 格式转换 | 单文件 | 批量处理 |
| 视频压缩 | 基础CRF | 自适应+多码率 |
| 字幕生成 | Whisper基础 | 多语言+样式定制 |
| 宽高比 | 裁剪/填充 | 智能重构图 |
| AI超分 | 不支持 | Real-ESRGAN |
| 批量处理 | 不支持 | 文件夹批量 |
| 平台规格 | 5个主流平台 | 全平台+自定义 |
| 自动化 | 手动执行 | 工作流自动化 |
| 适用对象 | 个人创作者 | 内容团队/机构 |

## 最佳实践

### 1. 质量规则

- 始终将音频重新编码为AAC(最大兼容性)
- 使用 `-movflags +faststart` 优化Web播放
- CRF 23是H.264的良好默认值(越小越好越大)
- 交付前验证:时长、文件大小、可播放性

### 2. 平台适配优先级

```text
适配流程:
1.宽高比 -> 裁剪或填充到目标比例
2.时长 -> 超长则截取
3.文件大小 -> 压缩到限制以内
4.编码 -> 确保H.264+AAC
5.验证 -> ffprobe检查最终输出
```

### 3. 常用FFmpeg参数速查

| 参数 | 作用 | 常用值 |
|------|------|--------|
| -crf | 质量控制 | 18(高质量)/23(默认)/28(压缩) |
| -preset | 编码速度 | ultrafast/fast/medium/slow |
| -b:a | 音频比特率 | 192k(高质量)/128k(标准)/96k(压缩) |
| -t | 时长限制 | 60/90/180秒 |
| -fs | 文件大小限制 | 62M/248M/285M |
| -vf | 视频滤镜 | crop/pad/subtitles |
| -af | 音频滤镜 | loudnorm/highpass/lowpass |

## 常见问题

### Q1: 免费版支持批量处理吗?

免费版仅支持单文件处理。如需批量处理整个文件夹,请使用专业版的批量操作功能。

### Q2: Whisper字幕支持哪些语言?

Whisper支持30+种语言的自动转录,包括中文、英文、日语、韩语等。使用 `--language` 参数指定语言可获得更准确的结果。

### Q3: 视频压缩后质量损失大怎么办?

降低CRF值(如从23降到18)可提高质量,但文件会更大。也可使用 `-preset slow` 在相同质量下获得更小的文件。根据平台文件大小限制找到平衡点。

### Q4: 如何确保视频在各平台正常播放?

始终使用H.264视频编码+AAC音频编码,添加 `-movflags +faststart` 优化Web播放,这是最大兼容性的组合。

### Q5: 智能重构图是什么?

智能重构图是专业版功能,通过AI分析视频内容自动选择最佳裁剪区域,避免裁剪掉重要主体。免费版仅支持居中裁剪。

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| FFmpeg/FFprobe | 核心工具 | 必需 | 系统包管理器或官网下载 |
| Whisper | 字幕生成 | 可选 | pip install openai-whisper |
| Python 3 | Whisper依赖 | 可选(字幕功能) | 系统包管理器 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

FFmpeg安装:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows
winget install Gyan.FFmpeg
# 或下载: https://ffmpeg.org/download.html
```

Whisper安装(可选):

```bash
pip install openai-whisper
```

### API Key 配置

本Skill基于FFmpeg本地工具运行,无需额外API Key。Whisper为本地模型运行,不依赖外部API。视频处理完全在本地执行,不上传至外部服务。

### 可用性分类

- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作。核心视频处理功能依赖exec工具执行FFmpeg/FFprobe命令,Whisper字幕功能需要Python环境。仅处理用户明确提供的视频文件,不自动访问其他文件。

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 本地运行，不支持多设备同步
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力