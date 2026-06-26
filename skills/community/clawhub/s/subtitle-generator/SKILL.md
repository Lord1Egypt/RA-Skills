---
name: subtitle-generator
description: 当用户需要生成字幕、制作字幕、字幕对齐、ASR识别、语音转文字时使用此技能。触发词：生成字幕, 字幕生成, 制作字幕, 视频字幕, 语音识别, ASR字幕, Whisper字幕, 字幕制作, 视频转字幕, 字幕对齐, 音频转字幕, 语音转文字, 自动字幕, ASR识别, faster-whisper, subtitle, subtitles, caption, transcription, speech to text
---

# Subtitle Generator / 字幕生成器

基于可插拔 ASR 引擎的多语言字幕生成技能，支持 Faster-Whisper（优先）和 OpenAI Whisper（兜底），自动检测 GPU 加速，支持 99+ 语言。

## ⚠️ 执行规则（强制，AI 必须遵守）

### 1. 必须后台直接执行，禁止委托子代理

字幕生成是纯执行任务，**禁止**使用 `sessions_spawn` 或子代理来执行命令，原因：
- 子代理消耗额外 tokens，纯属浪费
- 直接 `exec background:true` 效率最高

### 2. 执行模板

```bash
exec background:true command:"python3 ~/.openclaw/workspace/skills/subtitle-generator/scripts/main.py <视频文件> [srt|vtt] [语言] --notify"
```

**⚠️ 必须使用 `background:true`，禁止前台执行阻塞主窗口。**

### 3. 执行流程（强制顺序）

**步骤 0（首次自动）：** engines/__init__.py 在首次导入时自动检测 ~/.whisper-venv 是否存在，不存在时自动创建 venv 并安装依赖（faster-whisper 优先，openai-whisper 兜底），GPU 可用时自动启用 CUDA 加速。AI 无需手动干预。

1. 收到任务后**立即回复**用户：「🎬 字幕生成已启动（后台），完成后我会通知你。」
2. 使用 `exec background:true` 启动任务
3. 任务完成后（进程退出码为 0 或出错）**必须 kill 相关进程**
4. 通过 `openclaw system event --mode now` 唤醒 AI，再由 AI 使用 `message` 工具发送完成通知给用户
   - ⚠️ `openclaw system event` 只唤醒 AI，不发送 Telegram/Discord 等消息
   - ✅ 必须用 `message` 工具才能触达用户
5. 将字幕文件复制到视频同目录
6. 清理 `/tmp` 中的临时文件

### 4. 禁止行为

- ❌ `sessions_spawn` / 子代理执行此任务
- ❌ 前台执行 `exec command:"..."`（无 `background:true`）
- ❌ 不发送通知就结束会话
- ❌ 任务完成后不 kill 相关进程

### 5. AI 回复模板

任务启动时：
```
🎬 字幕生成已启动（后台），完成后我会通知你。
文件：xxx.mp4 | 格式：SRT | 语言：中文
```

Python 脚本输出 `【字幕生成完成】` 或 `【字幕生成失败】` 标记后，AI 被唤醒时使用 `message` 工具发送：

```python
message(
    action="send",
    # 不传 channel 参数，自动路由到用户当前所在的聊天平台
    message="✅ 字幕生成完成\n文件：xxx.srt | 条数：356\n路径：C:\\Users\\xxx\\Videos\\temp\\xxx.srt"
)
```

⚠️ **必须省略 `channel` 参数**，这样才能兼容所有 OpenClaw 支持的聊天工具（Telegram / Discord / WhatsApp / Slack 等）。

## 使用方法 / Usage

```bash
python ~/.openclaw/workspace/skills/subtitle-generator/scripts/main.py <video> [srt|vtt] [language] [--notify]
```

### 示例 / Examples

```bash
# English video, SRT subtitles
python ~/.openclaw/workspace/skills/subtitle-generator/scripts/main.py video.mp4 srt en --notify

# Japanese video, VTT subtitles
python ~/.openclaw/workspace/skills/subtitle-generator/scripts/main.py video.mp4 vtt ja --notify

# Chinese video, auto language detection
python ~/.openclaw/workspace/skills/subtitle-generator/scripts/main.py video.mp4 srt zh --notify

# Auto-detect any Whisper-supported language
python ~/.openclaw/workspace/skills/subtitle-generator/scripts/main.py video.mp4 srt --notify
```

### 支持语言 / Supported Languages

Whisper 支持 99+ 语言。常用语言代码：

| Code | Language |
|------|----------|
| `en` | English |
| `zh` | 中文 (Chinese) |
| `ja` | 日本語 (Japanese) |
| `ko` | 한국어 (Korean) |
| `fr` | Français |
| `de` | Deutsch |
| `es` | Español |
| `ru` | Русский |

不传语言参数 = 自动检测。

## GPU 加速 / GPU Acceleration

faster-whisper 使用 CTranslate2 作为推理引擎，运行时自动检测并启用 GPU：

| 系统 | GPU | 加速方式 | 说明 |
|------|-----|----------|------|
| Windows + NVIDIA | CUDA | cuDNN + CUDA | CTranslate2 自动加载 |
| macOS M1/M2/M3/M4 | Metal | Apple GPU | 需安装 Metal 版 CTranslate2（见下） |
| macOS Intel | CPU | — | 慢但可用 |
| Linux + NVIDIA | CUDA | cuDNN + CUDA | CTranslate2 自动加载 |
| CPU-only | — | 降级运行 | 所有平台均支持 |

### Apple Silicon (M系列) 安装 Metal 加速版

faster-whisper 默认不包含 Metal 加速，手动安装 Metal 版可获得显著提速：

```bash
# 先激活 venv，再安装 Metal 版 CTranslate2
~/.whisper-venv/bin/pip install \
  --extra-index-url https://download.pytorch.org/whl/metal \
  faster-whisper
```

安装后运行时日志会显示 `Using device Metal`，表示 Metal 加速已启用。

## 引擎优先级 / Engine Priority

| Priority | Engine | Notes |
|----------|--------|-------|
| 1 (preferred) | faster-whisper | CTranslate2, 2-4x faster, lower RAM |
| 2 (fallback) | openai-whisper | PyTorch, better compatibility |

Engine is auto-selected. No manual configuration needed.

## 输出 / Output

字幕文件生成在视频同目录：

```
video.mp4
video.srt   ← auto-generated
```

## 依赖项 / Dependencies

- `faster-whisper` or `openai-whisper` (auto-selected, auto-installed)
- `ffmpeg` (系统级，必须提前安装)
- `ffmpeg-python` (Python binding, auto-installed)

### ffmpeg 安装 / ffmpeg Installation

| 系统 | 安装命令 |
|------|----------|
| Windows | `winget install ffmpeg` 或 https://ffmpeg.org/download.html |
| macOS | `brew install ffmpeg` |
| Linux | `sudo apt install ffmpeg` 或 `sudo yum install ffmpeg` |

> ⚠️ ffmpeg 缺失时脚本会报错并给出对应系统的安装提示。
