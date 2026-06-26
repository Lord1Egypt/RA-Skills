# Telegram Voice Bot Skill

支持语音识别和中文语音合成的 Telegram 机器人技能。

## 功能

- 🎤 **语音识别** - 使用 OpenAI Whisper 自动识别语音消息
- 🔊 **语音合成** - 使用 Microsoft Edge TTS 进行中文语音回复
- 🇨🇳 **中文支持** - 默认支持中文

## 依赖

- Python 3.8+
- openai-whisper
- edge-tts
- requests
- Telegram Bot Token

## 安装

```bash
pip install -r requirements.txt
```

## 配置

1. 从 @BotFather 获取 Telegram Bot Token
2. 设置环境变量：
   ```bash
   export TELEGRAM_BOT_TOKEN="your_token"
   ```

## 使用方法

```bash
python bot.py
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| TELEGRAM_BOT_TOKEN | Telegram Bot Token | (必填) |
| VOICE_REPLY | 是否使用语音回复 | true |

## Whisper 模型

在代码中修改 `MODEL_NAME`：

- tiny (最快, ~75MB)
- base (默认, ~74MB)
- small (~244MB)
- medium (~769MB)
- large (~1550MB)

## 版本

- v2.0.0 - 添加中文语音合成
- v1.0.0 - 初始版本（仅语音识别）

## 许可证

MIT
