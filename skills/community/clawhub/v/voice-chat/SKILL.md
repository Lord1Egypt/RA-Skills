---
name: voice-chat
description: 自动处理语音消息：将语音转写为文字，结合上下文生成智能回复，并合成语音回复。当收到语音或音频消息时自动激活。
---

# Voice Chat Bridge

## 功能
自动处理语音消息，实现“语音 -> 文字 -> 智能回复 -> 语音”的完整闭环。

## 触发条件
当收到语音或音频消息时（`message.type` 为 `voice` 或 `audio`），自动激活此技能。

## 处理流程

### 1. 检测语音
检查消息是否包含 `media.type === 'voice'` 或 `media.type === 'audio'`。

### 2. 转写 (STT)
立即运行转写脚本：
```bash
python3 /root/.agents/skills/voice-chat/scripts/transcribe_audio.py <audio_path>
```
- 输入：音频文件路径（从 `event.message.media.localPath` 获取）。
- 输出：转写文本。

### 3. LLM 分析
使用**当前会话的上下文**生成智能回复。
- **Prompt**：
  ```text
  用户语音转写：{transcript}

  请结合上下文，给出简洁、有帮助的回复。
  ```
- **输出**：回复文本。

### 4. 合成语音 (TTS)
立即运行 TTS 脚本：
```bash
python3 /root/.agents/skills/voice-chat/scripts/reply_with_tts.py "{reply_text}"
```
- 输入：回复文本。
- 输出：`.opus` 语音文件路径。

### 5. 发送回复
使用 `message.send` 工具发送生成的语音文件：
- **文件**：生成的 `.opus` 文件。
- **Caption**：可选的简短文字说明。
- **注意**：不要发送中间状态文字（如“正在处理..."），直接发送最终语音回复。

## 技术细节
- **STT 引擎**：Vosk (离线，中文小模型)。
- **TTS 引擎**：Edge TTS (Microsoft Azure)。
- **音频格式**：OGG/Opus (48kHz, 单声道，64kbps)。
- **临时文件目录**：`/tmp/voice-chat/`。

## 依赖
- **系统**：`ffmpeg`
- **Python**：`vosk`, `edge-tts`, `pydantic`, `python-dotenv`
- **模型**：Vosk 中文小模型 (`vosk-model-small-cn-0.22`)

## 许可证
MIT
