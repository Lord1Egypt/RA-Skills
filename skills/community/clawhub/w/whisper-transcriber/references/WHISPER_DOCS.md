# Whisper.cpp 文档摘要

## 官方资源

- **GitHub:** https://github.com/ggml-org/whisper.cpp
- **模型下载:** https://huggingface.co/ggerganov/whisper.cpp
- **文档:** https://github.com/ggml-org/whisper.cpp#readme

## 支持的模型

| 模型 | 大小 | 描述 |
|------|------|------|
| tiny | 75 MB | 最快，精度一般 |
| base | 142 MB | 平衡推荐 |
| small | 466 MB | 精度好 |
| medium | 1.5 GB | 精度很好 |
| large-v3 | 2.9 GB | 精度最佳 |

## 常用命令

```bash
# 基础转写
whisper-cli -m model.bin -l zh audio.wav

# 输出 SRT
whisper-cli -m model.bin -l zh -osrt audio.wav

# 输出文本
whisper-cli -m model.bin -l zh -otxt audio.wav

# 自动检测语言
whisper-cli -m model.bin --detect-language audio.wav

# 翻译为英语
whisper-cli -m model.bin -l zh --translate audio.wav
```

## 性能优化

- 使用 Metal GPU 加速（Apple Silicon）
- 调整线程数：`-t 4`
- 使用量化模型：`base-q5_1`

## 音频格式

支持：FLAC, MP3, OGG, WAV

推荐格式：16kHz 单声道 WAV
