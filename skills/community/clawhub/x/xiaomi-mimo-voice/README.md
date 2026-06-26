# Xiaomi MiMo Voice

小米 MiMo V2 TTS 语音合成，支持情感、角色扮演、方言等多种风格。

## 特性

- 🎙️ 中文 / 英文语音合成
- 😊 情感风格：Happy、Sad、Angry 等
- 🎭 角色扮演：孙悟空、林黛玉等
- 🗣️ 方言：东北话、四川话、粤语等
- 📢 播报/讲故事风格
- 🎵 唱歌模式

## 配置

在 `~/.openclaw/openclaw.json` 中设置 API Key：

```json
{
  "skills": {
    "entries": {
      "xiaomi-mimo-voice": {
        "enabled": true,
        "env": {
          "MIMO_API_KEY": "your-key"
        }
      }
    }
  }
}
```

## 快速使用

```bash
python3 scripts/tts.py --text "你好世界" --output hello.wav
python3 scripts/tts.py --text "太开心了！" --style Happy --output happy.wav
```

## 安装

```bash
npx clawhub install xiaomi-mimo-voice
```

## 许可证

MIT
