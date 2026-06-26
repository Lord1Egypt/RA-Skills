---
name: video-batch-transcript
description: 通用视频批量转录工具 - 支持 1000+ 网站（B 站、YouTube、抖音、Twitch 等），使用 yt-dlp 批量下载视频音频，GPU 加速语音转文字（faster-whisper + CUDA），自动校正专业术语，生成结构化学习笔记。支持断点续传、批量导出、多格式输出、需要登录的网站配置。
---

# Video Batch Transcript

通用视频批量转录工具 - 支持 1000+ 网站

## 核心功能

- 🌐 **全网支持** - 基于 yt-dlp，支持 1000+ 网站（B 站、YouTube、抖音、Twitch 等）
- 📥 **批量下载** - 支持单视频、合集、播放列表、频道
- 🚀 **GPU 加速转录** - faster-whisper + CUDA，比 OpenAI Whisper 快 4-6 倍
- 📝 **结构化笔记** - 自动生成单集笔记 + 完整汇总
- 🔧 **术语校正** - 自动识别和校正专业术语
- 💾 **断点续传** - 支持中断后继续处理
- 📤 **多格式导出** - txt/md/docx，可选写入飞书文档
- 🔐 **登录支持** - 支持需要登录的网站（cookies 配置）

## 支持的网站

### 🇨🇳 国内平台
| 平台 | 支持类型 | 需要登录 |
|------|----------|----------|
| 哔哩哔哩 (Bilibili) | 视频、合集、频道 | 部分 |
| 抖音 (Douyin) | 视频、合集 | 部分 |
| 快手 (Kuaishou) | 视频 | 部分 |
| 西瓜视频 | 视频、合集 | 部分 |
| 腾讯视频 | 视频、剧集 | 部分 |
| 爱奇艺 | 视频、剧集 | 部分 |
| 优酷 | 视频、剧集 | 部分 |
| 微博视频 | 视频 | 否 |
| 小红书 | 视频 | 部分 |

### 🌍 国际平台
| 平台 | 支持类型 | 需要登录 |
|------|----------|----------|
| YouTube | 视频、播放列表、频道 | 部分 |
| Vimeo | 视频、合集 | 部分 |
| Dailymotion | 视频、播放列表 | 部分 |
| Twitch | 视频、频道 | 部分 |
| Twitter/X | 视频 | 否 |
| Instagram | 视频、Reels | 部分 |
| TikTok | 视频 | 部分 |
| Facebook | 视频 | 部分 |

### 📺 流媒体 (需登录)
- Netflix、Hulu、HBO、Disney+、Amazon Prime

### 🎵 音频平台
- SoundCloud、Bandcamp、Spotify、Apple Music

### 📚 教育平台
- Coursera、edX、Udemy、Khan Academy、TED

**完整支持列表**: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## 快速开始

### 1. 安装依赖

```bash
cd /root/.openclaw/workspace/skills/video-batch-transcript
pip install -r requirements.txt
```

### 2. 检查环境

```bash
python scripts/check_env.py
```

### 3. 基本使用

```bash
# YouTube 视频
python scripts/batch_transcript.py \
  --url "https://www.youtube.com/watch?v=xxx" \
  --output-dir "~/video-notes"

# B 站合集
python scripts/batch_transcript.py \
  --url "https://space.bilibili.com/xxx/channel/collectiondetail?sid=xxx" \
  --output-dir "~/video-notes"

# YouTube 播放列表
python scripts/batch_transcript.py \
  --url "https://www.youtube.com/playlist?list=xxx" \
  --output-dir "~/video-notes"
```

## 高级功能

### 1. 使用 Cookies（需要登录的网站）

```bash
# 从浏览器获取 cookies（推荐）
python scripts/batch_transcript.py \
  --url "https://www.youtube.com/watch?v=xxx" \
  --cookies-from-browser chrome

# 支持浏览器：chrome, firefox, safari, edge, brave, opera

# 或使用 cookies 文件
python scripts/batch_transcript.py \
  --url "https://www.netflix.com/title/xxx" \
  --cookies "cookies/netflix.txt"
```

