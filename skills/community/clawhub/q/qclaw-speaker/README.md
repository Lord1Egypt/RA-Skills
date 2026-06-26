# QClaw Speaker 🎙️

> 让 QClaw/OpenClaw 像豆包一样自然开口说话！

如果说 `video-subtitle-extractor` 给大模型安上了"视频字幕眼睛"，  
那么 `qclaw-speaker` 就是给大模型装上了"嘴巴" —— 让 AI 说话。

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🏠 **双引擎** | Edge TTS（在线高品质）+ sherpa-onnx（本地离线） |
| ⚡ **极轻量** | 本地模型仅 13MB（vs qwen-tts 1.7GB，150×更小） |
| 🔊 **6 款音色** | 3 款中文离线 + 3 款微软神经网络在线 |
| 📡 **自动播报** | `auto-speak` 模式，AI 回复自动语音朗读 |
| 🌊 **流式支持** | 边合成边播放，首句 <0.3s 听到 |
| 🔧 **零配置** | `pip install edge-tts` 即可用，一键安装 |

---

## 🚀 Quick Start

```bash
# 1. 安装
pip install edge-tts
python scripts/install.py    # 可选：下载本地模型

# 2. 说话！
python scripts/speak.py "你好，我是QClaw，很高兴为你服务！"

# 3. 开启自动语音播报
python scripts/speak.py --auto-speak on
```

---

## 🎚️ 音色选择

```bash
# 在线高品质（默认，推荐）
python scripts/speak.py "大家好" --voice xiaoxiao   # 晓晓 女声
python scripts/speak.py "大家好" --voice yunxi      # 云希 男声

# 本地离线（需先下载模型）
python scripts/speak.py "大家好" --voice xiao_ya   # 小雅 女声 13MB
python scripts/speak.py "大家好" --voice chaowen   # 超稳 男声 13MB
```

---

## 🔗 与 OpenClaw 集成

在 OpenClaw 中，AI 回复后自动调用：

```python
# AI 生成文本后
output = speak_text(text, voice_name="xiaoxiao")
# → 返回音频文件路径
# → OpenClaw message tool 自动发送语音消息
```

开启自动播报后，每次回复自动朗读，无需手动调用。

---

## 📦 技术架构

```
LLM文本输出 → speak.py → [Edge TTS / sherpa-onnx]
                            ↓
                      音频文件 (MP3/WAV)
                            ↓
                      OpenClaw message 发送
```

- **在线引擎**：edge-tts（微软神经网络，免费）
- **本地引擎**：sherpa-onnx + Piper VITS（13MB ONNX 模型）
- **CPU 推理**：无需 GPU，纯 CPU 实时合成

---

## 📝 License

MIT
