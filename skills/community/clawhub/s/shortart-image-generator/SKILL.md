---
name: shortart-image-generator
description: "Generate images using ShortArt AI platform with three modes: (1) Text-to-image and image-to-image generation for general artwork creation, (2) E-commerce suit images for product photography and Amazon listings, (3) Template-based image generation with customizable parameters. REQUIRES: SHORTART_API_KEY environment variable (get from https://shortart.ai/home). Use when users explicitly request: creating images, drawing, generating pictures, making artwork, product images, suit images, template images, or visual content creation using ShortArt. Triggers on: 生成图片, 画一张, 帮我画, 制作图片, 套图, 生成套图, 主图, 商品主图, 模版生图, 用模版生成图片, 推荐模版, generate image, create image, draw, visualize, suit image, product main image, template image generation, image-to-image, 以图生图."
homepage: https://shortart.ai
allowed-tools: Bash(python3 *)
metadata: {"openclaw": {"emoji": "🎨", "requires": {"env": ["SHORTART_API_KEY"]}, "primaryEnv": "SHORTART_API_KEY"}, "dependencies": {"python": ">=3.7", "pip": ["requests"]}}
compatibility: "Requires Python 3.7+, requests library (pip install requests), and SHORTART_API_KEY environment variable"
---

# ShortArt Image Generator

Unified interface for generating images using ShortArt AI with three specialized modes.

## Authentication Setup

`SHORTART_API_KEY` is required. Visit [https://shortart.ai/home](https://shortart.ai/home) and click on your profile picture to get the key. Configure via:

**Method 1: OpenClaw Config**
```json
{
  "skills": {
    "entries": {
      "shortart-image-generator": {
        "env": { "SHORTART_API_KEY": "your_api_key_here" }
      }
    }
  }
}
```

**Method 2: Shell Environment**
```bash
export SHORTART_API_KEY="your_api_key_here"
```

**IMPORTANT:** After setting the environment variable, restart your terminal or run `source ~/.zshrc` to apply the changes.

## Mode Selection

Identify user intent and route to appropriate mode:

### Mode 1: General Image Generation
**When to use**: User wants to create artwork from text descriptions or reference images
**Triggers**: "画一张图", "生成图片", "create image", "draw", "以图生图"
**See**: [references/text-to-image.md](references/text-to-image.md)

### Mode 2: E-commerce Suit Images
**When to use**: User wants product photography or Amazon listing images
**Triggers**: "套图", "生成套图", "组图", "suit image", "Image Set", "Photo Gallery", "A Set of Photos"
**See**: [references/suit-image.md](references/suit-image.md)

### Mode 3: Template-based Generation
**When to use**: User wants to use templates for posters, social media graphics, or marketing materials
**Triggers**: "模版生图", "用模版生成图片", "template image generation", "create from template", "推荐模版", "recommend template", "模版推荐"
**See**: [references/template-image.md](references/template-image.md)

## Quick Start

1. Verify API key: `echo $SHORTART_API_KEY`
2. Identify user intent from triggers above
3. Read the corresponding reference file for detailed workflow
4. Execute using scripts in the appropriate subdirectory
