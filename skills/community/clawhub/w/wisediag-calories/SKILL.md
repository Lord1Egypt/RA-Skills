---
name: wisediag-calories
description: "Food Calorie Estimator — Identify food items and estimate calories from an image (via local file binary upload or image URL) with AI-powered recognition. Triggered when the user asks to estimate food calories and provides a local image file path or image URL. Can also be invoked explicitly: say 'Use WiseDiag Calories to analyze this'."
registry:
  homepage: https://github.com/wisediag/WiseDiag-Calories
  author: wisediag
env_vars:
  - WISEDIAG_API_KEY
credentials:
  required: true
---

## When to Use This Skill

Activate this skill when any of the following conditions are met:

- The user provides **local image files** of food and asks to estimate calories
- The user sends an **image URL** of food and asks to estimate calories
- The user says things like "how many calories is this", "estimate calories", "analyze this food photo", or similar requests (in any language)

**Note:** This skill supports both **local file uploads** (binary stream) and **image URLs**. The most common usage scenario is **uploading local files via binary stream** (`--file`), as users typically have food photos saved on their device rather than hosted at a public URL.

**How to choose (mutually exclusive — pick one):**
- If the user provides a **local file path** (e.g. `/home/user/food.jpg`, `C:\Users\...\meal.png`) → use `--file` (binary upload). **This is the primary and most common usage.**
- If the user provides a **URL** (starts with `http://` or `https://`) → use `--image`
- Do NOT use `--file` and `--image` together in one command

---

# ⚠️ Privacy Notice

**Please read before installing:**

This tool transmits your food image files **to WiseDiag cloud servers** (via direct binary upload or image URL) for AI analysis.

**Do not upload images containing sensitive or private content** unless:
- You trust WiseDiag's data handling policy
- You accept that the file content will be transmitted to and processed remotely

**The output of this tool is for reference only and does not constitute professional nutritional or dietary advice. Please consult a qualified nutritionist for specific dietary needs.**

---

# WiseDiag Food Calorie Estimator (OpenClaw Skill)

Upload photos of food (meals, snacks, beverages, etc.) and let WiseDiag AI automatically identify food items, estimate calories and nutritional content per serving.

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

There are two ways to analyze food — pick one (mutually exclusive):

---

**Option A: Upload local files (recommended)** — when user provides local file paths

```bash
cd scripts

# Single food image
python3 calories.py -f "/path/to/food.jpg"

# Multiple images (e.g. multiple dishes, max 5)
python3 calories.py -f "/path/to/dish1.jpg" -f "/path/to/dish2.jpg"

# Ask a specific question
python3 calories.py -f "/path/to/food.jpg" --question "这顿饭大概多少卡路里？"

# Specify output filename
python3 calories.py -f "/path/to/food.jpg" -n "lunch_20260324"
```

---

**Option B: Submit via image URL** — when user provides a public HTTP/HTTPS link

```bash
cd scripts

# Single image URL
python3 calories.py --image "https://example.com/food.jpg"

# Multiple images
python3 calories.py --image "https://example.com/dish1.jpg" --image "https://example.com/dish2.jpg"

# Ask a specific question
python3 calories.py --image "https://example.com/food.jpg" --question "How many calories is this meal?"
```

---

**How to choose (mutually exclusive — pick one):**
- User gives a local file path (e.g. `/home/user/food.jpg`, `C:\Users\...\meal.png`) → use `-f`
- User gives a URL (starts with `http://` or `https://`) → use `--image`
- Do NOT use `-f` and `--image` together in one command

Results are automatically saved to `~/.openclaw/workspace/WiseDiag-Calories/{name}.md` — no manual saving needed.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `-f, --file` | Local file path to upload as binary stream — image, repeatable up to 5 times (mutually exclusive with --image) |
| `--image` | Public URL of the food image, repeatable up to 5 times (mutually exclusive with --file) |
| `--question` | Question to ask (default: estimate calories of the food in the image) |
| `-n, --name` | Output filename (without extension) |
| `-o, --output` | Output directory (default: ~/.openclaw/workspace/WiseDiag-Calories) |

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

The output of this tool is for reference only and does not constitute professional nutritional or dietary advice. Always consult a qualified nutritionist for specific dietary needs.

## License

MIT
