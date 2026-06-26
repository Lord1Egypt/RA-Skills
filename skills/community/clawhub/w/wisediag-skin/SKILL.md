---
name: wisediag-skin
description: "Skin Disease Analysis — Analyze skin photos (via local file binary upload) and identify possible conditions via WiseDiag AI. Triggered when the user asks to analyze a skin image and provides a local image file path. Can also be invoked explicitly: say 'Use WiseDiag Skin to analyze this photo'."
registry:
  homepage: https://github.com/wisediag/WiseDiag-Skin
  author: wisediag
env_vars:
  - WISEDIAG_API_KEY
credentials:
  required: true
---

## When to Use This Skill

Activate this skill when any of the following conditions are met:

- The user provides a **local image file** of a skin condition and asks to analyze it
- The user says things like "analyze this skin photo", "what is this rash", "check this mole", or similar requests (in any language)

**Note:** This skill uses **local file upload** (binary stream). The user should provide a local file path (e.g. `/home/user/skin.jpg`, `C:\Users\...\rash.png`) and the script uploads it via binary stream (`-f`).

---

# ⚠️ Privacy Notice

**Please read before installing:**

This tool transmits your skin image files **to WiseDiag cloud servers** (via direct binary upload) for AI analysis.

**Do not upload images containing sensitive or private content** unless:
- You trust WiseDiag's data handling policy
- You accept that the file content will be transmitted to and processed remotely

**The output of this tool is for reference only and does not constitute medical diagnosis. Please consult a doctor for any health concerns.**

---

# WiseDiag Skin Disease Analysis (OpenClaw Skill)

Upload a skin photo and let WiseDiag AI automatically identify possible skin conditions and provide analysis and recommendations.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-green.svg)

## Features

- **Local file binary upload**: upload skin images directly via multipart/form-data
- AI-powered skin condition identification from photos
- Streaming output — results appear in real time
- Results automatically saved as a Markdown file

## Installation

```bash
pip install -r requirements.txt
```

## 🔑 API Key Configuration (Required)

**Get your API Key:** 👉 [https://console.wisediag.com/apiKeyManage](https://s.wisediag.com/xsu9x0jq)

The API key MUST be set as an environment variable. The script reads it automatically.

```bash
export WISEDIAG_API_KEY=your_api_key
```

## Usage (Step-by-Step)

**Do not call any API or HTTP endpoints directly — use only the script below.**

**⚠️ IMPORTANT: The script makes HTTP requests to an external API and may take 30-120 seconds to complete (especially for large images). Do NOT kill or interrupt a running command — wait for it to finish. The script prints streaming output so you can see it is working.**

```bash
cd scripts

# Basic usage: upload a local skin image
python3 skin.py -f "/path/to/skin.jpg"

# Ask a specific question
python3 skin.py -f "/path/to/skin.jpg" --question "这个皮疹是什么原因？"

# Specify output filename
python3 skin.py -f "/path/to/skin.jpg" -n "skin_20260324"
```

Results are automatically saved to `~/.openclaw/workspace/WiseDiag-Skin/{name}.md` — no manual saving needed.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `-f, --file` | Local file path to upload as binary stream — image file (required) |
| `--question` | Question to ask (default: analyze skin and identify possible conditions) |
| `-n, --name` | Output filename (without extension) |
| `-o, --output` | Output directory (default: ~/.openclaw/workspace/WiseDiag-Skin) |

## FAQ

**"WISEDIAG_API_KEY is not set" error:**
Verify the environment variable is set correctly by running `echo $WISEDIAG_API_KEY`.

**"Authentication failed" error:**
Your API Key may be invalid or expired. Visit [console.wisediag.com](https://s.wisediag.com/xsu9x0jq) to check or regenerate it.

**"File not found" error:**
The local file path provided via `-f` does not exist. Check the path and try again.

**Image not recognized:**
Ensure the image is in JPG, JPEG, PNG, WebP, GIF, BMP, or TIFF format. Photos should be clear and well-lit for best results.

## Data Privacy

- **File upload mode (`-f`)**: Local files are uploaded as binary streams via multipart/form-data to WiseDiag's server for processing.

Image content is not permanently stored. Results are returned directly to you.

## ⚠️ Disclaimer

The output of this tool is for reference only and does not constitute medical diagnosis or treatment advice. Please consult a qualified healthcare professional for any health concerns.

## License

MIT
