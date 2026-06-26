# Video Subtitle Generator Skill

AI 视频字幕生成工具 — Claude Skill，基于 SenseAudio ASR。

输入一个视频或音频文件，自动完成：**语音识别 → 字幕生成 → 可选翻译 → 可选烧入视频**。

## 功能特点

- **自动语音识别**：基于 SenseAudio ASR，支持 4 种模型精度
- **20+ 种语言**：中英日韩法德西等主流语言全覆盖
- **字幕翻译**：识别后可翻译成任意支持的目标语言
- **说话人分离**：自动区分多人对话中的不同说话人
- **情感分析**：识别说话人的情感状态
- **字幕烧入**：一键将字幕烧入视频输出新文件
- **多格式输出**：SRT / VTT / TXT / JSON
- **内容总结**：Claude 直接读取转写文本进行内容总结

## 项目结构

```
.
├── SKILL.md              # Skill 描述（Claude 读取）
├── scripts/
│   └── video_subtitle.py # ASR + 字幕生成脚本
├── outputs/              # 输出目录
├── README.md
└── USAGE.md              # 详细使用指南
```

## 环境要求

- Python 3.10+
- 依赖：`requests`
- 系统依赖：`ffmpeg`（音频提取 + 字幕烧入）、`fonts-noto-cjk`（中日韩字幕烧入需要）
- `SENSEAUDIO_API_KEY` — [SenseAudio 官网](https://senseaudio.cn) 获取（唯一需要的密钥）

## 快速使用

在 Claude Code 中对话触发：

> "帮我给这个视频加字幕：/path/to/video.mp4"

详细使用方式和示例请参考 [USAGE.md](USAGE.md)。

## License

MIT

## Author

QWERTY0205
