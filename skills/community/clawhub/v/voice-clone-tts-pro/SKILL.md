# voice-clone - 语音合成与声音克隆技能

---
version: 1.0.0
author: OpenClaw Community
tags: [tts, voice, speech, audio, synthesis]
---

## 概述

voice-clone 是一个强大的语音合成技能，支持多种 TTS 引擎和高级声音克隆功能。可以将文本转换为自然语音，支持多种声音风格和语言。

## 触发词

- 语音合成
- TTS
- 声音克隆
- 文字转语音
- 读给我听
- 文本转语音
- 朗读
- 生成语音

## 功能特性

1. **多引擎支持**
   - Edge TTS (微软 Edge 浏览器语音)
   - OpenAI TTS (GPT-4o / GPT-4o-mini)
   - ElevenLabs (高质量声音克隆)
   - Coqui TTS (开源方案)

2. **声音管理**
   - 预设多种语言和声音风格
   - 支持自定义声音参数
   - 声音预览功能

3. **高级功能**
   - 语速调节
   - 音调调节
   - 情感表达
   - 批量处理

## 使用方法

### 基础用法

```
语音合成: [文本内容]
```

### 指定声音

```
用 [声音名称] 朗读: [文本内容]
```

### 指定语言

```
用 [语言] 语音合成: [文本内容]
```

### 声音克隆

```
克隆声音: [参考音频路径]
```

## 依赖

- Python 3.8+
- edge-tts
- openai
- elevenlabs
- coqui-tts
- pydantic

## 安装依赖

```bash
pip install edge-tts openai elevenlabs coqui-tts pydantic aiofiles
```

## 配置

可用的环境变量:
- `OPENAI_API_KEY` - OpenAI API 密钥
- `ELEVENLABS_API_KEY` - ElevenLabs API 密钥
- `DEFAULT_VOICE` - 默认声音设置
- `DEFAULT_RATE` - 默认语速
- `DEFAULT_PITCH` - 默认音调

## 可用声音列表

### 中文声音
- 晓晓 (zh-CN-XiaoxiaoNeural)
- 晓伊 (zh-CN-XiaoyiNeural)
- 云扬 (zh-CN-YunyangNeural)
- 云希 (zh-CN-YunxiNeural)

### 英文声音
- Jenny (en-US-JennyNeural)
- Aria (en-US-AriaNeural)
- Guy (en-US-GuyNeural)
- Sonia (en-GB-SoniaNeural)

## 输出格式

生成的音频文件保存在 `~/.cache/voice-clone/` 目录下。

## 注意事项

1. 部分功能需要 API 密钥
2. 声音克隆功能需要参考音频文件
3. 建议使用高质量音频作为输入以获得最佳效果
