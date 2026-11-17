---
name: zhz-tts
description: 中英文AI语音合成工具，支持 Edge-TTS（免费）和 DashScope CosyVoice 接口。用于将文字转换为语音并保存为 MP3 文件。英文听力练习时自动 0.9 倍速。当用户需要将文字转为语音文件时使用。
version: 1.1.0
homepage: http://openclaw.bjbook.net/
metadata:
  openclaw:
    requires:
      packages:
        - edge-tts
        - requests
        - pyyaml
---

# 中英文AI语音合成工具

基于 Edge-TTS（免费）和 DashScope CosyVoice 接口的语音合成工具，专为中文用户设计。

**适用场景：**
- **英文听力练习**：英文文本默认以 0.9 倍速朗读，方便跟读和听写
- **中文有声内容**：将文章、笔记转为语音文件
- **多语言朗读**：支持中、英、日、韩等多种语言和音色

## 安装依赖

```bash
pip install edge-tts requests pyyaml
```

## 快速开始

```bash

# 英文听力练习（自动 0.9 倍速）
python scripts/main.py -t "The quick brown fox jumps over the lazy dog." -a fox.mp3

# 朗读英文文章
python scripts/main.py --textfile article.txt -a article.mp3

# 中文语音
python scripts/main.py -t "你好世界" -a hello.mp3

# 自定义语速和音色
python scripts/main.py -t "Hello world" -a hello.mp3 -v en-US-JennyNeural -r "-20%"

# 使用 DashScope CosyVoice
python scripts/main.py -t "你好" -a hello.mp3 -e dashscope -v longxiaochun

# 列出可用音色
python scripts/main.py --list-voices
python scripts/main.py --list-voices --lang en

# 查看帮助
python scripts/main.py --help
```

## 命令行参数

| 参数 | 短参数 | 说明 |
|------|--------|------|
| `--text` | `-t` | 要合成的文本内容 |
| `--textfile` | | 从文件读取文本（支持 UTF-8 编码的 txt/md 等） |
| `--audio` | `-a` | 输出音频文件路径（默认: output.mp3） |
| `--engine` | `-e` | TTS 引擎: `edge`（免费，默认）或 `dashscope`（阿里云） |
| `--voice` | `-v` | 音色名称（不指定则根据语言自动选择） |
| `--model` | `-m` | DashScope 模型ID（仅 dashscope 引擎，默认: cosyvoice-v1） |
| `--rate` | `-r` | 语速调整，如 +20%（加速）、-10%（减速）。**英文默认 -10%（0.9 倍速）**，中文默认 +0% |
| `--volume` | | 音量调整，如 +20%、-10%（默认 +0%） |
| `--list-voices` | | 列出可用的音色（配合 `--lang` 过滤语言） |
| `--lang` | | 语言过滤，配合 --list-voices 使用（默认 zh，可选 en/ja/ko 等） |
| `--help` | `-h` | 显示帮助信息 |

## 支持的引擎

| 引擎 | 说明 | 需要 API Key |
|------|------|-------------|
| **edge** | 微软 Edge 神经网络 TTS（免费） | ❌ 不需要 |
| **dashscope** | 阿里云 CosyVoice | ✅ 需要 DASHSCOPE_API_KEY |

## Edge-TTS 常用音色

| 音色 | 语言 | 性别 | 特点 |
|------|------|------|------|
| `zh-CN-XiaoxiaoNeural` | 中文 | 女 | 温暖自然，适合通用场景 |
| `zh-CN-YunxiNeural` | 中文 | 男 | 年轻活力 |
| `zh-CN-YunyangNeural` | 中文 | 男 | 新闻播报风格 |
| `zh-CN-XiaoyiNeural` | 中文 | 女 | 活泼可爱 |
| `zh-TW-HsiaoChenNeural` | 繁体中文 | 女 | 台湾口音 |
| `en-US-GuyNeural` | 英文 | 男 | 自然流畅 |
| `en-US-JennyNeural` | 英文 | 女 | 温暖亲切 |
| `en-GB-RyanNeural` | 英文 | 男 | 英式口音 |

## DashScope CosyVoice 音色

| 音色 | 性别 | 特点 |
|------|------|------|
| `longxiaochun` | 女 | 温柔女声 |
| `longxiaoxia` | 女 | 甜美女声 |
| `longxiaochen` | 男 | 沉稳男声 |
| `longxiaobai` | 男 | 清朗男声 |
| `longlaotie` | 男 | 东北口音 |
| `longshu` | 男 | 书生风格 |
| `longjing` | 女 | 文静女声 |
| `longshuo` | 男 | 阳光男声 |

## 配置文件

工具会自动加载配置文件，按以下优先级查找：

1. `.zhz/tts/config.yaml`（项目级）
2. `~/.zhz/tts/config.yaml`（用户级）

配置文件格式：

```yaml
# 默认引擎
default_engine: edge

# Edge-TTS 默认音色
default_voice: zh-CN-XiaoxiaoNeural

# DashScope 默认模型
default_model: cosyvoice-v1
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `DASHSCOPE_API_KEY` | DashScope API密钥（仅 dashscope 引擎需要） |
| `DASHSCOPE_BASE_URL` | 自定义 API 端点（可选） |

## 英文听力练习示例

```bash
# 课文朗读（0.9 倍速）
python scripts/main.py --textfile lesson.txt -a lesson.mp3

# 更慢速度（0.8 倍速，适合初学者）
python scripts/main.py --textfile lesson.txt -a lesson_slow.mp3 -r "-20%"

# 正常速度（适合复习）
python scripts/main.py --textfile lesson.txt -a lesson_normal.mp3 -r "+0%"

# 指定女声朗读
python scripts/main.py --textfile lesson.txt -a lesson.mp3 -v en-US-JennyNeural
```

## 注意事项

- Edge-TTS 是免费服务，无需 API Key，适合大多数场景
- DashScope CosyVoice 需要 API Key，中文语音质量更高
- 工具会自动检测文本语言并选择合适的默认音色
- **英文文本默认 0.9 倍速**（`-10%`），适合听力练习；可通过 `--rate` 覆盖
- 中文文本默认正常速度（`+0%`）
- 语速和音量参数格式为百分比字符串，如 `"+20%"`、`"-10%"`
- 长文本合成可能需要较长时间
