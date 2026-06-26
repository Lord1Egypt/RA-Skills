# /thumbnail-qa

**AI-powered thumbnail image QA for Next.js sites.** Detects poorly cropped images, computes optimal `object-position` values using focal point analysis, and auto-fixes with before/after screenshot evidence. Each fix gets its own atomic commit.

## What it does

1. **Scans your codebase** for Next.js `<Image fill>` components
2. **Screenshots every thumbnail** in its container using a headless browser
3. **Analyzes the original image** to find the focal point (faces, subjects, key content)
4. **Compares the crop** against focal point rules (portraits keep forehead-to-chin, groups maximize visible faces, etc.)
5. **Computes optimal `object-position`** values when the current crop is wrong
6. **Applies fixes** with before/after screenshots and atomic commits
7. **Generates a report** with results for every image

## Install

Claude Code:

```
/plugin marketplace add kaicianflone/thumbnail-qa-skill
```

OpenClaw:

```
clawhub install thumbnail-qa
```

### Prerequisites

- [gstack](https://github.com/garrytan/gstack) installed (provides the `browse` headless browser binary)
- A Next.js project with `<Image fill>` components
- Dev server running on `localhost:3000` (or the skill starts one for you)

## Usage

In Claude Code, just say:

```
/thumbnail-qa
```

Or use natural language:

- "Check my thumbnails"
- "Fix image cropping"
- "The team photos look cut off"

The skill runs automatically after you upload new images to `/public`.

## How it works

### Image Registry

Greps your codebase for `<Image fill>` components, reads the full file to resolve conditional classNames and dynamic src values, and builds a registry of every thumbnail candidate. Filters out logos, avatars, and intentionally letterboxed images.

### Focal Point Analysis

Each image is classified by type (portrait, group, architecture, event, landscape) and assigned focal point coordinates. The skill uses these rules:

| Photo Type | Focal Point Priority |
|------------|---------------------|
| Portrait | Face fully visible, forehead to chin. Eyes in upper third. |
| Group | Maximize visible faces. Favor horizontal center. |
| Architecture | Full structure. Roofline and entryway both visible. |
| Event | Primary action or speaker in frame. |
| Landscape | Key subject centered; horizon depends on content. |

### object-position Semantics

The skill understands how CSS `object-position` actually works:

- `object-position: X Y` aligns the X% point of the image to the X% point of the container
- `object-top` (= `50% 0%`) pins the top of the image to the top of the container
- For tall portraits in short wide containers, low Y values (0-10%) show the top of the image

### Fix Verification

Every fix is verified with a before/after screenshot comparison. If the fix makes things worse (computed position degrades framing vs. the original), it's reverted and flagged for manual review.

## Output

The skill generates a structured report saved to `.gstack/thumbnail-qa/report-YYYY-MM-DD.md`:

```
THUMBNAIL QA REPORT
===================
Total candidates checked:  15
  OK (no fix needed):       9
  Repositioned:             4
  Skipped (filtered):       1
  Manual review needed:     1

REPOSITIONED IMAGES
-------------------
| # | Image      | Page   | Before       | After             | Reason                    |
|---|------------|--------|--------------|-------------------|---------------------------|
| 1 | alice.jpg  | /about | object-top   | object-[50%_15%]  | Face centered with brow   |
...
```

## License

MIT
