# Seedance Video

Generate AI videos using ByteDance Seedance models for OpenClaw.

## Features

- 🎬 **Text-to-Video**: Generate videos from text prompts
- 🖼️ **Image-to-Video**: Animate from first frame or first+last frame
- 🎵 **Audio Support**: Generate videos with audio (Seedance 1.5 Pro)
- 🎨 **Draft Mode**: Quick preview generation
- 📊 **Task Management**: Query status and retrieve generated videos

## Prerequisites

- OpenClaw agent environment
- Python 3.8+
- Volcengine Ark API key

## Installation

### Via ClawHub (Recommended)

```bash
clawhub install seedance-video
```

### Manual Installation

1. Clone to `~/.openclaw/skills/seedance-video`
2. Set your API key:
   ```bash
   export ARK_API_KEY="your-api-key-here"
   ```

## Usage

Talk to your OpenClaw agent:

```
生成一个视频：海边日落，浪花拍打礁石
Generate a video from this prompt: a cat playing piano
查询视频生成任务状态: task-id-here
```

## Supported Models

- **Seedance 1.5 Pro**: Text/image to video with audio
- **Seedance 1.0 Pro**: Text/image to video
- **Seedance 1.0 Pro Fast**: Faster generation
- **Seedance 1.0 Lite**: Budget-friendly text-to-video

## License

MIT License - see [LICENSE.txt](LICENSE.txt) file
