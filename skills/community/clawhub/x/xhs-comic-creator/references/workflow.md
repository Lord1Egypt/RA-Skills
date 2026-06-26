# Workflow

Follow this pipeline strictly.

---

# Step 1 — Topic Research

Search for information about the topic. Use Tavily Search skill or playwright skill.

Goal:

extract 6-8 core knowledge points.

Output format:

Topic Summary

topic:
key_points:
simple_explanation:

---

# Step 2 — Convert to Comic Story

Transform the explanation into a short narrative.

Setting:

AI research lab inspired by Rhodes Island.

Create dialogue explaining the topic.

Generate 15-20 panels.

Each panel must contain:

scene
action
dialogue (with specific Chinese text)

**IMPORTANT:** Write out the exact Chinese dialogue for each panel. The dialogue will appear in speech bubbles in the final comic.

Example:
```
Panel 1:
scene: 罗德岛情报室，大屏幕前
action: Doctor指着屏幕上的新闻头条
chinese_dialogue:
  Doctor: "阿米娅，2026年3月美以联合对伊朗发动了重大军事行动。"
  Amiya: "博士，这次冲突的起因是什么？"
```

---

# Step 3 — Organize Panels

Group panels into images.

Rules:

5-6 images total
Each image contains 3-4 panels

Example:

Image 1
panel 1
panel 2
panel 3

Image 2
panel 4
panel 5
panel 6

---

# Step 4 — Generate Image Prompts

Convert each image into a detailed prompt.

Use rules in:

`comic_generation.md`

**CRITICAL:** Include the specific Chinese dialogue text in each panel description. The AI needs to know exactly what text appears in speech bubbles.

Example prompt structure:
```
Panel 1: Doctor pointing at screen saying "阿米娅，2026年3月美以联合对伊朗发动重大作战行动", Amiya looking concerned asking "博士，这次冲突的起因是什么？"
Panel 2: [scene description with specific Chinese dialogue]
Panel 3: [scene description with specific Chinese dialogue]
```

---

# Step 5 — Generate Images (with Visual Consistency)

Call Banana Pro API with input-image chaining for consistency.

## Character Setup (Fixed Trio)
Use ONLY these characters across all images:
- **Doctor**: Black tactical coat, hood/mask - main instructor
- **Amiya**: Brown hair, rabbit ears, tablet - learner perspective
- **Kal'tsit**: Green hair, cat ears, lab coat - technical expert

## Generation Order (Chained for Consistency):

### Image 1 (Base)
```bash
uv run scripts/generate_image.py \
  --prompt "Arknights-inspired anime comic page, portrait orientation 9:16 aspect ratio, vertical layout optimized for mobile phone viewing, [scene description with Chinese dialogue]" \
  --filename "comic_1.png" \
  --resolution 1K
```

### Images 2-6 (Chained with --input-image)
```bash
# Image 2 uses Image 1 as style reference
uv run scripts/generate_image.py \
  --input-image "comic_1.png" \
  --prompt "Continue the comic story, portrait orientation 9:16, vertical layout, same art style, Doctor in black coat, Amiya with rabbit ears, Kal'tsit in lab coat... [Chinese dialogue]" \
  --filename "comic_2.png" \
  --resolution 1K

# Image 3 uses Image 2 as reference
uv run scripts/generate_image.py \
  --input-image "comic_2.png" \
  --prompt "Continue maintaining visual consistency, portrait 9:16, vertical layout... [Chinese dialogue]" \
  --filename "comic_3.png" \
  --resolution 1K

# Continue pattern for images 4, 5, 6...
```

### Aspect Ratio Note:
Always include in prompts:
- `portrait orientation`
- `9:16 aspect ratio`
- `vertical layout`
- `optimized for mobile phone viewing`
- `panels arranged vertically`

## Why This Works:
- `--input-image` preserves art style, color palette, and character designs
- Each image still gets its own unique scene description
- Visual narrative flows smoothly from page to page
- Character appearances remain consistent

Save all to:

assets/

Resolution: 1K (saves tokens)

---

# Step 6 — Prepare Xiaohongshu Post

Create:

Title
Body text

Body structure:

Hook
Short explanation
Friendly ending

Example:

如果这组漫画让你理解了这个概念，欢迎讨论。

Use rules in:

`xhs_posting.md`

---

# Step 7 — Publish

Upload images.

Create post using MCP tool.

## CRITICAL - Duplicate Prevention

**ALWAYS check if a similar task was just completed before executing.**

Look for:
- Recent process logs with same command patterns
- Existing image files with current timestamp
- Previous successful posts on the same topic

If you see signs of recent execution:
1. **DO NOT regenerate images**
2. **DO NOT republish**
3. Ask user for confirmation instead

## CRITICAL - VERIFY IMAGE PATHS:
Before publishing, double-check that:
1. All 6 image paths are unique (no duplicates)
2. Images are in correct order (comic_1, comic_2, ... comic_6)
3. All files exist at the specified paths

Correct example:
```json
"images": [
  "/path/to/comic_1.png",
  "/path/to/comic_2.png",
  "/path/to/comic_3.png",
  "/path/to/comic_4.png",
  "/path/to/comic_5.png",
  "/path/to/comic_6.png"
]
```

Incorrect example (AVOID):
```json
"images": [
  "/path/to/comic_1.png",
  "/path/to/comic_2.png",
  "/path/to/comic_3.png",
  "/path/to/comic_4.png",
  "/path/to/comic_4.png",  // DUPLICATE! Wrong!
  "/path/to/comic_6.png"
]
```