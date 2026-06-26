# video-to-text - 免费视频转文字 API

## 概述

免费视频转文字 API - 用户需要免费、无需本地下载、直接使用 API 将视频/音频转为文字。

## 触发词

当用户提到以下内容时激活此技能：
- "视频转文字"
- "音频转文字"
- "语音转文字"
- "video to text"
- "audio to text"
- "speech to text"
- "字幕提取"
- "提取字幕"
- "视频转字幕"
- "免费转文字"
- "API转文字"

## 工具

此技能提供以下工具：

### video_to_text

将视频或音频文件转换为文字（字幕/ transcripts）。

**参数：**
- `url` (必填): 视频/音频文件的 URL 地址，支持 mp4, wav, mp3, m4a, webm, ogg 等格式
- `language` (可选): 语言代码，如 "zh" (中文)、"en" (英语)、"ja" (日语)，默认自动检测
- `output_format` (可选): 输出格式，"text" (纯文字) 或 "srt" (字幕格式)，默认 "text"

## 使用示例

```
用户: 帮我把这个视频转成文字
AI: (使用 video_to_text 工具，传入视频URL)

用户: 提取这个音频的字幕
AI: (使用 video_to_text 工具，设置 output_format="srt")

用户: 把这个mp3转成文字
AI: (使用 video_to_text 工具)
```

## 实现说明

此技能使用免费的 Whisper API 服务进行语音识别，无需 API Key，直接调用即可使用。

支持的免费 API 端点：
- https://api.myshell.ai/v1/audio/transcriptions (MyShell Whisper)
- https://api.openai.com/v1/audio/transcriptions (OpenAI，需要Key)

如果主要API不可用，会自动尝试备用方案。

## 注意事项

- 支持的输入格式：mp4, wav, mp3, m4a, webm, ogg, flac
- 最大文件大小：25MB
- 处理时间取决于文件长度，通常需要等待
- 建议使用直接文件URL，避免需要认证的链接
