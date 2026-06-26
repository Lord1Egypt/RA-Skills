# Video Generation Skill

AI Video generation toolkit supporting both text-to-video and image-to-video generation using 40+ AI models.

## Features

- **Text to Video**: Generate videos from text prompts
- **Image to Video**: Animate static images into videos
- **Multiple Models**: Veo 3.1, Veo 3, Seedance 1.5 Pro, Wan 2.5, Grok Imagine Video, OmniHuman, and more
- **Auto Upload**: Automatically uploads local images to cloud storage for image-to-video generation

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install inference.sh CLI:
```bash
npm install -g @inference.sh/cli
# or
pip install inference-sh
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

### Text to Video

```bash
python scripts/text_to_video.py --prompt "A beautiful sunset over the ocean" --model veo-3.1
```

### Image to Video

```bash
python scripts/image_to_video.py --image path/to/image.jpg --prompt "Animate this image" --model veo-3.1
```

## Available Models

- `veo-3.1` - Google Veo 3.1 (recommended)
- `veo-3` - Google Veo 3
- `seedance-1.5-pro` - Seedance 1.5 Pro
- `wan-2.5` - Wan 2.5
- `grok-imagine-video` - Grok Imagine Video
- `omnihuman` - OmniHuman

## Output

Generated videos are saved to `./outputs/videos/` by default. The output includes the absolute path to the generated video file.
