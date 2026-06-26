# Video Batch Transcript

通用视频批量转录工具 - 支持 1000+ 网站

## 功能特点

- 🌐 **全网支持** - 基于 yt-dlp，支持 1000+ 网站
- 📥 **批量下载** - 支持单视频、合集、播放列表、频道
- 🚀 **GPU 加速** - faster-whisper + CUDA，转录速度快 4-6 倍
- 📝 **智能笔记** - 自动生成结构化学习笔记
- 🔧 **术语校正** - 自动识别和校正专业术语
- 💾 **断点续传** - 支持中断后继续处理
- 📤 **多格式导出** - 支持 txt/md/docx 格式
- 🔐 **登录支持** - 支持需要登录的网站（cookies 配置）

## 支持的网站

### 🇨🇳 国内平台
- **哔哩哔哩** - 视频、合集、频道
- **抖音** - 视频、合集
- **快手** - 视频
- **西瓜视频** - 视频、合集
- **腾讯视频** - 视频、剧集
- **爱奇艺** - 视频、剧集
- **优酷** - 视频、剧集
- **微博视频** - 视频
- **小红书** - 视频

### 🌍 国际平台
- **YouTube** - 视频、播放列表、频道
- **Vimeo** - 视频、合集
- **Dailymotion** - 视频、播放列表
- **Twitch** - 视频、频道
- **Twitter/X** - 视频
- **Instagram** - 视频、Reels
- **TikTok** - 视频
- **Facebook** - 视频

### 📺 流媒体 (需登录)
- Netflix、Hulu、HBO、Disney+、Amazon Prime

### 🎵 音频平台
- SoundCloud、Bandcamp、Spotify

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

### 3. 处理视频

```bash
# YouTube 视频
python scripts/batch_transcript.py \
  --url "https://www.youtube.com/watch?v=xxx" \
  --output-dir "~/video-notes"

# B 站合集
python scripts/batch_transcript.py \
  --url "https://space.bilibili.com/xxx/channel/collectiondetail?sid=xxx" \
  --output-dir "~/video-notes"

# 使用 GPU 加速
python scripts/batch_transcript.py \
  --url "xxx" \
  --device cuda \
  --model medium
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--url` | 视频/合集 URL | **必填** |
| `--output-dir` | 输出目录 | `~/video-notes` |
| `--episodes` | 指定集数 (e.g., "1-5,8,10") | 全部 |
| `--model` | Whisper 模型 (tiny/base/small/medium/large) | `small` |
| `--device` | 设备 (auto/cuda/cpu) | `auto` |
| `--language` | 语言代码 (auto=自动检测) | `auto` |
| `--format` | 视频格式选择 | `bestaudio` |
| `--cookies-from-browser` | 浏览器 cookies (chrome/firefox/safari/edge/brave/opera) | 无 |
| `--cookies` | cookies 文件路径 | 无 |
| `--terminology` | 术语表 JSON 文件路径 | 内置 |
| `--workers` | 并行处理数 | `1` |
| `--no-resume` | 禁用断点续传 | 否 |
| `--check-env` | 仅检查环境 | 否 |

## 输出结构

```
~/video-notes/
├── youtube_合集名称/
│   ├── 001_视频标题/
│   │   ├── audio.mp3          # 音频文件
│   │   ├── transcript.txt     # 原始转录
│   │   ├── notes.md          # 结构化笔记
│   │   └── metadata.json      # 元数据
│   ├── 002_视频标题/
│   │   └── ...
│   ├── 合集汇总.md            # 完整汇总笔记
│   └── metadata.json          # 合集元数据
```

## 模型选择建议

| 模型 | 显存需求 | 转录速度 | 准确率 | 适用场景 |
|------|----------|----------|--------|----------|
| tiny | ~1 GB | 最快 | 一般 | 快速测试、低配设备 |
| base | ~1 GB | 快 | 较好 | 日常使用 |
| small | ~2 GB | 中等 | 好 | **推荐默认** |
| medium | ~5 GB | 较慢 | 很好 | 高质量需求 |
| large | ~10 GB | 最慢 | 最佳 | 专业场景 |

## GPU 加速

### CUDA 要求

- NVIDIA GPU (支持 CUDA)
- CUDA Toolkit 11.8+
- PyTorch CUDA 版本

### 安装 CUDA 版 PyTorch

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### 检查 GPU 状态

```bash
nvidia-smi
```

## Cookies 配置（需要登录的网站）

### 方法 1: 从浏览器自动获取（推荐）

```bash
# Chrome
python scripts/batch_transcript.py \
  --url "https://youtube.com/watch?v=xxx" \
  --cookies-from-browser chrome

# Firefox
python scripts/batch_transcript.py \
  --url "xxx" \
  --cookies-from-browser firefox
```

### 方法 2: 使用 cookies 文件

1. 安装浏览器扩展（如 "Get cookies.txt"）
2. 登录目标网站
3. 导出 cookies 为 Netscape 格式
4. 使用 `--cookies` 参数

```bash
python scripts/batch_transcript.py \
  --url "https://www.netflix.com/title/xxx" \
  --cookies "cookies/netflix.txt"
```

## 网站特定提示

### YouTube
- 推荐使用 `--cookies-from-browser chrome` 避免 403 错误
- 支持播放列表、频道、订阅

### B 站
- 普通视频无需登录
- 部分合集需要 cookies

### 抖音/TikTok
- 通常需要 cookies
- 支持合集处理

### Netflix/流媒体
- 必须提供 cookies 文件
- 使用浏览器扩展导出

## 故障排除

### 下载失败
- 检查网络连接
- 尝试使用代理
- 更新 yt-dlp: `pip install -U yt-dlp`
- 使用 cookies

### 转录错误
- 检查音频文件是否完整
- 尝试使用更大的模型
- 确保内存充足

### GPU 不可用
- 检查 `nvidia-smi` 输出
- 确认 CUDA Toolkit 已安装
- 重新安装 CUDA 版 PyTorch

## 更多示例

详见 `examples/usage_examples.md`

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
