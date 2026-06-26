---
name: zc_douyin_xiazai_txt
description: 抖音无水印视频下载与文案提取工具，使用本地 ffmpeg 与 Whisper 完成下载、音频提取和文字转写，可选语义分段。
metadata:
  openclaw:
    emoji: 🎵
    requires:
      bins: [ffmpeg, whisper]
      config:
        whisper_model: base
---

# Douyin Download & Transcript Skill

## 功能概述
- **获取无水印视频链接**：解析抖音分享链接或 `modal_id`。
- **下载视频**：保存至指定目录。
- **提取音频**：使用 ffmpeg 转为 16kHz 单声道 PCM WAV（符合 Whisper 要求）。
- **语音转写**：调用本地 Whisper（默认 `base` 模型）生成文字稿。
- **可选语义分段**：使用 OpenClaw 内置 LLM 对转写文本进行分段，提升可读性。

## 环境依赖
- **ffmpeg**（已在脚本中使用绝对路径）。
- **whisper**（通过 `pip install -U openai-whisper` 安装）。
- **Node.js**（用于执行 `douyin.js`）。

确保上述工具可在系统上运行， `ffmpeg -version` 与 `whisper --version` 应返回版本信息。

## 使用方法（Windows CMD / PowerShell）

### 1. 获取视频信息
```bash
node "%USERPROFILE%\.openclaw\skills\zc_douyin_xiazai_txt\douyin.js" info "<抖音分享链接或 modal_id>"
```

### 2. 下载视频
```bash
node "%USERPROFILE%\.openclaw\skills\douyin-download-local\douyin.js" download "<链接或 modal_id>" -o "C:\\Temp\\douyin-download"
```
目录不存在时会自动创建。

### 3. 提取文案（默认语义分段）
```bash
node "%USERPROFILE%\.openclaw\skills\douyin-download-local\douyin.js" extract "<链接或 modal_id>"
```
此命令会下载视频、提取音频、使用 Whisper 转写并进行语义分段，结果保存在 `outputs/douyin/<video_id>/transcript.md`。

### 4. 仅转写（不分段）
```bash
node "%USERPROFILE%\.openclaw\skills\douyin-download-local\douyin.js" extract "<链接或 modal_id>" --no-segment
```

## 常见问题
- **Node 未识别**：请确认已安装 Node.js 并加入系统 PATH。
- **whisper 未识别**：请使用 `pip install -U openai-whisper` 安装，并确保 Python Scripts 目录在 PATH 中。
- **下载失败**：检查链接完整性、网络通畅以及目标目录写入权限。

## 注意事项
- 本工具仅用于个人学习、研究，勿用于商业或侵权用途，遵守抖音平台规则。
- 如平台接口更新导致解析失败，请更新技能或手动修复。
- Whisper 转写质量受音频清晰度影响，可能出现误差。

**声明**：技能中使用的 `https://aweme.snssdk.com` 链接不是私人网站，是抖音官方的服务域名，属于字节跳动旗下，主要用于抖音 App 的接口、授权、数据请求等服务。本次使用该链接仅用于解析下载无水印视频，不进行其他任何操作。
