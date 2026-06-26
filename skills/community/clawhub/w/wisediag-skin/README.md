# WiseDiag Skin Disease Analysis

Upload a skin photo and let WiseDiag AI identify possible skin conditions and provide analysis and recommendations.

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

## 🔑 API Key Setup (Required)

**Get your API key:** 👉 [https://console.wisediag.com/apiKeyManage](https://s.wisediag.com/xsu9x0jq)

```bash
# Temporary (current terminal session)
export WISEDIAG_API_KEY=your_api_key_here

# Permanent (add to ~/.zshrc or ~/.bashrc)
echo 'export WISEDIAG_API_KEY=your_api_key_here' >> ~/.zshrc
source ~/.zshrc
```

## Quick Start

**NEVER call any API or HTTP endpoint directly. ONLY use the script below.**

```bash
cd scripts

# Basic usage: upload a local skin image
python3 skin.py -f "/path/to/skin.jpg"

# Ask a specific question
python3 skin.py -f "/path/to/skin.jpg" --question "What is causing this rash?"

# Custom output filename
python3 skin.py -f "/path/to/skin.jpg" -n "skin_20260324"
```

Results are automatically saved to `~/.openclaw/workspace/WiseDiag-Skin/{name}.md`.

## Arguments

| Flag | Description |
|------|-------------|
| `-f, --file` | Local file path to upload as binary stream — image file (required) |
| `--question` | Question about the skin image (default: analyze and identify possible conditions) |
| `-n, --name` | Output filename stem (without `.md` extension) |
| `-o, --output` | Output directory (default: `~/.openclaw/workspace/WiseDiag-Skin`) |

## Troubleshooting

**"WISEDIAG_API_KEY is not set" error:**
Make sure you've set the environment variable correctly. Run `echo $WISEDIAG_API_KEY` to check.

**"Authentication failed" error:**
Your API key may be invalid or expired. Visit [console.wisediag.com](https://s.wisediag.com/xsu9x0jq) to regenerate it.

**"File not found" error:**
The local file path provided via `-f` does not exist. Check the path and try again.

**Image not recognized:**
Ensure the image is in JPG, JPEG, PNG, WebP, GIF, BMP, or TIFF format. Photos should be clear and well-lit for best results.

## Data Privacy

- **File upload mode (`-f`)**: Local files are uploaded as binary streams via multipart/form-data to WiseDiag's server for processing.

Image content is not permanently stored. Results are returned directly to you.

## ⚠️ Disclaimer

This tool's output is for reference only and does not constitute medical diagnosis or treatment advice.

## License

MIT