### 2. 指定视频质量

```bash
# 下载最佳质量
python scripts/batch_transcript.py \
  --url "xxx" \
  --format "best"

# 下载 1080p
python scripts/batch_transcript.py \
  --url "xxx" \
  --format "bestvideo[height<=1080]+bestaudio/best[height<=1080]"

# 仅音频
python scripts/batch_transcript.py \
  --url "xxx" \
  --format "bestaudio"
```

### 3. 并行处理

```bash
# 使用 4 个进程并行处理
python scripts/batch_transcript.py \
  --url "xxx" \
  --workers 4
```

### 4. 断点续传

```bash
# 自动续传（默认）
python scripts/batch_transcript.py --url "xxx"

# 强制重新处理
python scripts/batch_transcript.py --url "xxx" --no-resume
```

## 配置选项

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--url` | 视频/合集 URL | **必填** |
| `--output-dir` | 输出目录 | `~/video-notes` |
| `--episodes` | 指定集数 (e.g., "1-5,8,10") | 全部 |
| `--model` | Whisper 模型 (tiny/base/small/medium/large) | `small` |
| `--device` | 设备 (auto/cuda/cpu) | `auto` |
| `--language` | 语言代码 (zh/en/ja 等) | `auto` |
| `--format` | 视频格式选择 | `bestaudio` |
| `--cookies-from-browser` | 浏览器 cookies | 无 |
| `--cookies` | cookies 文件路径 | 无 |
| `--terminology` | 术语表 JSON 文件路径 | 内置 |
| `--workers` | 并行处理数 | `1` |
| `--no-resume` | 禁用断点续传 | 否 |
| `--check-env` | 仅检查环境 | 否 |

### 配置文件

创建 `config/config.yaml`：

```yaml
# 默认输出目录
output_dir: ~/video-notes

# Whisper 模型设置
whisper:
  model: small
  device: auto  # auto/cuda/cpu
  language: auto  # auto/zh/en/ja 等
  compute_type: float16

# 下载设置
download:
  format: bestaudio  # 默认下载格式
  audio_format: mp3  # 音频输出格式
  audio_quality: 192  # 音频质量 (kbps)
  
  # Cookies 配置（可选）
  cookies:
    enabled: false
    browser: chrome  # chrome/firefox/safari/edge
    file: ""  # 或使用 cookies 文件路径

# 输出格式
export:
  formats: [md, txt]  # md/txt/docx
  include_timestamps: false
  include_summary: true

# 术语校正
terminology:
  enabled: true
  custom_file: ""

# 并行处理
parallel:
  workers: 1
  max_memory_gb: 8
```

## 使用示例

### 示例 1: YouTube 教程系列

```bash
# 下载整个播放列表并转录
python scripts/batch_transcript.py \
  --url "https://www.youtube.com/playlist?list=PLxxx" \
  --output-dir "~/youtube-ml-course" \
  --device cuda \
  --model medium
```

### 示例 2: B 站 UP 主频道

```bash
# 下载 UP 主所有视频
python scripts/batch_transcript.py \
  --url "https://space.bilibili.com/123/channel/collectiondetail?sid=456" \
  --output-dir "~/bilibili-ai-series" \
  --episodes "1-20"
```

### 示例 3: 抖音合集

```bash
# 下载抖音合集（可能需要 cookies）
python scripts/batch_transcript.py \
  --url "https://www.douyin.com/collection/xxx" \
  --output-dir "~/douyin-notes" \
  --cookies-from-browser chrome
```

### 示例 4: Twitch 频道视频

```bash
# 下载 Twitch 频道视频
python scripts/batch_transcript.py \
  --url "https://www.twitch.tv/xxx/videos" \
  --output-dir "~/twitch-vods" \
  --language en
```

### 示例 5: 多平台混合处理

```bash
# 创建脚本处理多个平台的视频
cat > process_all.sh << 'EOF'
#!/bin/bash

# YouTube
python scripts/batch_transcript.py \
  --url "https://youtube.com/playlist?list=xxx" \
  --output-dir "~/notes/youtube"

