---
name: xhs-video-summary
description: 一键分析小红书视频链接，提取文案、转录语音并深度总结视频内容。当用户提供小红书链接并要求“总结、分析、提取视频”时触发此技能。
metadata:
  openclaw:
    requires:
      bins: ["curl", "ffmpeg", "whisper", "python"]
---

# 小红书视频深度总结 (xhs-video-summary)

## 技能说明

这个技能组合了无水印视频提取、音频分离、AI语音转录和深度文本总结，实现小红书视频的一键分析。支持 Windows / macOS / Linux 跨平台运行。

## 工作流

当用户提供小红书视频链接时，请按照以下步骤执行：

1. **执行自动化脚本**：
   运行封装好的 Python 脚本，传入用户提供的 URL。
   ```bash
   python skills/xhs-video-summary/scripts/run.py "<xhs_url>"
   ```
   *注意：这可能需要 1-2 分钟时间，请在执行时向用户说明正在后台处理。*

2. **读取产物**：
   脚本执行完成后，读取提取出的元数据和语音转录稿：
   - 元数据：`xhs_meta.json` (包含标题、描述、点赞等数据)
   - 逐字稿：`xhs_temp.txt` (视频内的所有语音文字)

3. **分析与输出总结**：
   根据读取到的数据，给用户输出一份结构化的深度总结，必须包含以下模块：
   - 🎬 **视频基础信息** (标题、作者、互动数据)
   - 💡 **视频主题** (一句话概括核心话题)
   - 📝 **详细内容拆解** (按逻辑或知识点拆解详细内容)
   - 🛠 **实用价值** (对观众的具体帮助)
   - 💎 **关键金句** (原话摘录 2-3 句)

4. **清理临时文件**：
   读取完成后，务必清理临时产物文件：
   ```bash
   rm xhs_temp.mp4 xhs_temp.mp3 xhs_temp.txt xhs_meta.json
   ```
   *(Windows 系统下请使用 `del /f xhs_temp.mp4 xhs_temp.mp3 xhs_temp.txt xhs_meta.json`)*

## 依赖要求
- `xiaohongshu-extract` (需通过 clawhub 安装)
- `curl` (用于下载视频)
- `ffmpeg` (用于提取音频)
- `openai-whisper` (用于本地语音识别)
