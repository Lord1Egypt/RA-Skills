# 🎬 短视频自动处理技能 - 使用指南

**版本**: v2.1  
**创建日期**: 2026-03-23  
**最后更新**: 2026-03-24

---

## ✨ 功能概述

自动处理短视频，实现：
- 🎙️ **语音识别** - 自动提取音频并识别为文字（支持 Whisper/faster-whisper）
- 📝 **字幕生成** - 生成 SRT 格式字幕（时间戳与人声精确同步）
- 🎯 **标题提炼** - 智能提炼吸引人的标题
- 📺 **字幕添加** - 将字幕烧录到视频
- 🎬 **视频生成** - 输出带字幕的新视频
- ✏️ **后处理** - 支持修改文字稿后重新生成
- 🎨 **样式配置** - 自定义字幕字体、颜色、大小、位置

---

## 🏆 推荐配置

**对于正式内容，推荐使用 medium 模型**：

```bash
python scripts/video_processor.py -i "video.mp4" -m "medium"
```

**准确度对比**（测试视频：2 分 35 秒）：

| 模型 | 准确度 | 处理时间 | 推荐场景 |
|------|--------|----------|----------|
| medium | ⭐⭐⭐⭐⭐ | ~3 分钟 | 正式内容、专业制作 |
| small | ⭐⭐⭐⭐ | ~1.5 分钟 | 较高精度需求 |
| base | ⭐⭐⭐ | ~45 秒 | 日常使用、快速处理 |
| tiny | ⭐⭐ | ~30 秒 | 仅测试 |

---

## 🔄 完整工作流程

### 步骤 1: 初次处理

```bash
python scripts/video_processor.py -i "video.mp4" -m "medium"
```

### 步骤 2: 编辑文字稿（修正错别字）

用文本编辑器打开 `output_medium/xxx/transcript.txt`，修正错别字后保存。

### 步骤 3: 重新生成（可选）

```bash
# 使用默认样式
python scripts/subtitle_processor.py \
  -t "output_medium/xxx/transcript_fixed.txt" \
  -v "video.mp4" \
  -o "./final"

# 使用自定义样式
python scripts/subtitle_processor.py \
  -t "output_medium/xxx/transcript_fixed.txt" \
  -v "video.mp4" \
  -o "./final" \
  -s "my_style.json"
```

---

## 🎨 字幕样式配置

### 快速使用

```json
{
  "font": "Microsoft YaHei",
  "fontsize": 28,
  "primary_color": "&H0000FFFF",
  "bold": 1,
  "border_style": 1,
  "outline": 3,
  "alignment": 2
}
```

### 预设样式

- `subtitle_style_template.json` - 完整模板
- `demo_style.json` - 黄色综艺字幕演示

详细配置见：`字幕后处理完整指南.md`

---

## 🚀 快速开始

### 1. 安装依赖

**安装 FFmpeg** (必需):

**Windows**:
```bash
# 使用 winget
winget install ffmpeg

# 或下载：https://ffmpeg.org/download.html
# 添加到系统 PATH
```

**macOS**:
```bash
brew install ffmpeg
```

**Linux**:
```bash
sudo apt install ffmpeg
```

---

### 🔧 安装语音识别引擎（可选但推荐）

**无 Whisper 时**：程序使用模拟模式生成示例字幕（用于测试）

**安装 faster-whisper**（推荐，更快）:
```bash
pip install faster-whisper
```

**或安装 openai-whisper**:
```bash
pip install openai-whisper
```

**模型大小选择**:
- `tiny` - 最快，适合测试（约 75MB）
- `base` - 平衡速度与精度（约 142MB）← 默认
- `small` - 更高精度（约 244MB）
- `medium` - 高精度（约 769MB）
- `large` - 最高精度（约 1550MB）

---

### 2. 基础使用

```bash
cd skills/video-processor

# 处理单个视频
python scripts/video_processor.py \
  --input "video.mp4" \
  --output "./output"
```

---

## 📋 完整流程

### 处理步骤

```
1. 输入视频
   ↓
2. 提取音频 (FFmpeg)
   ↓
3. 语音识别 → 文字稿
   ↓
4. 生成字幕 (SRT/VTT)
   ↓
5. 提炼标题
   ↓
6. 烧录字幕到视频
   ↓
7. 输出成品视频
```

### 命令行示例

```bash
# 完整处理流程
python scripts/video_processor.py \
  --input "input/interview.mp4" \
  --output "./output"
```

---

## 📁 输出文件

处理后会生成以下文件：

```
output/video_20260323_153300/
├── audio.wav                    # 提取的音频
├── transcript.txt               # 完整文字稿
├── subtitles.srt                # SRT 字幕文件
├── subtitles.vtt                # VTT 字幕文件
├── titles.txt                   # 提炼的标题
├── video_with_subtitles.mp4     # 带字幕视频
└── info.json                    # 视频信息
```

---

## 🎨 输出示例

### 1. SRT 字幕文件

```srt
1
00:00:01,000 --> 00:00:04,000
大家好，欢迎观看本期视频

2
00:00:04,000 --> 00:00:07,000
今天我们要分享一个非常实用的技巧

3
00:00:07,000 --> 00:00:10,000
关于如何自动处理短视频内容

4
00:00:10,000 --> 00:00:13,000
这将大大提高我们的工作效率
```

