# 短视频自动处理技能

**创建日期**: 2026-03-23  
**版本**: v1.0

---

## ✨ 技能概述

自动处理短视频，实现：
- 🎙️ **语音识别** - 自动提取视频音频并识别为文字
- 📝 **字幕生成** - 生成 SRT/VTT 格式字幕文件
- 🎯 **标题提炼** - 从内容中智能提炼吸引人的标题
- 📺 **字幕添加** - 将字幕烧录到视频中
- 🎬 **视频生成** - 输出带字幕的新视频

---

## 🎯 使用场景

### 1. 自媒体内容二次创作
- 提取视频内容
- 添加中文字幕
- 重新发布到多平台

### 2. 课程视频处理
- 自动添加字幕
- 提炼章节标题
- 生成学习资料

### 3. 访谈/会议记录
- 语音转文字
- 生成会议纪要
- 添加时间戳

### 4. 短视频本地化
- 识别原语言字幕
- 翻译为目标语言
- 烧录新字幕

---

## 🚀 快速使用

### 基础使用

```bash
# 处理单个视频
python scripts/video_processor.py \
  --input "video.mp4" \
  --output "./output"

# 处理并添加字幕
python scripts/video_processor.py \
  --input "video.mp4" \
  --output "./output" \
  --add-subtitles

# 处理并提炼标题
python scripts/video_processor.py \
  --input "video.mp4" \
  --output "./output" \
  --generate-title
```

### 完整流程

```bash
# 完整处理流程
python scripts/video_processor.py \
  --input "input/video.mp4" \
  --output "./output" \
  --extract-audio \
  --recognize-speech \
  --generate-subtitles \
  --add-subtitles \
  --generate-title \
  --export-video
```

---

## 📋 处理流程

### 1. 视频分析
```
输入视频
  ↓
提取音频
  ↓
分析视频信息（时长、分辨率等）
```

### 2. 语音识别
```
音频文件
  ↓
语音识别（Whisper/其他 ASR）
  ↓
生成文字稿（带时间戳）
```

### 3. 字幕生成
```
文字稿 + 时间戳
  ↓
生成 SRT/VTT 字幕文件
  ↓
字幕样式配置
```

### 4. 标题提炼
```
完整文字稿
  ↓
AI 提炼关键信息
  ↓
生成多个标题选项
```

### 5. 视频生成
```
原视频 + 字幕文件
  ↓
FFmpeg 烧录字幕
  ↓
输出新视频
```

---

## ⚙️ 技术栈

### 核心依赖
- **FFmpeg** - 视频处理、字幕烧录
- **OpenAI Whisper** - 语音识别（可选）
- **Python** - 脚本处理

### 可选依赖
- **yt-dlp** - 下载视频
- **moviepy** - 视频编辑
- **stable-diffusion** - 生成封面图

---

## 📁 文件结构

```
skills/video-processor/
├── SKILL.md                 # 技能说明
├── README.md                # 使用文档
├── scripts/
│   ├── video_processor.py   # 主处理脚本
│   ├── speech_recognition.py # 语音识别模块
│   ├── subtitle_generator.py # 字幕生成模块
│   ├── title_extractor.py   # 标题提炼模块
│   └── video_renderer.py    # 视频渲染模块
├── references/
│   ├── subtitle_styles.md   # 字幕样式配置
│   └── title_templates.md   # 标题模板
├── output/                  # 输出目录
│   ├── subtitles/           # 字幕文件
│   ├── videos/              # 输出视频
│   └── titles/              # 标题文件
└── examples/                # 示例文件
```

---

## 🎨 配置说明

### 语音识别配置

```yaml
speech_recognition:
  # 识别引擎
  engine: "whisper"  # whisper | google | azure
  
  # 语言设置
  language: "zh"     # zh | en | ja | ko
  
  # 模型大小
  model: "base"      # tiny | base | small | medium | large
  
  # 输出格式
  output_format: "srt"  # srt | vtt | txt
```

### 字幕样式配置

