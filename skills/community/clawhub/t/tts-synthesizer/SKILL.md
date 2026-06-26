---
name: TTS Synthesizer | TTS 合成器
description: |
  文字转语音（Text-to-Speech / TTS）工具。
  支持 edge-tts（微软神经网络 TTS，在线合成）和 OpenAI 兼容 API TTS。
  触发词：语音回复、TTS、文字转语音、语音合成、语音对话。
  适用平台：Linux / Windows / macOS。
---

# TTS Synthesizer | TTS 合成器 🔊

将文字转换为语音，支持微软神经网络 TTS（联网合成）和 OpenAI 兼容 API。

## 目录

1. [概述](#概述)
2. [快速开始](#快速开始)
3. [脚本说明](#脚本说明)
4. [声音列表](#声音列表)
5. [输出目录](#输出目录)
6. [环境变量](#环境变量)
7. [故障排查](#故障排查)

---

## 概述

> ⚠️ **注意**：OpenClaw 内置了 `tts` 工具，但它的输出格式（MP3/WebM）不适合直接发送飞书语音。
> **飞书语音消息必须用 `tts_simple.py`**，它会自动输出 OGG/Opus 格式。

### 支持的 TTS 引擎

| 引擎 | 说明 | 优点 | 缺点 |
|------|------|------|------|
| `edge` ⭐ | 微软神经网络 TTS | 免费、联网合成、高音质、支持中文 | 需访问微软服务 |
| `api` | OpenAI 兼容 API | 质量高、可选声音多 | 需要 API Key |

### edge-tts 支持的声音（完整列表）

**中文（大陆）**:
| 声音 | 风格 |
|------|------|
| `zh-CN-XiaoxiaoNeural` | 晓晓（女声，**默认**）|
| `zh-CN-YunxiNeural` | 云希（男声）|
| `zh-CN-YunyangNeural` | 云扬（男声）|
| `zh-CN-XiaoyiNeural` | 晓伊（女声）|

**中文（台湾）**:
| 声音 | 风格 |
|------|------|
| `zh-TW-HsiaoYuNeural` | 小宇（女声）|

**英文**:
| 声音 | 风格 |
|------|------|
| `en-US-JennyNeural` | 美式女声 |
| `en-US-GuyNeural` | 美式男声 |
| `en-GB-SoniaNeural` | 英式女声 |
| `en-GB-RyanNeural` | 英式男声 |
| `en-AU-NatashaNeural` | 澳式女声 |
| `en-IN-NeerjaNeural` | 印度女声 |

**日文**:
| 声音 | 风格 |
|------|------|
| `ja-JP-NanamiNeural` | 日语女声 |
| `ja-JP-MayuNeural` | 日语男声 |

**韩文**:
| 声音 | 风格 |
|------|------|
| `ko-KR-SunHiNeural` | 韩语女声 |
| `ko-KR-InJoonNeural` | 韩语男声 |

**其他常用**:
| 声音 | 语言 |
|------|------|
| `fr-FR-DeniseNeural` | 法语女声 |
| `de-DE-KatjaNeural` | 德语女声 |
| `es-ES-ElviraNeural` | 西班牙语女声 |
| `ru-RU-SvetlanaNeural` | 俄语女声 |
| `pt-BR-FranciscaNeural` | 葡萄牙语女声 |

> 💡 查看完整列表：`python3 scripts/tts_edge.py "test" --list-voices`

---

## 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/skills/tts-synthesizer
pip install -r requirements.txt
```

### 2. 运行（生成飞书语音用这个）

```bash
# ⭐ tts_simple.py — 输出 OGG/Opus，可直接作为飞书语音发送
python3 scripts/tts_simple.py "你好，这是测试语音"

# 使用指定声音（见下方声音列表）
python3 scripts/tts_simple.py "你好" --voice zh-CN-YunxiNeural

# 使用 API
python3 scripts/tts_simple.py "你好" --engine api \
    --api-url https://api.openai.com/v1 \
    --api-key sk-xxx \
    --voice alloy
```

### 3. 调节语速和音调

```bash
# 语速 +10%（稍快）
python3 scripts/tts_simple.py "快速播报" --rate "+10%"

# 语速 -10%（稍慢）
python3 scripts/tts_simple.py "慢速播报" --rate "-10%"

# 音调升高
python3 scripts/tts_simple.py "音调较高" --pitch "+5Hz"
```

---

## 脚本说明

### scripts/tts_simple.py ⭐ 推荐

通用的文字转语音脚本，**自动输出 OGG/Opus 格式，适合飞书语音消息**。

```bash
python3 scripts/tts_simple.py "要转换的文字" [选项]
```

**参数**:

| 参数 | 说明 |
|------|------|
| `text` | 要转换的文字，或 `.txt` 文件路径 |
| `--output, -o` | 输出文件路径 |
| `--engine, -e` | 引擎：`edge`（默认）或 `api` |
| `--voice, -v` | 声音名称 |
| `--rate, -r` | 语速，如 `+10%`、`-5%`（仅 edge） |
| `--pitch, -p` | 音调，如 `+5Hz`、`-3Hz`（仅 edge） |
| `--api-url` | API URL（api 模式） |
| `--api-key` | API Key（api 模式） |
| `--api-model` | API 模型（默认 `tts-1`） |

### scripts/tts_edge.py

纯粹的 edge-tts 脚本，**输出 MP3 格式**（不适合直接发送飞书语音）。

```bash
# 列出所有声音
python3 scripts/tts_edge.py "test" --list-voices

# 生成语音
python3 scripts/tts_edge.py "你好" -o output.mp3 --voice zh-CN-Xiaoxiao
```

> 💡 发送飞书语音消息请用 `tts_simple.py`。

---

## 声音列表

edge-tts 支持 100+ 声音，可通过以下命令查看：

```bash
python3 scripts/tts_edge.py "test" --list-voices
```

常用声音速查：

| 语言 | 代码 | 声音 |
|------|------|------|
| 中文女声 | `zh-CN-Xiaoxiao` | 晓晓（默认）|
| 中文男声 | `zh-CN-Yunxi` | 云希 |
| 美式女声 | `en-US-Jenny` | Jenny |
| 美式男声 | `en-US-Guy` | Guy |
| 英式女声 | `en-GB-Sonia` | Sonia |
| 日语女声 | `ja-JP-Nanami` | Nanami |

---

## 输出格式

**重要**：飞书语音消息需要 **OGG/Opus** 格式，必须使用 `tts_simple.py`。

| 脚本 | 输出格式 | 适用场景 |
|------|----------|----------|
| `tts_simple.py` ⭐ | OGG/Opus | **飞书语音消息**（直接发送） |
| `tts_edge.py` | MP3 | 通用场景（需转换后才能发飞书语音） |

> `tts_simple.py` 会自动将 edge-tts 输出的 webm 转换为 OGG/Opus，专门适配飞书语音消息。

## 输出目录

运行结果保存在工作区的 `projects/tts-synthesizer/` 目录下：

```
~/.openclaw/workspace/projects/tts-synthesizer/
└── output/
    └── tts_20260401_193000.ogg   # OGG/Opus 格式（飞书语音用这个）
```

---

## 环境变量

| 变量名 | 说明 |
|--------|------|
| `OPENCLAW_WORKSPACE` | 工作区根目录 |
| `TTS_API_URL` | OpenAI 兼容 API URL |
| `TTS_API_KEY` | API 密钥 |

---

## 故障排查

### edge-tts 下载失败

```bash
# 检查网络
curl -I https://www.bing.com

# edge-tts 需要访问微软服务
# 如有代理干扰，清除环境变量
unset all_proxy ALL_PROXY
```

### API 模式报错

- 确认 API URL 正确（包含 `/v1`）
- 确认 API Key 有效
- 检查账户余额

### 声音不自然

- 中文推荐：`zh-CN-Xiaoxiao`（晓晓）
- 调节语速 `--rate "+10%"` 或 `--rate "-10%"`
- 调节音调 `--pitch "+3Hz"` 或 `--pitch "-3Hz"`

---

## 平台说明

### edge-tts vs 其他 TTS 方案

| 方案 | 成本 | 音质 | 中文支持 | 离线 | API Key |
|------|------|------|---------|------|---------|
| edge-tts | 免费 | 高 | 很好 | 否 | 不需要 |
| OpenAI TTS | 按量计费 | 很高 | 一般 | 否 | 需要 |
| pyttsx3 | 免费 | 低 | 一般 | 是 | 不需要 |

### 已知限制

- edge-tts 依赖微软服务，需要能访问 `edge.microsoft.com`
- 部分声音在不同地区可能不可用

## 目录结构

### 技能目录（发布用）

```
tts-synthesizer/
├── SKILL.md                    # 本文档
├── _meta.json                  # 元数据
├── .clawhub/                   # ClawHub 源信息
├── requirements.txt            # Python 依赖
└── scripts/
    ├── tts_simple.py          # 通用 TTS 脚本（⭐ 推荐）
    └── tts_edge.py            # edge-tts 专用脚本
```

### 项目目录（运行时数据）

```
~/.openclaw/workspace/projects/tts-synthesizer/
├── output/                    # TTS 输出文件
└── *.ogg                     # 历史语音文件
```

### 模型说明

**edge-tts 无本地模型**，每次联网合成（微软服务器运行）。
如需本地 GPU TTS（用你自己的显卡），需要额外安装 Coqui XTTS 等。
