# STT Simple - 本地语音识别 / Local Speech-to-Text

基于 OpenAI Whisper 的简单本地语音转文字工具。  
A simple local speech-to-text tool based on OpenAI Whisper.

## ✨ 特点 / Features

- 🚀 **一键安装 / One-click install** - 自动配置虚拟环境、依赖、模型 / Auto-configures venv, dependencies, and models
- 🌍 **99+ 语言 / 99+ languages** - 支持中文、英文、日文等 / Supports Chinese, English, Japanese, etc.
- 💰 **完全免费 / Completely free** - 本地运行，无 API 费用 / Runs locally, no API costs
- 🔒 **隐私安全 / Privacy safe** - 音频文件不出本地 / Audio files never leave your machine

## 📦 安装 / Installation

```bash
# 进入技能目录 / Enter skill directory
cd /root/.openclaw/workspace/skills/stt-simple

# 运行安装脚本（首次使用）/ Run install script (first time)
bash install.sh
```

安装完成后 / After installation:
- 虚拟环境 / Virtual env: `/root/.openclaw/venv/stt-simple/`
- 模型缓存 / Model cache: `~/.cache/whisper/`
- 输出目录 / Output dir: `/root/.openclaw/workspace/stt_output/`

## 🎯 使用方法 / Usage

### 命令行 / Command Line

```bash
# 基本用法 / Basic usage
/root/.openclaw/venv/stt-simple/bin/whisper audio.ogg --model small --language Chinese

# 指定输出目录 / Specify output directory
/root/.openclaw/venv/stt-simple/bin/whisper audio.ogg --model small --language Chinese --output_dir /tmp/output

# 输出多种格式 / Output multiple formats
/root/.openclaw/venv/stt-simple/bin/whisper audio.ogg --model small --output_format txt,json,srt
```

### Python 脚本 / Python Script

```bash
/root/.openclaw/venv/stt-simple/bin/python \
  /root/.openclaw/workspace/skills/stt-simple/stt_simple.py \
  audio.ogg small zh
```

### Python API

```python
import whisper

model = whisper.load_model("small")
result = model.transcribe("audio.ogg", language="zh")
print(result["text"])
```

## 📊 模型对比 / Model Comparison

| 模型 / Model | 大小 / Size | CPU 速度 / Speed | 推荐场景 / Recommended For |
|------|------|---------|---------|
| tiny | 39MB | ⚡⚡⚡ | 快速测试 / Quick testing |
| base | 74MB | ⚡⚡ | 日常使用 / Daily use |
| small | 244MB | ⚡ | **推荐 / Recommended** |
| medium | 769MB | 🐌 | 高精度需求 / High accuracy needs |
| large | 1.5GB | 🐌🐌 | 最佳质量 / Best quality |

## 🌐 语言代码 / Language Codes

| 语言 / Language | 代码 / Code | 别名 / Alias |
|------|------|------|
| 中文 / Chinese | zh | Chinese |
| 英文 / English | en | English |
| 日文 / Japanese | ja | Japanese |
| 韩文 / Korean | ko | Korean |
| 法文 / French | fr | French |
| 德文 / German | de | German |
| 西班牙文 / Spanish | es | Spanish |

## 📁 输出格式 / Output Formats

- `.txt` - 纯文本 / Plain text
- `.json` - 完整结果（含时间戳、置信度）/ Full results with timestamps and confidence
- `.srt` - 字幕格式（视频用）/ Subtitle format (for videos)
- `.vtt` - WebVTT（网页用）/ WebVTT (for web)

## 🔧 故障排查 / Troubleshooting

### 检查安装状态 / Check Installation

```bash
/root/.openclaw/venv/stt-simple/bin/whisper --version
```

### 重新安装 / Reinstall

```bash
rm -rf /root/.openclaw/venv/stt-simple
bash /root/.openclaw/workspace/skills/stt-simple/install.sh
```

### 手动下载模型 / Manual Model Download

```bash
# 模型会下载到 ~/.cache/whisper/
# Models will be downloaded to ~/.cache/whisper/
# 可以预先下载避免首次运行等待
# Pre-download to avoid waiting on first run
/root/.openclaw/venv/stt-simple/bin/python -c "import whisper; whisper.load_model('small')"
```

## 📝 许可证 / License

- Whisper: MIT License (OpenAI)
- 本技能 / This skill: MIT License

## 🙏 致谢 / Acknowledgments

基于 [OpenAI Whisper](https://github.com/openai/whisper) 构建。  
Built on [OpenAI Whisper](https://github.com/openai/whisper).
