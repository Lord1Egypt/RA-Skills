---
name: image-to-pdf
description: Combine multiple image screenshots into a paginated A4 PDF. Intelligently handles page breaks to avoid cutting through text. Use when the user wants to combine, merge, or stitch images/screenshots into a PDF, especially exam papers or documents.
---

# Image to PDF

Combine multiple image screenshots (typically exam paper questions) into a well-formatted, paginated A4 PDF that is ready for printing.

## When to Use

Trigger this skill when the user wants to:

- Combine / merge / stitch images into a PDF
- Put screenshots together into a printable document
- Create a PDF from exam paper photos or screenshots
- Pack question images onto A4 pages for printing

Look for phrases like: "拼到一起", "合成PDF", "拼接", "打印", "combine images", "merge into PDF", etc.

## How to Use

This skill includes a Python script at `scripts/combine.py` (relative to this SKILL.md).

### Step 1: Identify inputs and output

From the user's request, extract:
- **Input**: a directory path or list of image file paths
- **Output**: the desired PDF output path (default: `output.pdf` in the input directory)

### Step 2: Run the script

Use `uv run` to handle dependencies automatically (no manual install needed):

```bash
uv run --with Pillow --with numpy python3 <path-to-this-skill>/scripts/combine.py <input> -o <output.pdf>
```

**Input formats:**
- A directory: `python scripts/combine.py ./my_images/ -o result.pdf`
- Multiple files: `python scripts/combine.py img1.png img2.png -o result.pdf`

**Optional flags:**
- `--margin <px>`: page margin in pixels at 300dpi (default: 80, ~7mm)
- `--no-trim`: disable automatic whitespace border trimming
- `--dpi <n>`: output DPI (default: 300)

### Step 4: Report result

Tell the user:
- How many images were processed
- How many PDF pages were generated
- The output file path

## What the Script Does

1. Loads images, auto-trims whitespace borders
2. Scales all images to the same width (A4 printable width)
3. Greedily packs images onto A4 pages (tight layout, no gaps)
4. When a page break is needed, uses pixel analysis to find whitespace rows so text is never cut
5. Outputs a 300 DPI PDF ready for printing
