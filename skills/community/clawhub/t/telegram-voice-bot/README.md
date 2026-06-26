# Telegram Voice Bot

支持语音识别和中文语音合成的 Telegram 机器人。

## 功能特性

- 🎤 **语音识别** - 使用 OpenAI Whisper 自动识别语音消息
- 🔊 **语音合成** - 使用 Microsoft Edge TTS 进行中文语音回复
- 🇨🇳 **中文支持** - 默认支持中文语音识别和回复

## 安装

```bash
git clone https://github.com/Polityang/telegram-voice-bot.git
cd telegram-voice-bot
pip install -r requirements.txt
```

## 配置

1. 从 [@BotFather](https://t.me/BotFather) 获取 Telegram Bot Token
2. 设置环境变量：

```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
```

## 运行

```bash
python bot.py
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| TELEGRAM_BOT_TOKEN | Telegram Bot Token | (必填) |
| VOICE_REPLY | 是否使用语音回复 | true |

## Whisper 模型

可选模型（通过修改 `MODEL_NAME`）：

| 模型 | 大小 | 速度 |
|------|------|------|
| tiny | ~75MB | 最快 |
| base | ~74MB | 快 |
| small | ~244MB | 中等 |
| medium | ~769MB | 慢 |
| large | ~1550MB | 最慢 |

## 更新日志

### v2.0.0
- 添加中文语音合成功能 (edge-tts)
- 支持语音回复
- 异步 TTS 处理

### v1.0.0
- 初始版本
- 语音识别功能

## 许可证

MIT
