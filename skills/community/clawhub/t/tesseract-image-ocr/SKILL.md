---
name: tesseract-image-ocr
description: Extract text from images using Tesseract.js (OCR). Supports multi-language recognition including Chinese and English, region recognition, character whitelist filtering, text orientation detection, and can run in a Node.js environment.
---

# Tesseract OCR Image Text Extraction

Extract text content from images based on Tesseract.js (the WebAssembly port of the Tesseract OCR engine).

## Use Cases

Use when users need "image to text," "OCR recognition," "extract text from images," "screenshot character recognition," "scan to text," or "image text orientation detection."

## Core Capabilities

- Recognize text from local images or image URLs
- Support for 100+ languages, with the ability to specify multiple languages simultaneously (e.g., `['eng', 'chi_sim']`)
- Support for specifying recognition regions (`--rectangle`), character whitelists (`--whitelist`)
- Support for text orientation and script detection (`--detect`)
- Support for switching page segmentation modes (`--psm`) and OCR engine modes (`--oem`)
- Output formats: `text` (default), `hocr`, `blocks` (JSON), `tsv`

## Limitations

- Does not support PDF files
- Does not modify the Tesseract recognition model to improve accuracy
- Requires a Node.js environment (this Skill uses Node.js scripts)

---

## Workflow

### 1. Confirm Environment

```shell
node -v && npm ls tesseract.js 2>/dev/null || echo "tesseract.js not installed"
```

If not installed:

```shell
cd /root/.openclaw/workspace/skills/tesseract-ocr && npm init -y > /dev/null 2>&1 && npm install tesseract.js
```

### 2. Execute Recognition

Basic command:

```shell
node scripts/ocr.js <image-path-or-url> [--options]
```

**Parameter Descriptions:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `<image>` | Required | — | Local path or HTTPS URL |
| `--lang` | string | `eng` | Language code(s), multiple joined with `+`, e.g., `eng+chi_sim` |
| `--psm` | number | — | Page segmentation mode (see PSM table below) |
| `--oem` | number | — | OCR engine mode (see OEM table below) |
| `--whitelist` | string | — | Character whitelist, e.g., `0123456789` to recognize only digits |
| `--rectangle` | string | — | Recognition region, format `top,left,width,height` |
| `--output` | string | `text` | Output format: `text` / `hocr` / `blocks` / `tsv` |
| `--detect` | flag | — | Detect text orientation and script (does not perform OCR) |
| `--dpi` | number | — | Manually specify image DPI |

**Common Examples:**

```shell
# Basic mixed Chinese-English recognition
node scripts/ocr.js photo.jpg --lang chi_sim+eng

# Recognize digits only (license plates, CAPTCHAs, etc.)
node scripts/ocr.js captcha.png --whitelist 0123456789

# Column-based recognition (suitable for vertical Chinese text)
node scripts/ocr.js scroll.jpg --lang chi_sim --psm 4

# Specify a region for recognition
node scripts/ocr.js receipt.png --rectangle 50,100,400,200

# Detect image text orientation
node scripts/ocr.js rotated.jpg --detect

# Output structured data
node scripts/ocr.js doc.png --output blocks

# Manually specify DPI (avoids "Invalid resolution 0 dpi" warning)
node scripts/ocr.js scan.png --dpi 300
```

### 3. Batch Recognition of Multiple Images

To reuse a Worker, the AI should write an inline script:

```javascript
const { createWorker } = require('tesseract.js');
(async () => {
  const worker = await createWorker('eng');
  for (const img of ['a.png', 'b.png', 'c.png']) {
    const { data: { text } } = await worker.recognize(img);
    console.log(img, '→', text);
  }
  await worker.terminate();
})();
```

---

## PSM — Page Segmentation Modes

The `--psm` parameter controls how Tesseract analyzes page layout:

| PSM | Name | Description |
|-----|------|-------------|
| 0 | OSD_ONLY | Orientation and script detection only |
| 1 | AUTO_OSD | Automatic page segmentation + orientation detection |
| 2 | AUTO_ONLY | Automatic page segmentation, no orientation detection |
| 3 | AUTO | Fully automatic page segmentation (default) |
| 4 | SINGLE_COLUMN | Single column of variable size text |
| 5 | SINGLE_BLOCK_VERT_TEXT | Single block of vertical text |
| 6 | SINGLE_BLOCK | Single block of text |
| 7 | SINGLE_LINE | Single line of text |
| 8 | SINGLE_WORD | Single word |
| 9 | CIRCLE_WORD | Single word in a circular arrangement |
| 10 | SINGLE_CHAR | Single character |
| 11 | SPARSE_TEXT | Sparse text (find as much as possible) |
| 12 | SPARSE_TEXT_OSD | Sparse text + orientation detection |
| 13 | RAW_LINE | Raw line (treated as a single line) |

## OEM — OCR Engine Modes

| OEM | Description |
|-----|-------------|
| 0 | Legacy engine |
| 1 | LSTM neural network engine (default) |
| 2 | Legacy + LSTM |
| 3 | Default (automatically selected based on current configuration) |

## Language Code Quick Reference

| Language | Code |
|----------|------|
| English | `eng` |
| Simplified Chinese | `chi_sim` |
| Traditional Chinese | `chi_tra` |
| Japanese | `jpn` |
| Korean | `kor` |
| French | `fra` |
| German | `deu` |
| Spanish | `spa` |
| Russian | `rus` |
| Arabic | `ara` |
| Hindi | `hin` |

Full list: [tesseract_lang_list.md](https://github.com/naptha/tesseract.js/blob/master/docs/tesseract_lang_list.md)

## Advanced Usage

The following scenarios require the AI to write inline scripts directly rather than using `scripts/ocr.js`:

- **Reusing a Worker after switching languages**: Use `worker.reinitialize(langs, oem)`
- **Setting Tesseract parameters**: Use `worker.setParameters({ tessedit_pageseg_mode: ... })`
- **Detecting text orientation** (requires Legacy engine): Call `worker.detect(image)` after `createWorker('eng', 0, { legacyCore: true, legacyLang: true })`
- **Processing large numbers of images in parallel**: Use `createScheduler()` + multiple Workers

For complete API reference, see [references/api.md](references/api.md).