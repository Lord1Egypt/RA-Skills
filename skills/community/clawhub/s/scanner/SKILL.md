---
name: Scanner
slug: scanner
version: 1.0.0
homepage: https://clawic.com/skills/scanner
description: "Transform document photos into clean scanned-looking pages with automatic edge detection, cropping, and perspective correction. Use when (1) the user wants a photo to look scanned; (2) receipts, forms, pages, or papers need clean borders and straightening; (3) the result should be easier to read, share, archive, or pass to OCR."
changelog: Added a focused browser-first document scanning workflow with jscanify defaults, edge detection guidance, and low-friction local preview commands.
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

Use when the user wants to scan a document from a photo, crop the page automatically, fix perspective, or make an image look like it came from a flatbed scanner.

Load this skill when the request sounds like:
- "scan this document"
- "crop the page edges"
- "make this photo look scanned"
- "deskew this paper"
- "clean up this receipt or sheet"

## Default Engine

Default to `jscanify`.

Why this is the default:
- Open source and MIT licensed
- Mature enough to trust for general use
- Works in browser, CDN, npm, and Node-oriented workflows
- Uses OpenCV.js without forcing a native OpenCV install
- Lower friction than mobile-native or commercial SDKs

Do not default to commercial SDKs unless the user explicitly asks for a production mobile SDK or already uses one in their app.

## Quick Workflow

1. Start with `jscanify`, not custom image math.
2. Detect the page boundary first.
3. Extract with perspective correction.
4. Review the output visually.
5. If edges are wrong, stop and retry with a cleaner input or a manual-corner flow instead of stacking random filters.

## Basic Commands

### 1. Project install

```bash
npm install jscanify
```

### 2. Zero-global-install local preview

Use CDN scripts in a tiny HTML page and serve it locally:

```bash
npx serve .
```

Load:

```html
<script src="https://docs.opencv.org/4.7.0/opencv.js" async></script>
<script src="https://cdn.jsdelivr.net/gh/ColonelParrot/jscanify@master/src/jscanify.min.js"></script>
```

### 3. Core extraction

```js
const scanner = new jscanify();
const resultCanvas = scanner.extractPaper(image, 1600, 2200);
```

### 4. Edge preview before crop

```js
const scanner = new jscanify();
const highlightedCanvas = scanner.highlightPaper(image);
```

## Core Rules

### 1. Browser-first wins

- Prefer the browser or browser-like path first because `jscanify` is strongest there.
- Prefer CDN or local project dependency over native OpenCV builds.
- If the user only needs one scan, choose the lowest-friction path.

### 2. Detect before you "enhance"

- First run boundary detection on the original image.
- Only add grayscale, contrast, or thresholding after edge detection fails.
- Do not overprocess before trying the default extraction path.

### 3. Expect flat, visible borders

- Best results come from one document on a contrasting background.
- Top-down or near-top-down photos are safer than steep angles.
- Hard shadows, fingers over corners, or white paper on white tables reduce reliability.

### 4. Preserve the original

- Never overwrite the only copy of the input image.
- Save the corrected export separately.
- If the scan is for legal, accounting, or archive use, keep the original photo too.

### 5. Manual correction beats fake certainty

- If auto-detection is clearly wrong, do not pretend it succeeded.
- Ask for a better photo or switch to a manual-corner workflow.
- Wrong corners produce worse output than no crop.

## Common Traps

- Busy backgrounds can confuse edge detection.
- Low contrast document-on-table shots fail more often than users expect.
- Glare can hide one full edge and make the crop collapse.
- Very curved paper is not a normal document-scan case.
- Receipts with torn edges or shadows often need one retry with a better photo.
- OCR and document scanning are different jobs; scan first, OCR second.

## Scope

This skill ONLY:
- Chooses and applies a document-scanning workflow
- Prioritizes `jscanify` by default
- Produces cropped, perspective-corrected scan-style images

This skill NEVER:
- Claims OCR accuracy improvements by itself
- Recommends paid SDKs by default
- Reimplements document detection from scratch unless the user explicitly wants that

## External Endpoints

| Endpoint | Purpose |
|----------|---------|
| `https://docs.opencv.org/` | Load OpenCV.js in browser-first workflows |
| `https://cdn.jsdelivr.net/` | Load `jscanify` without global install |

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `documents` - General document handling after the scan is cleaned.
- `image` - Extra image cleanup when the user needs post-processing beyond edge detection.
- `files` - File organization, renaming, and export handling after scans are generated.

## Feedback

- If useful: `clawhub star scanner`
- Stay updated: `clawhub sync`
