---
name: video-subtitle-skill
description: 为视频/音频自动生成字幕，支持多语言识别、翻译、说话人分离、字幕烧入视频
---

# 视频字幕生成器 (Video Subtitle Generator)

基于 SenseAudio ASR API，为视频或音频文件自动生成字幕。

## 核心功能

1. **语音识别** — 自动识别视频/音频中的语音内容，生成带时间戳的字幕
2. **多语言支持** — 支持中文、英文、日文、韩文等 20+ 种语言
3. **字幕翻译** — 识别后可自动翻译成目标语言
4. **说话人分离** — 多人对话场景自动区分不同说话人
5. **字幕烧入** — 将生成的字幕直接烧入视频输出新文件
6. **多格式输出** — 支持 SRT / VTT / TXT / JSON 格式

## 使用方式

用户说出类似以下请求时触发此 Skill：
- "帮我给这个视频加字幕"
- "识别这个音频的内容并生成字幕"
- "把这个英文视频翻译成中文字幕"
- "帮我总结一下这个视频讲了什么"

## 执行步骤

### 第一步：检查 API 密钥

```bash
echo "SENSEAUDIO_API_KEY=$SENSEAUDIO_API_KEY"
```

**如果 `SENSEAUDIO_API_KEY` 为空，必须先向用户询问，说明在 https://senseaudio.cn 注册获取。不要直接运行脚本让它报错。**

### 第二步：运行脚本生成字幕

```bash
# 基础用法
python scripts/video_subtitle.py "/path/to/video.mp4" --output outputs/

# 指定语言 + 翻译
python scripts/video_subtitle.py "/path/to/video.mp4" --language zh --translate en

# 生成字幕并烧入视频
python scripts/video_subtitle.py "/path/to/video.mp4" --burn --font-size 28

# 说话人分离
python scripts/video_subtitle.py "/path/to/meeting.mp4" --model pro --speaker
```

注意：如果环境变量 `SENSEAUDIO_API_KEY` 已设置，无需 `--senseaudio-api-key`。

### 第三步：内容总结（如用户需要）

脚本会输出纯文本转写结果（`*.txt`）。如果用户需要视频内容总结，**你（Claude）直接读取这个 txt 文件并总结**，不需要调用外部 LLM。

### 第四步：返回结果

将生成的字幕文件路径（和烧入后的视频路径）返回给用户。

## ASR 模型选择

| 模型 | 参数值 | 特点 | 适用场景 |
|------|--------|------|---------|
| 极速版 | `lite` | 毫秒级响应、30+ 语言 | 低成本批量转写 |
| 标准版 | `standard` | 功能全面、性价比高 | **通用转写、视频字幕（推荐）** |
| 专业版 | `pro` | 高精度、说话人分离 | 会议记录、访谈、多人场景 |
| 深度版 | `deepthink` | 智能纠错、方言增强 | 方言/术语较多的场景 |

## 环境要求

- Python 3.10+，依赖：`requests`
- 系统依赖：`ffmpeg`（音频提取和字幕烧入）、`fonts-noto-cjk`（中日韩字幕烧入需要）
- `SENSEAUDIO_API_KEY` — SenseAudio API 密钥（唯一需要的密钥）

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 输入视频/音频文件路径（必填） | - |
| `--output` | 输出目录 | 输入文件同级 subtitle_output/ |
| `--model` | ASR 模型 (lite/standard/pro/deepthink) | standard |
| `--language` | 音频语言代码 (zh/en/ja 等) | 自动检测 |
| `--translate` | 翻译目标语言代码 | 不翻译 |
| `--speaker` | 启用说话人分离 | 否 |
| `--sentiment` | 启用情感分析 | 否 |
| `--burn` | 将字幕烧入视频 | 否 |
| `--font-size` | 烧入字幕字体大小 | 24 |
| `--format` | 字幕格式 (srt/vtt/both) | srt |
| `--senseaudio-api-key` | SenseAudio API 密钥 | 环境变量 |

## 输出文件

| 文件 | 说明 |
|------|------|
| `文件名.srt` | SRT 格式字幕 |
| `文件名.vtt` | VTT 格式字幕（需指定 --format vtt/both） |
| `文件名.txt` | 纯文本转写结果 |
| `文件名_detail.json` | 详细识别结果（含时间戳、说话人等） |
| `文件名_subtitled.mp4` | 烧入字幕的视频（需指定 --burn） |

## 支持的语言代码

zh(中文) en(英文) ja(日文) ko(韩文) fr(法语) de(德语) es(西班牙语) pt(葡萄牙语) ru(俄语) it(意大利语) ar(阿拉伯语) yue(粤语) nl(荷兰语) id(印尼语) ms(马来语) th(泰语) tr(土耳其语) vi(越南语) 等
