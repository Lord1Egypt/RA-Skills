---
name: video-transcribe-v1-0-3
description: 本地视频转文字 - 使用 OpenAI Whisper 进行语音识别，完全免费、离线运行、保护隐私
---

# Video Transcribe - 视频转文字

🎬 **一键转录本地视频/音频为文字稿**

使用 OpenAI Whisper 进行本地语音识别，完全免费、离线运行、保护隐私。

---

## ✨ 功能特点

- ✅ **完全免费** - 无需 API 密钥，无使用限制
- ✅ **本地运行** - 视频不上传，保护隐私
- ✅ **支持多格式** - mp4, mov, avi, mkv, mp3, wav, m4a 等
- ✅ **自动语言检测** - 支持中文、英文等 90+ 语言
- ✅ **带时间戳** - 输出 SRT 字幕格式
- ✅ **多模型选择** - 从快速到高精度任选
- ✅ **AI 内容总结** - 转录后自动生成 200-300 字摘要 + 关键要点

---

## 📦 安装依赖

**v1.0.3+ 无需手动安装！** 首次运行时会自动检测并安装 Whisper 引擎（约 300MB，一次性）。

如果自动安装失败，可手动安装：

```bash
pip3 install openai-whisper -i https://pypi.tuna.tsinghua.edu.cn/simple
```

> 💡 安装大小：约 200-300 MB
> ⏱️ 安装时间：5-10 分钟（首次需下载模型）

---

## 🚀 使用方法

### 方式 1：直接用命令

```bash
# 基础用法（自动检测语言）
python transcribe.py /path/to/video.mp4

# 指定中文
python transcribe.py /path/to/video.mp4 base zh

# 转录 + AI 总结
python transcribe.py /path/to/video.mp4 --summarize

# 输出到指定目录 + 总结
python transcribe.py /path/to/video.mp4 base zh --summarize
```

### 方式 2：在 OpenClaw 中调用

```
/transcribe /path/to/video.mp4 --summarize
```

---

## 📁 输出文件

转录完成后会生成以下文件（在同一目录）：

| 文件 | 格式 | 说明 |
|------|------|------|
| `视频名.txt` | 纯文本 | 无时间戳的文字稿 |
| `视频名.srt` | SRT 字幕 | 带时间戳，可导入剪映/PR |
| `视频名.vtt` | WebVTT | 网页字幕格式 |
| `视频名_summary.json` | JSON | AI 内容总结（使用 --summarize 时生成） |

---

## 🔧 高级选项

```bash
# 只输出文字，不生成字幕
whisper video.mp4 --output_format txt

# 指定输出语言（翻译为英文）
whisper video.mp4 --task translate

# 调整温度（越高越随机，0 最确定）
whisper video.mp4 --temperature 0

# 显示详细日志
whisper video.mp4 --verbose True
```

完整选项：`whisper --help`

---

## 📝 注意事项

1. **首次运行会下载模型**（一次性，约 100-800 MB）
2. **视频文件路径不要有空格**，或用引号括起来
3. **长视频需要耐心等待**（5 分钟视频约 5-10 分钟转录时间）
4. **背景噪音会影响准确率**，安静环境效果更好

---

## 🙏 致谢

- 核心引擎：[OpenAI Whisper](https://github.com/openai/whisper)
- 开源协议：MIT

---

## 📮 反馈

遇到问题或有建议？欢迎反馈！

**作者：** Seven  
**版本：** 1.0.3  
**更新时间：** 2026-03-18

---

## 📋 更新日志

### v1.0.3 (2026-03-18)
- ✨ **新增**：首次运行时自动安装 Whisper 依赖，无需手动执行 pip 命令
- 🔧 优化：使用清华镜像源自动安装，国内用户更快
- 📝 更新：SKILL.md 说明文档，告知用户自动安装行为

### v1.0.2 (2026-03-16)
- 🐛 **修复**：添加 YAML front matter 到 SKILL.md，修复技能在 OpenClaw 中无法显示的问题
- 📦 更新元数据格式，确保与 ClawHub 规范兼容

### v1.0.0 (2026-03-13)
- ✨ 初始版本发布
- 🎬 支持本地视频/音频转录
- 🤖 集成 OpenAI Whisper 引擎
- 📄 输出 TXT 和 SRT 格式
- 📊 支持 AI 内容总结
