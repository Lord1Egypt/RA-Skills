---
name: wisediag-report
description: "Medical Report Interpretation — Interpret medical report images (via local file binary upload or image URL) with AI-powered OCR recognition, abnormal indicator detection, and health advice. Triggered when the user asks to interpret a medical report and provides a local image/PDF file path or image URL. Can also be invoked explicitly: say 'Use WiseDiag Report to interpret this report'."
registry:
  homepage: https://github.com/wisediag/WiseDiag-Report
  author: wisediag
env_vars:
  - WISEDIAG_API_KEY
credentials:
  required: true
---

## When to Use This Skill

Activate this skill when any of the following conditions are met:

- The user provides **local image/PDF files** of a medical report and asks to interpret them
- The user sends an **image URL** of a medical report and asks to interpret it
- The user says things like "help me interpret this report", "look at my blood test", "what do these results mean", or similar requests (in any language)

**Note:** This skill supports both **local file uploads** (binary stream) and **image URLs**. The most common usage scenario is **uploading local files via binary stream** (`--file`), as users typically have report images/PDFs saved on their device rather than hosted at a public URL.

**How to choose (mutually exclusive — pick one):**
- If the user provides a **local file path** (e.g. `/home/user/report.jpg`, `C:\Users\...\scan.png`) → use `--file` (binary upload). **This is the primary and most common usage.**
- If the user provides a **URL** (starts with `http://` or `https://`) → use `--image`
- Do NOT use `--file` and `--image` together in one command

---

# ⚠️ Privacy Notice

**Please read before installing:**

This tool transmits your medical report files **to WiseDiag cloud servers** (via direct binary upload or image URL) for AI analysis.

**Do not upload images containing sensitive or private content** unless:
- You trust WiseDiag's data handling policy
- You accept that the file content will be transmitted to and processed remotely

**The output of this tool is for reference only and does not constitute medical diagnosis. Please consult a qualified healthcare professional for any health concerns.**

---

# WiseDiag Medical Report Interpretation (OpenClaw Skill)

Upload photos of physical medical reports (blood tests, urine tests, imaging reports, etc.) and let WiseDiag AI automatically recognize the text, parse key indicators, highlight abnormal values, and provide health advice.

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

There are two ways to interpret a report — pick one (mutually exclusive):

---

**Option A: Upload local files (recommended)** — when user provides local file paths

```bash
cd scripts

# Single report image
python3 report.py -f "/path/to/report.jpg"

# Multiple images (e.g. multi-page report, max 5)
python3 report.py -f "/path/to/page1.jpg" -f "/path/to/page2.jpg"

# Ask a specific question
python3 report.py -f "/path/to/report.jpg" --question "请解读报告中的异常指标"

# Specify output filename
python3 report.py -f "/path/to/report.jpg" -n "bloodtest_20260324"
```

---

**Option B: Submit via image URL** — when user provides a public HTTP/HTTPS link

```bash
cd scripts

# Single image URL
python3 report.py --image "https://example.com/report.jpg"

# Multiple images
python3 report.py --image "https://example.com/p1.jpg" --image "https://example.com/p2.jpg"

# Ask a specific question
python3 report.py --image "https://example.com/report.jpg" --question "请解读报告中的异常指标"
```

---

**How to choose (mutually exclusive — pick one):**
- User gives a local file path (e.g. `/home/user/report.jpg`, `C:\Users\...\scan.png`) → use `-f`
- User gives a URL (starts with `http://` or `https://`) → use `--image`
- Do NOT use `-f` and `--image` together in one command

Results are automatically saved to the current working directory as `{name}.md` — no manual saving needed.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `-f, --file` | Local file path to upload as binary stream — image or PDF, repeatable up to 5 times (mutually exclusive with --image) |
| `--image` | Public URL of the report image, repeatable up to 5 times (mutually exclusive with --file) |
| `--question` | Question to ask (default: interpret abnormal indicators and provide advice) |
| `-n, --name` | Output filename (without extension) |
| `-o, --output` | Output directory (default: current working directory) |

## FAQ

**"WISEDIAG_API_KEY is not set" error:**
Verify the environment variable is set correctly by running `echo $WISEDIAG_API_KEY`.

**"Authentication failed" error:**
Your API Key may be invalid or expired. Visit [console.wisediag.com](https://s.wisediag.com/xsu9x0jq) to check or regenerate it.

**"File not found" error:**
The local file path provided via `-f` does not exist. Check the path and try again.

**Image not recognized:**
Ensure the image is in JPG, JPEG, or PNG format. Photos should be clear and well-lit for best results.

## Data Privacy

- **File upload mode (`-f`)**: Local files are uploaded as binary streams via multipart/form-data to WiseDiag's server for processing.
- **URL mode (`--image`)**: Image URLs are transmitted to WiseDiag cloud servers; their server downloads and processes them.

Image content is not permanently stored. Results are returned directly to you.

## ⚠️ Disclaimer

The output of this tool is for reference only and does not constitute medical diagnosis or treatment advice. Always consult a qualified healthcare professional for medical decisions.

## License

MIT
