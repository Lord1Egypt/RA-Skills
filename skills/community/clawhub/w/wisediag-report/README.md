# WiseDiag Medical Report Interpretation

Upload photos of medical reports and let WiseDiag AI interpret them — identifying test items, result values, reference ranges, abnormal indicators, and providing health advice.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-green.svg)

## Features

- **Local file binary upload**: upload report images/PDFs directly via multipart/form-data
- Upload up to 5 report images per request (blood tests, urine tests, imaging reports, etc.)
- AI automatically recognizes test items, result values, and abnormal indicators
- Streaming output — results appear in real time
- Results saved as Markdown files automatically

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

There are two ways to interpret a report — **upload local files** or **by URL**. Only one method can be used per request.

**Option A: Upload local files (recommended)** — when user provides local file paths, uploads binary stream via multipart/form-data

```bash
cd scripts

# Interpret a single report image
python3 report.py -f "/path/to/blood_test.jpg"

# Ask a specific question about the report
python3 report.py -f "/path/to/report.jpg" --question "Which indicators are abnormal?"

# Interpret a multi-page report (up to 5 files)
python3 report.py -f "/path/to/page1.jpg" -f "/path/to/page2.jpg"

# Save result with a custom filename
python3 report.py -f "/path/to/report.jpg" -n "checkup_20260324"
```

**Option B: Submit via image URL** — when user provides a public HTTP/HTTPS link

```bash
cd scripts

# Interpret a single report image
python3 report.py --image "https://example.com/blood_test.jpg"

# Multiple images
python3 report.py --image "https://example.com/p1.jpg" --image "https://example.com/p2.jpg"

# Ask a specific question
python3 report.py --image "https://example.com/report.jpg" --question "请解读异常指标"
```

**How to choose (mutually exclusive — pick one):**
- User gives a local file path (e.g. `/home/user/report.jpg`, `C:\Users\...\scan.png`) → use `-f`
- User gives a URL (starts with `http://` or `https://`) → use `--image`
- Do NOT use `-f` and `--image` together in one command

Results are automatically saved to `~/.openclaw/workspace/WiseDiag-Report/{name}.md`.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `-f, --file` | Local file path to upload as binary stream — image or PDF, repeatable up to 5 times (mutually exclusive with --image) |
| `--image` | Public URL of the report image, repeatable up to 5 times (mutually exclusive with --file) |
| `--question` | Question to ask about the report (default: interpret abnormal indicators and provide advice) |
| `-n, --name` | Output filename stem (without `.md` extension) |
| `-o, --output` | Output directory (default: `~/.openclaw/workspace/WiseDiag-Report`) |

## Troubleshooting

**"WISEDIAG_API_KEY is not set" error:**
Make sure you've set the environment variable correctly. Run `echo $WISEDIAG_API_KEY` to check.

**"Authentication failed" error:**
Your API key may be invalid or expired. Visit [console.wisediag.com](https://s.wisediag.com/xsu9x0jq) to check or regenerate your key.

**"File not found" error:**
The local file path provided via `-f` does not exist. Check the path and try again.

**Image not recognized:**
Ensure the image is in JPG, JPEG, or PNG format. Photos should be clear and well-lit for best results.

## ⚠️ Disclaimer

The output of this tool is for reference only and does not constitute medical diagnosis or treatment advice. Always consult a qualified healthcare professional for medical decisions.

## Data Privacy

- **File upload mode (`-f`)**: Local files are uploaded as binary streams via multipart/form-data to WiseDiag's server for processing.
- **URL mode (`--image`)**: Image URLs are transmitted to WiseDiag cloud servers; their server downloads and processes them.

Image content is not permanently stored. Results are returned directly to you.

## License

MIT
