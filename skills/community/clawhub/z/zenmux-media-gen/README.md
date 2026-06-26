# ZenMux Media Gen

Generate images and videos using ZenMux API - a unified API for multiple AI models.

## Features

- 🖼️ **Image Generation**: Support for multiple models including Gemini, Qwen, Hunyuan, GPT Image
- 🎞️ **Video Generation**: Google Veo 3.1 and ByteDance Seedance
- 🔑 **Single API Key**: Use one ZenMux API key for all models
- 📦 **Python Client**: Easy-to-use CLI tool

## Quick Start

1. Get your ZenMux API key from https://zenmux.ai
2. Set the environment variable:
   ```bash
   export ZENMUX_API_KEY="your-key"
   ```
3. Generate an image:
   ```bash
   python3 scripts/zenmux_media_client.py image \
     --model "google/gemini-2.5-flash-image" \
     --prompt "A cute panda" \
     --out panda.png
   ```

## Supported Models

See SKILL.md for the complete list of supported models.

## License

MIT
