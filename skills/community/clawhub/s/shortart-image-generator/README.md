<div align="center">

# 🎨 ShortArt Image Generator

**Unified AI image generation skill with three powerful modes**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

> 🎉 **Generate images from text, create e-commerce product photos, or use professional templates - all in one skill!**

[Get Started](#-installation) • [Features](#-features) • [Quick Start](#-quick-start)

</div>

---

## 📦 Installation

### Step 1: Install the skill

```bash
npx skills add yige666s/shortart-image-generator
```

This will install the skill to `~/.agents/skills/shortart-image-generator`.

### Step 2: Create symlink

If you need to link the skill to a specific agent directory:

```bash
# For Claude Code
ln -s ~/.agents/skills/shortart-image-generator ~/.claude/skills/shortart-image-generator

# For OpenClaw
ln -s ~/.agents/skills/shortart-image-generator ~/.openclaw/skills/shortart-image-generator
```

## ✨ Features

### 🎯 Three Generation Modes

- **Mode 1: Text-to-Image & Image-to-Image** - Generate artwork from text descriptions or reference images
- **Mode 2: Suit Images** - Professional product photography for suit Images generate.
- **Mode 3: Template-based Generation** - Use professional templates for posters, social media, and marketing

### 🚀 Key Capabilities

- 🤖 **AI-Assisted Workflow** - Interactive guidance through the entire generation process
- 🖼️ **Multiple AI Models** - Choose from nano-banana-pro, nano-banana-2, seedream4.5
- 📊 **Flexible Output** - Multiple resolutions (0.5K-4K), aspect ratios (1:1, 16:9, 9:16)
- 🎨 **Batch Generation** - Generate 1-4 images at once
- ⚡ **Smart Polling** - Automatic status checking with estimated completion times
- 🌐 **Bilingual Support** - Works with English and Chinese commands

## 🚀 Quick Start

### 1. Get Your API Key

1. Visit [ShortArt.ai](https://shortart.ai) to register an account with Google
2. Get your API Key from [shortart.ai/key](https://shortart.ai/key)
3. Configure it in `~/.openclaw/openclaw.json` or export to `~/.zshrc`

**IMPORTANT:** After setting the environment variable in `~/.zshrc`, restart your terminal or run `source ~/.zshrc` to apply the changes.

### 2. Generate Images

Simply chat with your AI assistant:

**Mode 1: Text-to-Image**
```
Draw a futuristic cityscape at night with neon lights
```

**Mode 2: Suit Images**
```
Help me create Amazon product images for this phone
```

**Mode 3: Template-based**
```
Generate a professional headshot for me using a template
```

Or in Chinese:
```
画一张未来城市夜景图
帮我给这个手机产品制作亚马逊商品主图
帮我生成个人职业照，推荐一个模版
```

**Interactive Workflow:**

1. **Task Submission** - Generation task is submitted and returns a `project_id`
2. **Wait Confirmation** - You can wait for completion or not
3. **Polling** - If you agree, AI polls the generation status
4. **Download Confirmation** - When complete, you'll be asked if you want to download
5. **Local Download** - Images are downloaded and local file paths provided

### 3. Example Interaction Flow

#### Example 1: Text-to-Image Generation

```
👤 User: Draw a sunset over mountains

🤖 Assistant: I'll generate a sunset over mountains image for you.

[Generating with nano-banana-pro model...]

✅ Task submitted successfully!
- Project ID: proj_abc123xyz
- Status: Processing

Would you like me to wait and check when it's complete?

👤 User: Yes, please wait

🤖 Assistant: Polling status...

[Checking... ⏳]

✅ Generation complete! Your image is ready.

Would you like me to download it?

👤 User: Yes

🤖 Assistant: Downloading...

✅ Download complete!

Your image has been saved to:
📁 /Users/you/Downloads/shortart_20260318_143022_1.jpg
```

#### Example 2: E-commerce Product Photo

```
👤 User: Create professional product photos for this phone
[Uploads phone image]

🤖 Assistant: I'll create professional e-commerce images for your phone.

[Uploading image...]
[Submitting task...]

✅ Task submitted successfully!
- Project ID: proj_def456uvw

Would you like me to wait for completion?

👤 User: Yes

🤖 Assistant: [Polling...]

✅ Generation complete!

Your product images have been saved to:
📁 /Users/you/Downloads/shortart_suit_20260318_143530_1.jpg
📁 /Users/you/Downloads/shortart_suit_20260318_143530_2.jpg
```

#### Example 3: Template-based Professional Headshot

```
👤 User: Generate a professional headshot for me, recommend a template
[Uploads photo]

🤖 Assistant: I found professional headshot templates. Here are the top 3:

1. Professional Studio Headshot - Customizable attire and backgrounds
2. Corporate Headshot Navy Suit - Classic business look
3. Blue Textured Studio Portrait - ID photo style

Which one would you like?

👤 User: 1

🤖 Assistant: Great! This template needs:
- Your photo (already uploaded)
- Attire style (Smart Casual / Formal / Modern Business / Clean Minimal)
- Background color (Studio Blue / Dark Grey / Clean White / Warm Beige)

Please specify your preferences, or I'll use defaults.

👤 User: Use defaults

🤖 Assistant: [Generating professional headshot...]

✅ Generation complete!

Your headshot has been saved to:
📁 /Users/you/Downloads/shortart_template_20260318_212146_1.jpg
```

### 4. Input Requirements

#### Mode 1: Text-to-Image

| Parameter | Options | Default |
|-----------|---------|---------|
| **Prompt** | Text description | Required |
| **Model** | nano-banana-pro, nano-banana-2, seedream4.5 | nano-banana-pro |
| **Resolution** | 0.5k, 1k, 2k, 4k | 2k |
| **Aspect Ratio** | 1:1, 16:9, 9:16 | 1:1 |
| **Count** | 1-4 | 1 |
| **Reference Image** | Local file or Base64 | Optional |

#### Mode 2: E-commerce Suit Images

| Parameter | Description |
|-----------|-------------|
| **Reference Image** | One product photo (local file or Base64) |
| **Prompt** | Description of desired output (e.g., "Create an Amazon product image set for this mobile phone.") |

#### Mode 3: Template-based Generation

| Parameter | Description |
|-----------|-------------|
| **Template** | Selected from AI recommendations |
| **Parameters** | Varies by template (text, images, colors, etc.) |
| **Images** | Local files, Base64 strings |

### 5. Supported Image Upload Methods

The skill supports three ways to provide images:

1. **Local File Path**
   ```
   /Users/you/Pictures/photo.jpg
   ./images/product.png
   ```

2. **Base64 String**
   ```
   data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
   iVBORw0KGgoAAAANSUhEUgAA...
   ```
---

## 📋 Requirements

- Python 3.7+
- `requests` library
- ShortArt account

## 📄 License

MIT License - see [LICENSE](LICENSE) for details
