---
name: voice-reply
description: |
  语音回复模式。使用 /voiceMode 切换语音回复模式。
  开启后所有回复自动转换为语音发送，关闭后恢复文字回复。
  支持 Telegram、iMessage 等渠道的语音消息发送。
---

# Voice Reply Skill

## 功能

1. **语音模式切换** - 使用 /voiceMode 命令切换
2. **语音自动发送** - 开启后回复自动转为语音发送

## 指令

### /voiceMode
切换语音回复模式：
- 开启：所有回复自动转换为中文女声语音发送（只发语音，不发文字）
- 关闭：恢复普通文字回复

### /voice status
查看当前语音模式状态

## 工作流程

### 语音模式开启时
1. 捕获回复内容
2. 使用 edge-tts 生成语音
3. 发送到用户渠道（只发语音，不发文字）

### 语音模式关闭时
1. 正常发送文字回复

## 一键发送脚本

### voice-send.js
快速生成语音并发送到 Telegram：

```bash
node scripts/voice-send.js "要发送的文字" [telegram_id]
```

示例：
```bash
node scripts/voice-send.js "你好呀！" 5500262186
```

### 工作流程（自动）
1. 生成语音文件 -> /tmp/voice-reply/voice_xxx.mp3
2. 复制到 ~/.openclaw/workspace/voice.mp3
3. 使用 openclaw message 发送

## 技术细节

- **语音生成**: edge-tts
- **默认语音**: zh-CN-XiaoxiaoNeural（中文女声）
- **输出目录**: /tmp/voice-reply/
- **文件格式**: MP3
- **支持渠道**: Telegram, iMessage, Discord 等

## 状态管理

当前模式由 agent 自行维护在会话上下文中。

## 重要提示

- 语音模式下：只发语音，不发文字
- 文字模式下：正常文字回复
- 切换命令：/voiceMode
