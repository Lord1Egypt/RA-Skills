---
name: xhs-video-analyzer
description: 下载并分析小红书视频内容。当用户提供小红书链接（xiaohongshu.com）时，自动下载视频、提取语音文字、整理总结内容。Use when user provides a xiaohongshu.com URL and wants video content analysis.
---

# 小红书视频分析器

下载小红书视频并提取语音内容进行总结。

## 快速使用

当用户提供小红书链接时，执行以下流程：

```bash
~/.openclaw/skills/xhs-video-analyzer/scripts/full-analyze.sh "https://www.xiaohongshu.com/explore/..."
```

## 工作流程

1. **下载视频** - 使用 Python 脚本或 yt-dlp
2. **提取音频** - 使用 ffmpeg
3. **语音转文字** - 使用 Poe API + Gemini (云端转录)
4. **详细总结** - 基于转录文本生成深度分析报告

## 依赖

- `ffmpeg` - 提取音频
- `curl` - API 请求
- `Poe API Key` - 需要配置 POE_API_KEY 环境变量或在 ~/.openclaw/openclaw.json 中配置

## API 配置

在 `~/.openclaw/openclaw.json` 中配置 Poe API：

```json
{
  "models": {
    "providers": {
      "poe": {
        "baseUrl": "https://api.poe.com/v1",
        "apiKey": "YOUR_POE_API_KEY"
      }
    }
  }
}
```

或设置环境变量：
```bash
export POE_API_KEY="your-api-key"
```

## 转录技术

使用 Poe API 的 `file` 格式发送音频到 Gemini 模型进行转录：

```json
{
  "type": "file",
  "file": {
    "filename": "audio.mp3",
    "file_data": "data:audio/mp3;base64,<base64>"
  }
}
```

## 输出

- 视频文件: `video.mp4`
- 音频文件: `audio.mp3`
- 转录文本: `audio.txt`
- 音频片段: `chunks/` (3分钟一个片段)

## 详细总结指南

转录完成后，**必须**对转录文本进行深度分析和详细总结。总结应包含以下内容：

### 总结结构

1. **视频主题** - 一句话概括视频的核心话题
2. **核心观点** - 提取视频中的主要论点和见解（3-5条）
3. **详细内容分解** - 按话题/章节拆解视频内容，每个部分包含：
   - 子话题标题
   - 具体内容和论据
   - 举例或案例说明
   - 讲述者的个人见解或建议
4. **实用价值** - 视频对观众的实际帮助或启发
5. **关键金句** - 摘录视频中有价值的原话（2-3句）

### 总结原则

- **详尽而非简略** - 不要只列出要点，要展开说明每个观点的具体内容
- **保留原意** - 准确传达讲述者的观点，不要过度概括导致信息丢失
- **结构清晰** - 用标题、列表、引用等方式组织内容，便于阅读
- **突出价值** - 强调视频中对观众有实际帮助的信息和建议
- **语言自然** - 使用流畅的中文表达，避免机械式罗列

### 示例格式

\`\`\`
## 视频主题
[一句话概括]

## 核心观点
1. [观点1] - [具体解释]
2. [观点2] - [具体解释]
3. [观点3] - [具体解释]

## 详细内容

### [子话题1]
[详细说明内容，包括背景、论据、案例等]

### [子话题2]
[详细说明内容，包括背景、论据、案例等]

### [子话题3]
[详细说明内容，包括背景、论据、案例等]

## 实用价值
- [对观众的实际帮助1]
- [对观众的实际帮助2]

## 关键金句
> "[原话摘录1]"
> "[原话摘录2]"
\`\`\`

分析完成后，先输出转录文本的详细总结，再提及工作目录信息。
