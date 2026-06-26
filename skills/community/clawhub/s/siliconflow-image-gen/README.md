# SiliconFlow Image Generation Skill

Generate images using SiliconFlow API with support for FLUX.1, Stable Diffusion, and more.

## Features

- 🎨 **Multiple Models**: FLUX.1-schnell (free), FLUX.1-dev, Stable Diffusion 3.5
- 🔑 **Auto API Key Detection**: Reads from environment or OpenClaw config
- 💾 **Auto Download**: Saves generated images locally
- 📱 **OpenClaw Ready**: Designed for OpenClaw Agent integration

## Installation

```bash
# Via ClawHub
npx clawhub install siliconflow-image-gen

# Or manual
clone to ~/.openclaw/workspace/skills/siliconflow-image-gen
```

## Configuration

Set your SiliconFlow API key:

```bash
export SILICONFLOW_API_KEY="your-api-key"
```

Or the skill will auto-detect from `~/.openclaw/openclaw.json`

## Usage

### Command Line

```bash
# Generate with default model (FLUX.1-schnell)
python3 scripts/generate.py "A cup of coffee on wooden table"

# Specify model
python3 scripts/generate.py "Sunset over mountains" --model "black-forest-labs/FLUX.1-dev"

# Save to file
python3 scripts/generate.py "Cute cat" --output ~/Desktop/cat.png
```

### OpenClaw Agent

```
生成图片：一杯咖啡放在木质桌面上，温暖舒适的咖啡馆氛围
```

## Available Models

| Model | Cost | Quality | Speed |
|-------|------|---------|-------|
| `black-forest-labs/FLUX.1-schnell` | Free | Good | Fast |
| `black-forest-labs/FLUX.1-dev` | Paid | Excellent | Medium |
| `stabilityai/stable-diffusion-3-5-large` | Paid | Excellent | Medium |

## Author

MaxStorm Team

## License

MIT