### 2. 提炼的标题

```
视频标题选项：

1. 🔥 短视频自动处理，效率提升 10 倍！
2. 📹 AI 自动加字幕，这个方法太神了！
3. 💡 用 AI 提炼标题，解放双手！
4. 🎬 视频处理神器，一键生成！
5. ✨ 自媒体必备！AI 视频处理！
```

### 3. 文字稿

```
[00:00:01] 大家好，欢迎观看本期视频
[00:00:03] 今天我们要分享一个非常实用的技巧
[00:00:06] 关于如何自动处理短视频内容
[00:00:09] 这将大大提高我们的工作效率
[00:00:12] 让我们开始吧
```

---

## ⚙️ 配置选项

### 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| --input | -i | 输入视频文件 | 必需 |
| --output | -o | 输出目录 | ./output |

### 字幕样式（待实现）

```yaml
subtitle:
  font: "Arial"
  font_size: 24
  font_color: "white"
  border_color: "black"
  position: "bottom"
  background: true
```

### 标题风格（待实现）

```yaml
title:
  style: "clickbait"  # normal | clickbait | professional
  max_length: 30
  count: 5
  include_emoji: true
```

---

## 🎯 使用场景

### 1. 自媒体二次创作

```bash
# 处理下载的视频
python scripts/video_processor.py \
  --input "downloaded_video.mp4" \
  --output "./output"
```

**输出**:
- ✅ 带字幕视频
- ✅ 文字稿
- ✅ 多个标题选项

### 2. 课程视频处理

```bash
# 批量处理课程视频
python scripts/video_processor.py \
  --input "./courses/" \
  --output "./output" \
  --batch
```

**输出**:
- ✅ 每节课带字幕
- ✅ 课程文字稿
- ✅ 章节标题

### 3. 访谈/会议记录

```bash
# 处理会议录像
python scripts/video_processor.py \
  --input "meeting.mp4" \
  --output "./output"
```

**输出**:
- ✅ 会议文字记录
- ✅ 带时间戳字幕
- ✅ 关键要点提炼

---

## 🔧 高级功能

### 语音识别引擎

**当前**: 模拟模式（演示用）

**计划支持**:
- OpenAI Whisper
- Google Speech-to-Text
- Azure Speech Service
- 百度语音识别

### 字幕格式

**支持**:
- ✅ SRT (SubRip)
- ✅ VTT (WebVTT)
- ⏸️ ASS/SSA (高级字幕)

### 视频格式

**支持**:
- ✅ MP4
- ✅ MOV
- ✅ AVI
- ✅ MKV
- ✅ WebM

---

## ⚠️ 注意事项

### 视频要求
- ✅ 格式：MP4/MOV/AVI/MKV/WebM
- ✅ 大小：<500MB（建议）
- ✅ 时长：<60 分钟（建议）

### 音频质量
- ✅ 清晰语音识别效果好
- ⚠️ 背景噪音会影响识别
- ⚠️ 音乐/音效会干扰识别

### 字幕规范
- 每行不超过 30 字
- 每段不超过 2 行
- 显示时间 1-7 秒
- 与语音同步

### 处理时间
- 1 分钟视频 ≈ 1-3 分钟处理
- 取决于视频长度和配置
- 受硬件性能影响

---

## 🐛 常见问题

### Q: FFmpeg 未安装？
**A**: 
```bash
# Windows
winget install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

### Q: 识别不准确？
**A**: 
- 确保音频清晰
- 减少背景噪音
- 使用高质量音源
- 考虑使用专业 ASR 服务

### Q: 字幕不同步？
**A**: 
- 检查视频帧率
- 调整字幕时间偏移
- 手动校准时间轴

### Q: 处理速度慢？
**A**: 
- 降低视频分辨率
- 使用 GPU 加速
- 分段处理长视频

---

## 📚 相关文件

```
skills/video-processor/
├── SKILL.md                 # 技能说明
├── README.md                # 本文档
├── scripts/
│   └── video_processor.py   # 主处理脚本
├── output/                  # 输出目录
└── examples/                # 示例文件
```

---

## 🚀 下一步计划

### 短期（1 周）
- [ ] 集成 Whisper 语音识别
- [ ] 支持批量处理
- [ ] 优化字幕样式

### 中期（1 月）
- [ ] 多语言支持
- [ ] 字幕翻译功能
- [ ] 封面图生成

### 长期（3 月）
- [ ] 视频剪辑功能
- [ ] 自动配音
- [ ] 多平台发布

---

## ✅ 功能清单

- [x] 视频音频提取
- [x] 模拟文字稿生成
- [x] SRT 字幕生成
- [x] 标题提炼
- [x] 字幕烧录视频
- [ ] Whisper 语音识别
- [ ] 批量处理
- [ ] 多语言支持
- [ ] 字幕翻译
- [ ] 封面图生成

---

## 📞 使用示例

### 示例 1: 处理单个视频

```bash
python scripts/video_processor.py \
  -i "my_video.mp4" \
  -o "./output"
```

### 示例 2: 查看帮助

```bash
python scripts/video_processor.py --help
```

### 示例 3: 检查 FFmpeg

```bash
ffmpeg -version
```

---

**版本**: v1.0  
**创建日期**: 2026-03-23  
**状态**: ✅ 框架已完成  
**下一步**: 集成真实语音识别
