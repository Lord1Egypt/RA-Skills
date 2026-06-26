# OpenClaw Skill - YouTube Transcript + Summary

> Forked and enhanced from [happynocode/openclaw-skill-youtube](https://github.com/happynocode/openclaw-skill-youtube)

Production-ready OpenClaw skill for YouTube video transcription and summarization.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/openclaw-compatible-green.svg)](https://openclaw.ai)

## Features

- ✅ **Reliable Transcript Fetching** - Dual-method approach bypasses YouTube rate limiting
- ✅ **Batch Processing** - Process multiple channels in one run
- ✅ **AI-Powered Summaries** - Generate structured, insightful summaries
- ✅ **3 Output Modes** - text-only / auto-insert / ai-review (configurable)
- ✅ **Cron-Friendly** - Built for automated daily runs
- ✅ **JSON Output** - Flexible integration with any agent or platform
- ✅ **Filters Shorts** - Skip videos under 5 minutes
- ✅ **Zero-config** - Works without any API key (Pollinations free tier)

> **B站视频说明**：此 Skill 仅支持 YouTube。B站视频建议使用 yt-dlp + faster-whisper 本地方案，效果更稳定。

## Quick Start

```bash
# Install
cd ~/.openclaw/workspace/skills
git clone https://github.com/mcdowell8023/oc-youtube-summarizer.git youtube-summarizer
cd youtube-summarizer
./setup.sh
# ↑ 安装完成后会引导你选择默认图文模式

# Re-configure mode anytime
./youtube-summarizer --setup

# Test single video
./youtube-summarizer --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# With explicit mode
./youtube-summarizer --url "https://b23.tv/xxx" --mode ai-review

# Scan channel (last 24 hours)
./youtube-summarizer --channel "UCSHZKyawb77ixDdsGog4iWA" --hours 24

# Daily batch (for cron)
./youtube-summarizer --config channels.json --daily --output /tmp/youtube_summary.json
```

## Output Modes

| Mode | Description | Extra Tokens |
|------|-------------|-------------|
| `text-only` | Text only, no frames | 0 |
| `auto-insert` | Fixed-rule frame selection, insert by timestamp | ~0 |
| `ai-review` ← **default** | AI-driven image selection based on article structure | ~5-8k |

Select mode at install time, or override anytime:
- `--mode <mode>` CLI flag
- `SUMMARY_MODE` env var
- `config/settings.json` → `default_mode`

## How It Works

### Transcript Fetching

Uses dual-method approach to ensure reliability:

1. **Primary**: innertube ANDROID client
   - Bypasses YouTube's rate limiting
   - Works reliably from various environments

2. **Fallback**: youtube-transcript-api
   - Automatic fallback if primary method fails

### Summary Generation

LLM fallback chain (fully environment variable driven, no config files needed):

1. `LLM_API_URL` + `LLM_API_KEY` + `LLM_MODEL` → custom endpoint
2. `OPENCLAW_GATEWAY_TOKEN` → OpenClaw local gateway
3. `GITHUB_TOKEN` / `GH_TOKEN` → GitHub Copilot API
4. `POLLINATIONS_API_KEY` → Pollinations API (with key)
5. Pollinations free anonymous call (no key required)

## Environment Variables

| 变量 | 用途 | 必须 |
|------|------|------|
| `LLM_API_URL` | 自定义 LLM API 端点 | 否 |
| `LLM_API_KEY` | 自定义 LLM API Key | 否 |
| `LLM_MODEL` | 自定义模型名 | 否 |
| `OPENCLAW_GATEWAY_TOKEN` | OpenClaw Gateway token | 否 |
| `GITHUB_TOKEN` | GitHub token（有 Copilot 订阅时可用） | 否 |
| `POLLINATIONS_API_KEY` | Pollinations API Key | 否 |

无需任何 Key 也可运行：转录功能不需要 API Key；摘要功能会尝试 Pollinations 免费匿名调用。

## Configuration

Create `channels.json`:

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

## Output Format

```json
{
  "generated_at": "2026-02-14T11:17:00Z",
  "items": [
    {
      "video_id": "dQw4w9WgXcQ",
      "title": "Video Title",
      "url": "https://youtube.com/watch?v=...",
      "channel": "Channel Name",
      "duration": "15:30",
      "published": "20260214",
      "has_transcript": true,
      "summary": "# Markdown summary...",
      "metadata": {
        "view_count": 12345,
        "like_count": 678
      }
    }
  ],
  "stats": {
    "total_videos": 5,
    "with_transcript": 4,
    "without_transcript": 1
  }
}
```

## OpenClaw Integration

### Cron Job Example

```yaml
schedule:
  kind: cron
  expr: "0 8 * * *"  # 8 AM daily
payload:
  kind: agentTurn
  message: |
    Run YouTube daily summary:
    
    1. Execute skill:
       youtube-summarizer --config channels.json --daily --output /tmp/summary.json
    
    2. Read output and process each video
    
    3. Send to Discord / Feishu / Telegram
```

## Dependencies

- `yt-dlp` - Video metadata extraction
- `youtube-transcript-api` - Transcript fetching (fallback)
- `innertube` - YouTube API client (primary method)
- Python 3.9+

All dependencies are installed automatically by `setup.sh`.

## Troubleshooting

### Transcript fetch fails
- Video may not have captions
- Check `has_transcript: false` in output

### Rate limiting
- Reduce `max_videos_per_channel` in config

### yt-dlp errors
- Update yt-dlp: `pip install -U yt-dlp`
- Check video is publicly accessible

## License

MIT License - Copyright (c) Contributors

## Acknowledgments

- [happynocode/openclaw-skill-youtube](https://github.com/happynocode/openclaw-skill-youtube) - Original skill
- [OpenClaw](https://openclaw.ai) - AI agent framework
- [innertube](https://github.com/tombulled/innertube) - YouTube API client
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube metadata extraction
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) - Transcript fetching

---

**Built for the OpenClaw community**