```yaml
subtitle_style:
  # 字体设置
  font: "Arial"
  font_size: 24
  font_color: "white"
  
  # 边框设置
  border_color: "black"
  border_width: 2
  
  # 位置设置
  position: "bottom"  # top | bottom | center
  margin: 50
  
  # 背景设置
  background: true
  background_color: "black@0.5"  # 50% 透明黑色
```

### 标题提炼配置

```yaml
title_generation:
  # 标题风格
  style: "clickbait"  # normal | clickbait | professional
  
  # 标题长度
  max_length: 30
  
  # 生成数量
  count: 5
  
  # 包含元素
  include_emoji: true
  include_hashtags: true
```

---

## 📊 输出示例

### 生成的字幕文件 (SRT)

```srt
1
00:00:01,000 --> 00:00:03,500
大家好，今天我们来分享一个有趣的话题

2
00:00:03,500 --> 00:00:06,000
关于如何使用 AI 来处理视频内容

3
00:00:06,000 --> 00:00:09,000
这将大大提高我们的工作效率
```

### 提炼的标题

```
标题选项 1:
🔥 AI 自动处理视频，效率提升 10 倍！

标题选项 2:
📹 短视频自动加字幕，这个方法太神了！

标题选项 3:
💡 用 AI 提炼视频标题，解放双手！

标题选项 4:
🎬 视频处理神器，一键生成字幕 + 标题！

标题选项 5:
✨ 自媒体必备！AI 视频处理全流程！
```

### 输出文件结构

```
output/
└── video_20260323_153300/
    ├── original.mp4              # 原视频
    ├── audio.wav                 # 提取的音频
    ├── transcript.txt            # 完整文字稿
    ├── subtitles.srt             # SRT 字幕
    ├── subtitles.vtt             # VTT 字幕
    ├── titles.txt                # 提炼的标题
    ├── video_with_subtitles.mp4  # 带字幕视频
    └── thumbnail.jpg             # 视频封面
```

---

## 🔧 安装说明

### 1. 安装 FFmpeg

**Windows**:
```bash
# 使用 winget
winget install ffmpeg

# 或下载：https://ffmpeg.org/download.html
```

**macOS**:
```bash
brew install ffmpeg
```

**Linux**:
```bash
sudo apt install ffmpeg
```

### 2. 安装 Python 依赖

```bash
pip install openai-whisper
pip install moviepy
pip install yt-dlp
```

### 3. 安装 Whisper（可选）

```bash
# 使用 OpenAI Whisper
pip install openai-whisper

# 或使用 faster-whisper（更快）
pip install faster-whisper
```

---

## 🎯 使用示例

### 示例 1: 基础处理

```bash
# 提取字幕
python scripts/video_processor.py \
  --input "interview.mp4" \
  --extract-subtitles \
  --output "./output"
```

### 示例 2: 完整流程

```bash
# 完整处理
python scripts/video_processor.py \
  --input "course.mp4" \
  --output "./output" \
  --all
```

### 示例 3: 批量处理

```bash
# 批量处理视频
python scripts/video_processor.py \
  --input "./videos/" \
  --output "./output" \
  --batch
```

---

## ⚠️ 注意事项

### 视频格式
- ✅ 支持：MP4, MOV, AVI, MKV, WebM
- ⚠️ 建议：使用 MP4 格式

### 音频质量
- ✅ 清晰语音识别效果好
- ⚠️ 背景噪音会影响识别

### 字幕长度
- 每行不超过 30 字
- 每段不超过 2 行
- 显示时间 1-7 秒

### 处理时间
- 1 分钟视频 ≈ 1-3 分钟处理
- 取决于视频长度和配置

---

## 📚 相关文档

- `README.md` - 完整使用文档
- `references/subtitle_styles.md` - 字幕样式指南
- `references/title_templates.md` - 标题模板

---

## ✅ 功能清单

- [ ] 视频音频提取
- [ ] 语音识别转文字
- [ ] SRT/VTT 字幕生成
- [ ] 智能标题提炼
- [ ] 字幕烧录到视频
- [ ] 批量处理支持
- [ ] 多语言支持
- [ ] 封面图生成

---

**版本**: v1.0  
**创建日期**: 2026-03-23  
**状态**: ⏸️ 框架已完成，待实现
