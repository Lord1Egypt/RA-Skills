---
name: video-summarizer
description: Multi-platform video transcript extraction and AI-powered summarization (YouTube, Bilibili, extensible). Use when you need to summarize videos, extract transcripts, scan channels, or generate daily video digests.
metadata:
  author: mcdowell8023
  repo: https://github.com/mcdowell8023/oc-youtube-summarizer
---

# Video Summarizer Skill

多平台视频摘要工具，支持 YouTube 和 B站（未来可扩展更多平台），支持单个视频、频道扫描、每日批量处理。

## 功能

- ✅ 获取 YouTube 视频信息（yt-dlp）
- ✅ 提取字幕/transcript（youtube-transcript-api）
- ✅ **B站视频下载 + 语音转录**（yt-dlp + faster-whisper，本地，无需 API Key）
- ✅ **B站关键帧提取**（ffmpeg，每 30 秒一帧，供 agent 视觉分析）
- ✅ 生成深度摘要（LLM API）
- ✅ 输出 JSON 格式（agent 自行处理发送）
- ✅ 支持多频道配置
- ✅ 过滤 Shorts（< 5 分钟）
- 🔮 架构可扩展：新增平台只需添加 extractor 模块

## 安装

```bash
cd ~/.openclaw/skills/video-summarizer
./setup.sh
```

安装完成后会引导你选择默认图文模式（可随时重新配置）：

```
📋 选择默认图文模式:
  1) text-only    - 纯文字，不抽帧（最快）
  2) auto-insert  - 自动选帧插入文档（推荐平衡）
  3) ai-review    - AI 智能选图（默认，最佳效果，多消耗 ~5-8k token）
请选择 [1/2/3] (默认 3):
```

配置写入 `config/settings.json`，可随时运行 `video-summarizer --setup` 重新配置。

### 跨平台依赖安装

#### Linux（当前已支持）

```bash
sudo apt install ffmpeg
pip install faster-whisper yt-dlp youtube-transcript-api innertube
```

#### macOS

```bash
brew install ffmpeg
pip install faster-whisper yt-dlp youtube-transcript-api innertube
```

#### Windows

```bash
# 安装 ffmpeg（推荐 chocolatey 或 scoop）
choco install ffmpeg
# 或 scoop install ffmpeg

pip install faster-whisper yt-dlp youtube-transcript-api innertube
```

#### 注意事项

- **路径分隔符**：脚本已使用 `path.join()`，跨平台兼容
- **faster-whisper**：Windows 下需要 CUDA 或 CPU 模式（无 CUDA 时自动 fallback CPU，速度较慢）
- **Chrome cookies**：各平台路径不同，yt-dlp 会自动处理
- **Python 版本**：需要 Python 3.9+

### 核心依赖说明

| 依赖 | 用途 |
|------|------|
| `yt-dlp` | 视频下载、信息获取（YouTube + B站） |
| `youtube-transcript-api` | YouTube 字幕提取 |
| `innertube` | 绕过 YouTube API 限流 |
| `faster-whisper` | B站语音转文字（本地，无需 API） |
| `ffmpeg` | 音频提取 + 关键帧截取（系统级） |

## 工作原理

Skill 使用多种方法获取字幕，避免 YouTube 限流：

1. **innertube ANDROID client + Cloudflare proxy** - 主要方法，绕过限流
2. **youtube-transcript-api** - 备用方法

B站视频使用 yt-dlp 下载音频 → faster-whisper 本地转录，全程无需外部 API。

## 使用

### 三种图文模式

| 模式 | 说明 | 额外 token | 适用场景 |
|------|------|-----------|---------|
| `text-only` | 纯文字，不抽帧 | 0 | 快速摘要、纯文字需求 |
| `auto-insert` | 固定规则选帧，按时间戳插入（帧偏移+5s避转场） | ~0 | 平衡速度与图文效果 |
| `ai-review` ← **默认** | 基于文章结构反向选图，可补帧/删帧/替换 | ~5-8k | 最佳图文效果 |

**ai-review 流程（文章驱动选图）：**
1. Skill 抽帧 → 固定规则多选（~15-20帧，比最终需要多50%）
2. 先写纯文字版文档（分好章节）
3. 逐章判断：需要配图？→ 从已选帧匹配 / 补帧 / 跳过
4. 输出精选帧 + 画面描述 + 对应章节

**auto-insert 流程：**
1. Skill 抽帧 → 固定规则选帧（多选留余量）
2. 帧时间偏移 +5s（避开转场）
3. 按时间戳匹配章节，全部插入

通过以下方式指定模式（优先级从高到低）：
1. CLI 参数 `--mode`
2. 环境变量 `SUMMARY_MODE`
3. `config/settings.json` 中的 `default_mode`

