---
name: Vision Tool
slug: vision-tool
version: 1.1.3
description: Image recognition using Ollama + qwen3.5:4b with think=False for reliable content extraction.
author: HuRuilizhen
repository: https://github.com/HuRuilizhen/vision-tool
license: MIT
metadata:
  openclaw:
    emoji: "👁️"
    primaryEnv: ""
    requires:
      bins: ["ollama", "python3"]
      env: []
    channels: ["*"]  # All channels
    category: "vision"
    tags: ["image", "vision", "recognition", "ollama"]
---

# Vision Tool 👁️

Image recognition using Ollama + qwen3.5:4b. Uses /api/chat endpoint for direct content extraction.

## Features

✅ **Direct content extraction** - Uses /api/chat endpoint for clean output  
✅ **Simplified architecture** - No complex thinking field processing needed  
✅ **English prompts** - Optimized for English language analysis  
✅ **Multi-channel support** - Works in WeChat, Telegram, Discord, etc.  
✅ **Error handling** - Full error recovery and reporting  

## Installation

### Prerequisites
1. **Ollama service**: `ollama serve` (must be running)
2. **qwen3.5:4b model**: `ollama pull qwen3.5:4b`
3. **Python 3.8+**: Required for running the skill

### Install the skill
```bash
clawhub install vision-tool
```

### Development Setup (For Contributors)
If you want to contribute or modify the skill, see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development instructions.

Basic setup:
```bash
# Clone the repository
git clone https://github.com/HuRuilizhen/vision-tool
cd vision-tool

# Set up development environment
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Run tests
python3 -m pytest tests/
```

## Usage

### Basic usage
```bash
# From any OpenClaw channel
exec: python3 /path/to/vision-tool/main.py /path/to/image.jpg

# With custom prompt
exec: python3 /path/to/vision-tool/main.py /path/to/image.jpg --prompt "Describe this image"

# Debug output
exec: python3 /path/to/vision-tool/main.py /path/to/image.jpg --debug
```

### Channel-specific examples

**WeChat Channel:**
```bash
# When receiving an image
exec: python3 /path/to/vision-tool/main.py "$IMAGE_PATH"
```

**Telegram Channel:**
```bash
# Reply to photo messages
exec: python3 /path/to/vision-tool/main.py "/path/to/telegram_photo.jpg"
```

**Discord Channel:**
```bash
# Process attachments
exec: python3 /path/to/vision-tool/main.py "./discord_attachment.jpg"
```

## Example Output

```
Analysis (30.7s):
------------------------------------------------------------
The user wants a description of the image provided.
**1. Overall Composition:**
- It's a top-down view of a meal served on a white tray.
- There are six distinct dishes/bowls arranged...
**2. Detailed Breakdown of Dishes:**
- **Top Left:** A small white rectangular dish...
- **Top Middle:** A small white rectangular dish...
------------------------------------------------------------
```

## How It Works

1. **Image reading**: Reads and Base64 encodes the image
2. **API call**: Calls Ollama /api/chat endpoint with qwen3.5:4b
3. **Direct extraction**: Gets analysis directly from content field
4. **Fallback handling**: Simple cleanup if thinking field is used
5. **Output formatting**: Generates clean analysis results

## Performance

- **Average processing time**: 25-35 seconds per image (hardware dependent)
- **Image size support**: 100KB-500KB recommended
- **Token consumption**: ~2000 tokens per image
- **API endpoint**: Uses /api/chat for direct content access

## Troubleshooting

### Common Issues

1. **Ollama not running**: Run `ollama serve` first
2. **Model not installed**: Run `ollama pull qwen3.5:4b`
3. **Image path incorrect**: Use absolute paths or correct relative paths
4. **Timeout**: Model may take 30+ seconds for complex images

### Performance Tips

- Compress images to under 300KB for faster processing
- Use clear, concise prompts
- Ensure Ollama has sufficient system resources

## API Reference

### Python API
```python
from vision_core import VisionAnalyzer

analyzer = VisionAnalyzer()
result = analyzer.analyze_image("image.jpg", "Describe this image")
print(result["analysis"])
```

### Command Line
```bash
# Basic analysis
python3 main.py image.jpg

# Custom prompt
python3 main.py image.jpg --prompt "What objects are in this image?"

# Debug mode
python3 main.py image.jpg --debug
```

## Development

### File Structure
```
vision-tool/
├── SKILL.md          # This documentation
├── main.py           # Main skill script
├── scripts/
│   └── vision_core.py  # Core analysis engine
└── tests/
    └── test_basic.py   # Basic tests
```

### Testing
```bash
# Test with example image
python3 main.py /path/to/test.jpg --prompt "Test analysis"

# Run unit tests
python3 -m pytest tests/
```

## Changelog

### v1.1.0 (2026-04-13)
- Uses /api/chat endpoint for direct content extraction
- Simplified architecture without complex thinking field processing
- Default English prompt "Describe this image"
- Removed regex dependencies for cleaner code

### v1.0.0 (2026-04-12)
- Initial release

## Contributing

Issues and pull requests are welcome. Please ensure tests pass before submitting.

## License

This skill is part of the OpenClaw ecosystem.

---

**Ready to use in all OpenClaw channels!** 🚀