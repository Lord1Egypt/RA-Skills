---
name: voice-reply
description: "语音回复技能 - 每次回复自动生成语音并保存到桌面，支持 Noiz AI TTS"
---

# 语音回复技能 (Voice Reply Skill)

🦞 自动将文字回复转换为语音，每次回复后自动保存到桌面。

## 功能

- 🎙️ 每次回复自动生成语音
- 💾 自动保存到桌面：`~/Desktop/YYYYMMDD_HHMMSS.mp3`
- 🔄 自动删除上一次语音文件
- 📻 自动播放语音
- 🤖 支持 Noiz AI 语音合成

## 前置要求

1. **Noiz AI API Key** - 需要配置 API Key
   - 申请地址：https://noiz.ai
   - 配置命令：
   ```bash
   python3 ~/.openclaw/workspace/skills/voice-reply/scripts/voice.py config --set-api-key 你的APIKey
   ```

2. **依赖安装**：
   ```bash
   pip3 install requests
   ```

## 使用方法

### 方式 1：命令行直接生成
```bash
~/.openclaw/workspace/skills/voice-reply/voice "你好，这是测试"
```

### 方式 2：在对话中自动使用
当用户说话时，使用 skill 自动将回复转为语音。

## 脚本说明

### voice 命令
```bash
~/.openclaw/workspace/skills/voice-reply/voice "你想说的话"
```

参数：
- 文本内容（必需）

输出：
- MP3 文件保存到桌面
- 自动播放语音
- 自动删除上一次录音

### voice.py 脚本
位于 `scripts/voice.py`，功能：
- 调用 Noiz AI TTS API 生成语音
- 支持情感参数设置
- 自动管理语音文件（保存/删除）

## 配置

### 设置 API Key
```bash
python3 ~/.openclaw/workspace/skills/voice-reply/scripts/voice.py config --set-api-key YOUR_API_KEY
```

### 查看当前配置
```bash
python3 ~/.openclaw/workspace/skills/voice-reply/scripts/voice.py config
```

## 技术细节

- 使用 Noiz AI TTS API 进行语音合成
- 默认使用中文女声参考音频
- 输出格式：MP3
- 存储位置：~/Desktop/
- 文件命名：YYYYMMDD_HHMMSS.mp3

## 常见问题

**Q: 提示 API Key 无效？**
A: 确保已在 https://noiz.ai 申请并获取正确的 API Key

**Q: 语音播放失败？**
A: 检查系统音频设置，或直接打开桌面上的 MP3 文件播放

**Q: 如何停止自动语音回复？**
A: 告诉"停止使用语音"即可

---

**版本**：1.0.0  
**平台**：macOS / OpenClaw  
**依赖**：Noiz AI API