### 1. 单个视频摘要（YouTube）

```bash
video-summarizer --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 2. B站视频摘要

```bash
video-summarizer --url "https://www.bilibili.com/video/BV1xxxxx"

# 短链接也支持（自动跟随跳转）
video-summarizer --url "https://b23.tv/xxxxx"

# 指定图文模式
video-summarizer --url "https://www.bilibili.com/video/BV1xxxxx" --mode text-only
video-summarizer --url "https://www.bilibili.com/video/BV1xxxxx" --mode auto-insert
video-summarizer --url "https://www.bilibili.com/video/BV1xxxxx" --mode ai-review

# 自定义 whisper 模型（精度更高，但更慢）
video-summarizer --url "https://www.bilibili.com/video/BV1xxxxx" --whisper-model large-v3

# 跳过关键帧提取（等效 --mode text-only）
video-summarizer --url "https://www.bilibili.com/video/BV1xxxxx" --no-frames

# 自定义关键帧间隔（默认30秒一帧）
video-summarizer --url "https://www.bilibili.com/video/BV1xxxxx" --frame-interval 60
```

### 3. 频道扫描（过去 24 小时）

```bash
video-summarizer --channel "UC_x5XG1OV2P6uZZ5FSM9Ttw" --hours 24
```

### 4. 每日批量处理（Cron 用）

```bash
video-summarizer --config /path/to/channels.json --daily --output /tmp/video_daily.json
```

## 配置文件格式

`channels.json`:
```json
{
  "channels": [
    {
      "name": "Lex Fridman",
      "id": "UCSHZKyawb77ixDdsGog4iWA",
      "url": "https://www.youtube.com/@lexfridman"
    },
    {
      "name": "Y Combinator",
      "id": "UCcefcZRL2oaA_uBNeo5UOWg",
      "url": "https://www.youtube.com/@ycombinator"
    }
  ],
  "hours_lookback": 24,
  "min_duration_seconds": 300,
  "max_videos_per_channel": 5
}
```

## 输出格式

```json
{
  "generated_at": "2026-02-14T11:17:00Z",
  "items": [
    {
      "title": "视频标题",
      "url": "https://youtube.com/watch?v=...",
      "video_id": "VIDEO_ID",
      "platform": "youtube",
      "channel": "频道名",
      "duration": "15:30",
      "published": "2026-02-14T08:00:00Z",
      "has_transcript": true,
      "summary": "# 摘要内容（markdown）\n\n### 🎯 核心问题..."
    },
    {
      "video_id": "BV1xxxxx",
      "title": "B站视频标题",
      "url": "https://www.bilibili.com/video/BV1xxxxx",
      "platform": "bilibili",
      "has_transcript": true,
      "transcript_path": "/tmp/bili_BV1xxxxx_transcript.txt",
      "frame_files": ["/tmp/bili_BV1xxxxx_frames/frame_001.jpg", "..."],
      "frame_count": 12,
      "summary": "# 摘要内容（markdown）..."
    }
  ],
  "stats": {
    "total_videos": 5,
    "with_transcript": 4,
    "without_transcript": 1
  }
}
```

## 环境变量

| 变量 | 用途 | 必须 |
|------|------|------|
| `LLM_API_URL` | 自定义 LLM API 端点 | 否 |
| `LLM_API_KEY` | 自定义 LLM API Key | 否 |
| `LLM_MODEL` | 自定义模型名 | 否 |
| `OPENCLAW_GATEWAY_TOKEN` | OpenClaw Gateway token | 否 |
| `GITHUB_TOKEN` | GitHub token（有 Copilot 订阅时可用） | 否 |
| `POLLINATIONS_API_KEY` | Pollinations API Key | 否 |
| `SUMMARY_MODE` | 图文模式：text-only / auto-insert / ai-review | 否 |
| `WHISPER_MODEL` | B站 whisper 模型大小（默认 small） | 否 |
| `FRAME_INTERVAL` | B站关键帧间隔秒数（默认 30） | 否 |
| `FRAME_TIME_OFFSET` | 帧时间戳偏移秒数，避开转场（默认 5） | 否 |

无需任何 Key 也可运行：转录功能不需要 API Key；摘要功能会尝试 Pollinations 免费匿名调用。

## 故障排查

### 字幕获取失败
- 视频可能没有字幕
- 输出 JSON 中 `has_transcript: false`
- Agent 应生成简短摘要（基于标题/描述）

### yt-dlp 限流
- 设置 `REQUEST_DELAY_SECONDS` (默认 3 秒)
- 减少 `max_videos_per_channel`
