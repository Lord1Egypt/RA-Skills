# Vision Tool 👁️

Image recognition tool using Ollama + qwen3.5:4b. Automatically cleans thinking field output for clean analysis results.

## Features

✅ **Multi-channel support** - Works in WeChat, Telegram, Discord, etc.  
✅ **Smart cleaning** - Automatically processes qwen3.5:4b's thinking field  
✅ **Easy to use** - One command to analyze images  
✅ **High-quality output** - Clean, detailed analysis results  
✅ **Error handling** - Full error recovery and reporting  

## Quick Start

### Installation
```bash
clawhub install vision-tool
```

### Prerequisites
1. **Ollama service**: `ollama serve` (must be running)
2. **qwen3.5:4b model**: `ollama pull qwen3.5:4b`
3. **Python dependencies**: `pip install requests`

### Basic Usage
```bash
# Analyze an image
vision-tool path/to/image.jpg

# With custom prompt
vision-tool image.jpg --prompt "Describe this image in detail"

# JSON output
vision-tool image.jpg --json
```

## Documentation

Full documentation is available in [SKILL.md](SKILL.md).

## Development

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/vision-tool.git
cd vision-tool

# Install dependencies
pip install -e .
```

### Testing
```bash
# Run tests
python -m pytest tests/
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.