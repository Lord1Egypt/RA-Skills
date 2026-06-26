# Video Generator Skill

Automated text-to-video generation system with multi-provider TTS/ASR support.

## Version

**Current Version**: v1.3.1

## What's New in v1.3.1

### Critical Bug Fixes
- Fixed Aliyun ASR timestamp sync issue (0% error, was -75%)
- Added smart text segmentation for Aliyun ASR (6 segments vs 1)
- Fixed OpenAI Whisper data format bug
- Improved subtitle display effect significantly

## Features

- Multi-provider TTS/ASR support (OpenAI, Azure, Aliyun, Tencent)
- Automatic fallback mechanism
- Smart text segmentation
- Precise timestamp synchronization
- Background video support
- Cyber wireframe visual effects
- Fully automated pipeline

## Quick Start

### Installation

```bash
# Install via npm
npm install -g openclaw-video-generator

# Or via ClawHub
clawhub install ZhenStaff/video-generator
```

### Basic Usage

```bash
# Generate video from text script
openclaw-video-generator script.txt --voice nova --speed 1.15

# With background video
openclaw-video-generator script.txt \
  --voice Aibao \
  --bg-video background.mp4 \
  --bg-opacity 0.4
```

## Configuration

### Environment Variables

```bash
# OpenAI (default)
export OPENAI_API_KEY="your-key"

# Aliyun (optional)
export ALIYUN_ACCESS_KEY_ID="your-id"
export ALIYUN_ACCESS_KEY_SECRET="your-secret"
export ALIYUN_APP_KEY="your-app-key"

# Azure (optional)
export AZURE_SPEECH_KEY="your-key"
export AZURE_SPEECH_REGION="your-region"

# Tencent (optional)
export TENCENT_SECRET_ID="your-id"
export TENCENT_SECRET_KEY="your-key"
export TENCENT_APP_ID="your-app-id"
```

### Provider Priority

```bash
# Set provider priority (default: openai,azure,aliyun,tencent)
export TTS_PROVIDERS="aliyun,openai,azure,tencent"
export ASR_PROVIDERS="openai,aliyun,azure,tencent"
```

## Commands

### Generate Video

```bash
openclaw-video-generator <script.txt> [options]
```

**Options:**
- `--voice <name>` - TTS voice (default: nova)
  - OpenAI: alloy, echo, nova, shimmer
  - Aliyun: Aibao, Aiqi, Aimei, etc.
- `--speed <number>` - TTS speed (0.25-4.0, default: 1.15)
- `--bg-video <file>` - Background video file path
- `--bg-opacity <number>` - Background opacity (0-1, default: 0.3)
- `--bg-overlay <color>` - Overlay color (default: rgba(10,10,15,0.6))

### Examples

```bash
# Simple generation
openclaw-video-generator my-script.txt

# Custom voice and speed
openclaw-video-generator my-script.txt --voice Aibao --speed 1.2

# With background video
openclaw-video-generator my-script.txt \
  --voice nova \
  --bg-video backgrounds/tech/video.mp4 \
  --bg-opacity 0.4
```

## Output

The command generates:
- `audio/<name>.mp3` - TTS audio file
- `audio/<name>-timestamps.json` - Timestamp data
- `src/scenes-data.ts` - Scene configuration
- `out/<name>.mp4` - Final video (1080x1920, 30fps)

## Performance

- Video generation: ~2 minutes for 20-second video
- Resolution: 1080x1920 (vertical)
- Frame rate: 30 fps
- Bitrate: ~4.6 Mbps
- Concurrency: 6x rendering

## Troubleshooting

### Audio/Subtitle Sync Issues
✅ **Fixed in v1.3.1** - Timestamps now use ffprobe for precise detection

### Single Segment Display
✅ **Fixed in v1.3.1** - Smart segmentation generates multiple segments

### Provider Failures
- Check API credentials in environment variables
- Verify provider priority settings
- System automatically falls back to next provider

## Links

- **GitHub**: https://github.com/ZhenRobotics/openclaw-video-generator
- **npm**: https://www.npmjs.com/package/openclaw-video-generator
- **Issues**: https://github.com/ZhenRobotics/openclaw-video-generator/issues
- **Documentation**: See GitHub repository for detailed docs

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check GitHub Issues
2. Read documentation in repository
3. Create new issue with details

---

**Version**: v1.3.1
**Last Updated**: 2026-03-11
**Maintainer**: ZhenStaff
