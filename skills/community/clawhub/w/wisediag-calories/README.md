# WiseDiag Food Calorie Estimator

Upload photos of food and let WiseDiag AI identify food items and estimate calories and nutritional content per serving.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-green.svg)

## Features

- **Local file binary upload**: upload food images directly via multipart/form-data
- Upload up to 5 food images per request (meals, snacks, beverages, etc.)
- AI automatically identifies food types and estimates calories (kcal)
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

There are two ways to analyze food — **upload local files** or **by URL**. Only one method can be used per request.

**Option A: Upload local files (recommended)** — when user provides local file paths, uploads binary stream via multipart/form-data

```bash
cd scripts

# Analyze a single food image
python3 calories.py -f "/path/to/food.jpg"

# Ask a specific question about the food
python3 calories.py -f "/path/to/food.jpg" --question "How many calories is this meal?"

# Analyze multiple dishes (up to 5 files)
python3 calories.py -f "/path/to/dish1.jpg" -f "/path/to/dish2.jpg"

# Save result with a custom filename
python3 calories.py -f "/path/to/food.jpg" -n "lunch_20260324"
```

**Option B: Submit via image URL** — when user provides a public HTTP/HTTPS link

```bash
cd scripts

# Single image URL
python3 calories.py --image "https://example.com/food.jpg"

# Multiple images
python3 calories.py --image "https://example.com/dish1.jpg" --image "https://example.com/dish2.jpg"

# Ask a specific question
python3 calories.py --image "https://example.com/food.jpg" --question "这顿饭大概多少卡路里？"
```

**How to choose (mutually exclusive — pick one):**
- User gives a local file path (e.g. `/home/user/food.jpg`, `C:\Users\...\meal.png`) → use `-f`
- User gives a URL (starts with `http://` or `https://`) → use `--image`
- Do NOT use `-f` and `--image` together in one command

Results are automatically saved to `~/.openclaw/workspace/WiseDiag-Calories/{name}.md`.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `-f, --file` | Local file path to upload as binary stream — image, repeatable up to 5 times (mutually exclusive with --image) |
| `--image` | Public URL of the food image, repeatable up to 5 times (mutually exclusive with --file) |
| `--question` | Question to ask about the food (default: estimate calories of the food in the image) |
| `-n, --name` | Output filename stem (without `.md` extension) |
| `-o, --output` | Output directory (default: `~/.openclaw/workspace/WiseDiag-Calories`) |

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

The output of this tool is for reference only and does not constitute professional nutritional or dietary advice. Always consult a qualified nutritionist for specific dietary needs.

## Data Privacy

- **File upload mode (`-f`)**: Local files are uploaded as binary streams via multipart/form-data to WiseDiag's server for processing.
- **URL mode (`--image`)**: Image URLs are transmitted to WiseDiag cloud servers; their server downloads and processes them.

Image content is not permanently stored. Results are returned directly to you.

## License

MIT
