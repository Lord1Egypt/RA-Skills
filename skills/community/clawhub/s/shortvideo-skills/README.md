# ShortVideo Skills

Create videos using ShortVideo API with Claude Code / OpenClaw skills.

A collection of Python scripts and Claude Code skills for generating marketing videos, ad videos, and replicating existing videos using the ShortVideo backend API.

## Features

- **Product to Video** - Generate marketing videos from product images using Sora2 AI
- **Image to Ad Video** - Create advertisement videos from 1-7 product images
- **Replicate Video** - Replicate existing video style with new product/model images

## Requirements

- Python 3.9+
- `requests` library

## Installation

### Option 1: Install as Claude Code Skill

Copy the `shortvideo-skills` directory to your Claude Code skills location:

```bash
cp -r shortvideo-skills ~/.claude/skills/
```

### Option 2: Use as Standalone Scripts

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-org/shortvideo-skills.git
cd shortvideo-skills
pip install -r requirements.txt
```

## Configuration

Set environment variables for API authentication:

```bash
export SHORTVIDEO_BASE_URL="https://api.shortvideo.ai"
export SHORTVIDEO_API_KEY="your-api-key-here"
```

Or add to `~/.claude/settings.json`:

```json
{
  "env": {
    "SHORTVIDEO_BASE_URL": "https://api.shortvideo.ai",
    "SHORTVIDEO_API_KEY": "your-api-key-here"
  }
}
```

## Usage

### Product to Video

Generate a marketing video from a single product image:

```bash
python3 scripts/product-to-video.py \
  --product-name "Premium Headphones" \
  --image https://example.com/product.jpg \
  --aspect-ratio 16:9 \
  --duration 12
```

**Parameters:**
| Parameter | Required | Valid Values | Description |
|-----------|----------|--------------|-------------|
| `--product-name` | Yes | - | Product name |
| `--image` | Yes | local/OSS/URL | Product image path |
| `--aspect-ratio` | Yes | `16:9`, `9:16` | Video ratio |
| `--duration` | Yes | `12` | Duration (only 12s supported) |
| `--product-info` | No | - | Product description |

**Credit Cost**: 100 (fixed)

---

### Image to Ad Video

Create advertisement videos from 1-7 product images:

```bash
python3 scripts/image-to-ad-video.py \
  --images product1.jpg product2.jpg \
  --duration 15 \
  --aspect-ratio 16:9
```

**Parameters:**
| Parameter | Required | Valid Values | Description |
|-----------|----------|--------------|-------------|
| `--images` | Yes | 1-7 paths | Image paths (local/OSS/URL) |
| `--duration` | Yes | `8`, `15`, `30`, `60` | Duration in seconds |
| `--aspect-ratio` | Yes | `16:9`, `9:16`, `1:1` | Video ratio |
| `--prompt` | No | max 2000 chars | Style prompt |

**Credit Cost**: 30 per second

---

### Replicate Video

Replicate an existing video style with new product/model images:

```bash
python3 scripts/replicate-video.py \
  --video template.mp4 \
  --aspect-ratio 16:9 \
  --resolution 1080p \
  --product-images product.jpg
```

**Parameters:**
| Parameter | Required | Valid Values | Description |
|-----------|----------|--------------|-------------|
| `--video` | Yes | local/OSS/URL | Source video (5-300s) |
| `--aspect-ratio` | Yes | `16:9`, `9:16` | Video ratio |
| `--resolution` | Yes | `540p`, `720p`, `1080p` | Output resolution |
| `--product-images` | No* | 1-7 paths | Product images |
| `--model-images` | No* | 1-7 paths | Model images |
| `--prompt` | No | max 2000 chars | Style prompt |
| `--remove-audio` | No | - | Remove audio |

*At least one image (product or model) is required.

**Credit Cost**: 9-15 per second (by resolution)

---

### Poll for Video Results

Check video generation status:

```bash
# Continuous polling
python3 scripts/poll-videos.py --video-ids video_abc123

# Single check
python3 scripts/poll-videos.py --video-ids video_abc123 --once
```

**Video Status Codes:**
| Status | Description |
|--------|-------------|
| 0 | Pending |
| 1 | Processing |
| 2 | Completed |
| 3 | Failed |

## File Path Types

All file parameters support:

| Type | Example | Behavior |
|------|---------|----------|
| Local file | `/Users/xxx/file.jpg` | Upload to OSS |
| OSS path | `d2mm4m9addr0008000a0.png` | Use directly |
| URL | `https://example.com/file.jpg` | Download → Upload |

## Supported File Types

| Type | Extensions | Max Size |
|------|------------|----------|
| Images | `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp` | 100MB |
| Videos | `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` | 100MB |

## API Response Format

```json
// Success
{"code": 0, "data": {...}}

// Failure
{"code": 1, "info": "error message"}
```

## Project Structure

```
shortvideo-skills/
├── SKILL.md                    # Claude Code skill definition
├── README.md                   # This file
├── LICENSE                     # MIT License
├── requirements.txt            # Python dependencies
├── scripts/
│   ├── impl.py                 # General API utilities
│   ├── product-to-video.py     # Product video generator
│   ├── image-to-ad-video.py    # Ad video generator
│   ├── replicate-video.py      # Video replicator
│   └── poll-videos.py          # Video status poller
├── references/
│   ├── product-to-video.md     # Product video documentation
│   ├── image-to-ad-video-v2.md # Ad video documentation
│   └── replicate-video.md      # Replicate video documentation
└── examples/
    └── example_usage.sh        # Example commands
```

## Claude Code Integration

When installed as a Claude Code skill, you can use natural language commands:

- "Create a product video from this image..."
- "Generate an ad video using these product images..."
- "Replicate this video with new product images..."

The skill will automatically:
1. Parse your request
2. Upload any local files or URLs
3. Create the video generation task
4. Poll for results
5. Display the final video URLs

## Error Handling

All scripts return JSON responses with status:

```json
{
  "status": "success",
  "task_id": "task_abc123",
  "video_ids": ["video_xyz789"]
}
```

On error:

```json
{
  "status": "error",
  "error": "Error message"
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Create an issue for bug reports or feature requests
- Check the [references/](references/) directory for detailed API documentation

## Acknowledgments

- Powered by ShortVideo API
- Video generation by Sora2 and Vidu AI