# B 站
python scripts/batch_transcript.py \
  --url "https://space.bilibili.com/xxx/collectiondetail?sid=xxx" \
  --output-dir "~/notes/bilibili"

# Vimeo
python scripts/batch_transcript.py \
  --url "https://vimeo.com/album/xxx" \
  --output-dir "~/notes/vimeo"
EOF

chmod +x process_all.sh
./process_all.sh
```

## 输出结构

```
~/video-notes/
├── 合集或频道名称/
│   ├── 001_视频标题/
│   │   ├── audio.mp3          # 音频文件
│   │   ├── transcript.txt     # 原始转录
│   │   ├── notes.md          # 结构化笔记
│   │   └── metadata.json      # 元数据（含来源网站）
│   ├── 002_视频标题/
│   │   └── ...
│   ├── 合集汇总.md            # 完整汇总笔记
│   └── metadata.json          # 合集元数据
```

## 网站特定配置

### YouTube

```bash
# 推荐：使用 cookies 避免 403 错误
python scripts/batch_transcript.py \
  --url "https://youtube.com/watch?v=xxx" \
  --cookies-from-browser chrome

# 下载字幕（如果有）
python scripts/batch_transcript.py \
  --url "https://youtube.com/watch?v=xxx" \
  --write-subs \
  --sub-langs zh-Hans,en
```

### B 站 (Bilibili)

```bash
# 普通视频（无需登录）
python scripts/batch_transcript.py \
  --url "https://www.bilibili.com/video/BVxxx"

# 需要登录的合集
python scripts/batch_transcript.py \
  --url "https://space.bilibili.com/xxx/collectiondetail?sid=xxx" \
  --cookies-from-browser chrome
```

### 抖音/TikTok

```bash
# 可能需要 cookies
python scripts/batch_transcript.py \
  --url "https://www.douyin.com/video/xxx" \
  --cookies-from-browser chrome
```

### Netflix/流媒体

```bash
# 需要 cookies 文件
# 1. 使用浏览器扩展导出 cookies
# 2. 保存为 netscape 格式
python scripts/batch_transcript.py \
  --url "https://www.netflix.com/title/xxx" \
  --cookies "cookies/netflix.txt"
```

## 模型选择建议

| 模型 | 显存需求 | 转录速度 | 准确率 | 适用场景 |
|------|----------|----------|--------|----------|
| tiny | ~1 GB | 最快 | 一般 | 快速测试、低配设备 |
| base | ~1 GB | 快 | 较好 | 日常使用 |
| small | ~2 GB | 中等 | 好 | **推荐默认** |
| medium | ~5 GB | 较慢 | 很好 | 高质量需求 |
| large | ~10 GB | 最慢 | 最佳 | 专业场景 |

## 故障排除

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| HTTP 403 | 网站阻止请求 | 使用 `--cookies-from-browser` |
| 需要登录 | 内容需认证 | 配置 cookies |
| 下载慢 | 网络问题 | 使用代理或 CDN |
| 转录错误 | 音频损坏 | 重新下载音频 |
| 内存不足 | 模型太大 | 使用更小模型或减少 workers |

### 获取 Cookies

**方法 1: 从浏览器自动获取（推荐）**
```bash
python scripts/batch_transcript.py \
  --url "xxx" \
  --cookies-from-browser chrome
```

**方法 2: 导出 cookies 文件**
1. 安装浏览器扩展（如 "Get cookies.txt"）
2. 登录目标网站
3. 导出 cookies 为 Netscape 格式
4. 使用 `--cookies "path/to/cookies.txt"`

### GPU 加速检查

```bash
# 检查 CUDA
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# 查看 GPU
nvidia-smi
```

## 更新日志

### v1.0.0 (2026-03-05)
- 初始版本
- 支持 1000+ yt-dlp 兼容网站
- GPU 加速转录 (faster-whisper)
- 结构化笔记生成
- 断点续传
- 多格式导出
- Cookies 登录支持

## 许可证

MIT License
