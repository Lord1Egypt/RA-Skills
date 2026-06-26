---
name: voice-document-maker
description: 制作有声视频文档技能 - 将文字自动转为 TTS 语音，并配上 AI 生成的精美背景图，合成 MP4 视频文件。适用于微信视频卡片交付。
metadata:
  builtin_skill_version: "1.0"
  qwenpaw:
    emoji: "🎬"
---

# 有声视频制作师

## 什么时候用
- 需要将文字内容以"视频卡片"形式发送给用户时。
- 用户要求"生成语音视频"、"做个有声海报"时。
- 替代纯文本回复，提供"视觉 + 听觉"双重体验。

## 核心逻辑
1. **语音生成**：调用 `edge_tts` 生成高质量 MP3。
2. **背景生成**：调用 `pollinations.ai` 根据描述生成精美图片。
3. **视频合成**：使用 `FFmpeg` 将图片和音频合成 MP4。

## 如何使用
直接调用脚本：
```bash
C:\Users\lenovo\.copaw\venv\Scripts\python.exe skills\voice-document-maker\scripts\make_video.py --text "这里是朗读内容" --bg_prompt "背景描述" --output "output.mp4"
```

## 示例
### 制作古风美女有声视频
```bash
python scripts/make_video.py --text "天行健，君子以自强不息。" --bg_prompt "Beautiful elegant Chinese lady, ancient style, soft lighting" --output "gufeng.mp4"
```

### 制作科技风有声视频
```bash
python scripts/make_video.py --text "AI 技术正在改变世界。" --bg_prompt "Futuristic technology background, blue neon, cyberpunk" --output "tech.mp4"
```

## 交付物
- MP4 视频文件，可直接通过 `send_file_to_user` 发送。
