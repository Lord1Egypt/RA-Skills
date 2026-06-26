---
name: zgcai-weekly-restaurant-menu-skill
description: Extracts structured weekly menu content (breakfast, lunch, snacks by day) from a cafeteria menu image using a VLM via OpenRouter. Use when the user provides a cafeteria or canteen menu photo and wants to know what dishes are available for the week.
version: "1.0.0"
emoji: "🍱"
metadata:
  openclaw:
    emoji: "🍱"
    primaryEnv: "MENU_OPENROUTER_API_KEY"
    requires:
      env: ["MENU_OPENROUTER_API_KEY"]
---

# 食堂周菜单识别

Extracts a full weekly cafeteria menu from an image: date range, and each day's breakfast, lunch, and snacks.

## When to use

When the user provides a cafeteria menu image (PNG or JPG) and wants to extract or reference its dish contents.

## How to extract

Run the extraction script with the image path:

```bash
python scripts/extract_menu.py <image_path>
```

Output is structured Markdown containing:
- Week date range
- Each day's breakfast items
- Each day's lunch items
- Each day's snack stall items (standalone `+`-separated line, e.g. `牛肉拉面+云南过桥米线`)

## Notes

- Requires `MENU_OPENROUTER_API_KEY` (OpenRouter API key)
- Model: `qwen/qwen-vl-plus` via OpenRouter
- Supports PNG and JPEG; no compression needed for files under 5 MB
- Snack stall items appear as a standalone line in the lunch section, with dishes joined by `+`
