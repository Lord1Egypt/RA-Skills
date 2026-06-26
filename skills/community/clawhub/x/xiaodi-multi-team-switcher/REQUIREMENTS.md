# 系统要求

## 必需依赖

### 命令行工具

| 工具 | 版本要求 | 用途 | 安装命令 |
|------|----------|------|----------|
| `ffmpeg` | >= 4.0 | 视频压缩、转码、音频提取 | `apt install ffmpeg` / `brew install ffmpeg` |
| `ffprobe` | >= 4.0 | 视频信息分析 | 随 ffmpeg 安装 |
| `convert` | ImageMagick >= 7.0 | 图片处理、压缩、转换 | `apt install imagemagick` / `brew install imagemagick` |

### Python 包

| 包名 | 用途 | 安装命令 |
|------|------|----------|
| `requests` | HTTP 请求 | `pip install requests` |

## 可选依赖

### Python 包

| 包名 | 用途 | 安装命令 |
|------|------|----------|
| `akshare` | A股实时数据 | `pip install akshare` |
| `openai-whisper` | 语音识别、字幕生成 | `pip install openai-whisper` |
| `pillow` | 图片处理 | `pip install pillow` |

### 外部服务（需 API Key）

| 服务 | 环境变量 | 用途 | 获取方式 |
|------|----------|------|----------|
| 可灵 AI | `KLING_API_KEY` | AI 视频生成 | https://klingai.kuaishou.com |
| Runway | `RUNWAY_API_KEY` | AI 视频生成 | https://runwayml.com |
| Pika | `PIKA_API_KEY` | AI 视频生成 | https://pika.art |
| OpenAI | `OPENAI_API_KEY` | Sora/DALL-E | https://platform.openai.com |

## 权限要求

### OpenClaw 工具权限

| 工具 | 用途 | 风险等级 |
|------|------|----------|
| `web_search` | 网络搜索 | 低 |
| `web_fetch` | 获取网页内容 | 低 |
| `memory_search` | 搜索记忆 | 低 |
| `exec` | 执行系统命令 | 中（仅限媒体处理工具） |
| `browser` | 浏览器自动化 | 中（仅限公开网页） |

## 系统资源

| 资源 | 最低要求 | 推荐配置 |
|------|----------|----------|
| 内存 | 2GB | 4GB+ |
| 磁盘 | 1GB | 5GB+（视频处理需要更多临时空间） |
| CPU | 2核 | 4核+ |

## 验证安装

```bash
# 检查 ffmpeg
ffmpeg -version

# 检查 ImageMagick
convert -version

# 检查 Python 包
python3 -c "import requests; print('requests OK')"
```

## 故障排除

### ffmpeg 未找到

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

### ImageMagick 未找到

```bash
# Ubuntu/Debian
sudo apt install imagemagick

# macOS
brew install imagemagick
```

### Whisper 安装失败

Whisper 需要 Rust 编译环境：

```bash
# 安装 Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 然后安装 whisper
pip install openai-whisper
```