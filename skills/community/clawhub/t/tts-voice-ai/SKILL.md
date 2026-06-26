---
name: tts-voice-ai
description: AI Text-to-Speech (TTS) 语音合成工具 - 支持中文/英文/日语/韩语/粤语多语言语音生成，语音克隆，AI配音。关键词: TTS, text to speech, 语音合成, 文字转语音, voice generator, AI voice, speech synthesis, 语音生成, 配音, dubbing, 朗读, 有声书, voice cloning, 语音克隆, MiniMax。使用场景：语音合成、文本转语音、有声内容创作、多语言配音、智能客服语音、语音播报、视频配音。
metadata:
  openclaw:
    emoji: 🔊
    requires:
      bins: [python3]
      env: [MINIMAX_API_KEY]
      pip: [requests]
    primaryEnv: MINIMAX_API_KEY
    envHelp:
      MINIMAX_API_KEY:
        required: true
        description: MiniMax API Key (国内版或国际版)
        howToGet: 
          - 国内版: https://platform.minimax.io 注册账号获取 API Key
          - 国际版: https://platform.minimax.io 注册账号获取 API Key
---

# AI TTS 语音合成工具

支持 MiniMax 国内版(`api.minimaxi.com`)和国际版(`api.minimax.io`) API。

## 快速开始

### 1. 设置 API Key

```bash
# 国内版 (sk-api-xxx 格式)
export MINIMAX_API_KEY="sk-api-xxx"

# 国际版
export MINIMAX_API_KEY="your-key"
```

### 2. 生成语音

```bash
# 自动选择最佳音色
python3 tts.py "你好世界"

# 指定语言/风格
python3 tts.py "Hello world" --language english --gender female

# 粤语推荐使用 language_boost
python3 tts.py "你好" --language cantonese --language-boost "Chinese,Yue"

# 指定音色
python3 tts.py "你好" --voice girlfriend_5_speech02_01

# 列出音色
python3 tts.py --list-voices
```

## 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--text` | | 要转语音的文本 | (必填) |
| `--voice` | `-v` | 音色ID | 自动匹配 |
| `--language` | `-l` | 语言 | auto |
| `--gender` | `-g` | 性别 (male/female) | auto |
| `--age` | | 年龄 (young/middle/elder/child) | auto |
| `--style` | `-s` | 风格 | auto |
| `--language-boost` | `-b` | 语言增强 | auto |
| `--model` | `-m` | 模型 | speech-2.8-turbo |
| `--speed` | | 语速 (0.5-2.0) | 1.0 |
| `--format` | `-f` | 格式 (mp3/wav/flac) | mp3 |
| `--output` | `-o` | 输出文件 | output.mp3 |
| `--api` | | API版本 (cn/int) | cn |
| `--list-voices` | | 列出音色 | - |

## Language Boost (语言增强)

`--language-boost` 参数用于增强对小语种和方言的识别能力：

| 语言 | Boost 值 |
|------|----------|
| 普通话 | Chinese |
| 粤语 | **Chinese,Yue** |
| 英语 | English |
| 日语 | Japanese |
| 韩语 | Korean |
| 自动检测 | auto |

**注意：** 粤语必须使用 `Chinese,Yue`，不是 `Cantonese`！

```bash
# 粤语示例
python3 tts.py "你食咗未呀" --language cantonese --language-boost "Chinese,Yue"

# 英语示例
python3 tts.py "Hello world" --language english --language-boost English
```

## 黄金音色推荐

### ✨ 中文 (Mandarin)
| 音色ID | 说明 | 风格 |
|--------|------|------|
| girlfriend_5_speech02_01 | 温柔治愈 | 女声 |
| girlfriend_1_speech02_01 | 甜美软萌 | 女声 |
| ttv-voice-2026011810595326-hxYkopxR | 活泼吐槽 | 女声 |
| ttv-voice-2026011806464526-IPLmlZ8C | 清爽阳光 | 男声 |
| ttv-voice-2026011910402426-5fSKtVmM | 幽默大叔 | 男声 |

### 🌐 English
| 音色ID | 说明 |
|--------|------|
| english_voice_agent_ivc_female_nora | 自然女声 |
| english_voice_agent_ivc_male_julian | 自然男声 |
| english_voice_agent_ivc_female_maya | 年轻女声 |

### 🇭🇰 Cantonese 粤语
| 音色ID | 说明 |
|--------|------|
| HK_Cantonese_female1 | 标准港女 |
| Cantonese_ProfessionalHost（M) | 专业男主持 |

### 🇹🇼 Taiwan 台湾国语
| 音色ID | 说明 |
|--------|------|
| vc_wanwan_0303_01 | 台湾女生 |

### 🇯🇵 Japanese
| 音色ID | 说明 |
|--------|------|
| Japanese_DecisivePrincess | 果断公主 |
| Japanese_IntellectualSenior | 睿智老人 |

### 🇰🇷 Korean
| 音色ID | 说明 |
|--------|------|
| Korean_SweetGirl | 甜妹 |

## 使用示例

### 视频配音 (Dubbing)
```bash
# 中文女声配音
python3 tts.py "欢迎观看本期节目" --voice girlfriend_5_speech02_01 --output intro.mp3

# 英文配音
python3 tts.py "Welcome to our channel" --language english --gender female --output intro_en.mp3
```

### 粤语配音 (强烈建议使用 language_boost)
```bash
# 粤语女声
python3 tts.py "你食咗未呀" --language cantonese --language-boost "Chinese,Yue" --voice HK_Cantonese_female1

# 粤语男声
python3 tts.py "大家好" --language cantonese --language-boost "Chinese,Yue" --voice "Cantonese_ProfessionalHost（M)"
```

### 有声书/朗读
```bash
# 温柔女声朗读
python3 tts.py "从前有座山" --style gentle

# 故事讲述
python3 tts.py "这是一个有趣的故事" --voice ttv-voice-2026011810595326-hxYkopxR
```

### 语音克隆
```bash
# 使用你的克隆音色
python3 tts.py "这是我的声音" --voice jiachuan_0115
```

## 语言代码

| 代码 | 语言 |
|------|------|
| chinese | 普通话 |
| cantonese | 粤语 (推荐配合 language-boost) |
| english | 英语 |
| japanese | 日语 |
| korean | 韩语 |
| taiwan | 台湾国语 |

## API 版本

- `--api cn`: 国内版 (api.minimaxi.com)
- `--api int`: 国际版 (api.minimax.io)
