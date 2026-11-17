---
name: scan-watermark-removal
description: Deterministically remove light translucent text watermarks from scanned paper pages (lecture notes, handouts, exam papers, workbooks) as images or PDF, plus printed coloured header logos. Use when the user asks to 去水印 / remove watermark / clean watermarks from 扫描笔记、讲义、试卷、资料图片、PDF 讲义, especially batches of course-note scans with pale diagonal tiled text (WeChat id, brand name, URL) or a brand logo in the page header. Not for photo watermarks, dark or photographic logos, or cases where the watermark colour is indistinguishable from content — those need generative inpainting instead, which redraws the page and can destroy handwriting, so warn the user and require per-page review.
license: MIT
---

# Scan Watermark Removal

Remove two different things that both get called "watermark" on scanned course
material:

| Family | Looks like | Method |
|---|---|---|
| **Translucent text** | pale pink/purple diagonal tiled text over the whole page | colour-cone pixel isolation |
| **Printed header logo** | solid coloured brand text (e.g. a teacher's name) in the page header | colour wedge + shape test, header band only |

Both are deterministic: no model, no generative redraw, no network. Red pen,
black print, blue table rules, grey figures and colour illustrations survive
100% — verified by pixel accounting on every page.

## When to use

- Scanned lecture notes / handouts / exam papers with pale diagonal watermark
  text tiled across the paper.
- PDF bundles of such scans, where the watermark is baked into the page bitmap.
- Pages carrying a printed coloured logo in the header that the user wants gone.

## When NOT to use

- Photo watermarks, stock-photo overlays, or semi-transparent logos over busy
  imagery — the paper-white assumption does not hold.
- Dark, saturated, or photographic logos. Only *light* translucent overlays and
  *flat-colour printed* header text are in scope.
- Watermark colour within a few units of the content colour. Ink protection will
  bail out and leave it behind, which is the correct trade — do not force it.
- **Do not** reach for generative image-editing tools on this material. On a
  dense handwriting page they repaint the whole page and swallow most of the red
  ink, then leave pink fringes around remaining strokes. Measured: ~75% of red
  handwriting lost on the worst page. If a generative tool is the only option,
  say so and require per-page review.

## Workflow

### 1. Look before you cut

Open 2–3 pages at full resolution. Identify which families are present:

- pale diagonal tiled text → translucent watermark
- solid coloured text in the header → printed logo
- both → handle both (the tool does, by default)

### 2. Sample the watermark colour

Pick a patch of paper that has watermark but no content, read the RGB.
Typical measured values:

| Watermark | Sample colour | Signal |
|---|---|---|
| pink | (244,191,191) | `r-g ≈ 53`, `|b-g| ≈ 0` |
| purple | (200,190,215) | `b-g ≈ 20`, `|r-g| ≈ 5` |
| header logo | (255,192,0) | `r-g = 63`, `b = 0` |

If the sampled colour is far from these, adjust the constants at the top of
`scripts/wmcore.py` (`PINK`, `PURPLE`, `FAINT`) — see
`references/watermark-signature.md` for how to derive thresholds.

### 3. Run

```bash
# image folder or single image
python scripts/remove_watermark.py <folder_or_image>

# PDF
python scripts/remove_watermark.py <file.pdf> --output <out.pdf>
```

Defaults: output `<input>/去水印输出/` for images, `<name>_去水印.pdf` for PDF;
suffix `_去水印`; both colour cones on; header logo cleared. Originals are never
modified.

Useful flags: `--near` (ink-protection window, default 5), `--no-logo`,
`--no-pink`, `--no-purple`, `--all` (reprocess already-suffixed files).

### 4. Read the metrics — this is the acceptance gate

Every page prints:

- `erased` px → **must be 0.** Pixels that were unambiguously content (dark
  `min < 120`, saturated red, saturated blue) and are now near-white. This is the
  real safety metric.
- `residue` px plus `visible` in parentheses → watermark pixels on clean paper,
  and how many are dark enough to actually be seen. **Visible must be ~0**; the
  raw count is often in the thousands on a JPEG page and means nothing.
- `red / dark / blue` retention % → coverage reference only, expected ≥ 90.

Why `erased` rather than a retention percentage: JPEG re-encoding shifts the
palest antialiased edges by a few units, which pushes a percent or two of them
below the "is this content" threshold. Retention can read 91% on a page where
zero real pixels were lost. Percentage thresholds therefore either fail correct
output or invite loosening until they hide real damage. Counting *documented
content that disappeared* has neither problem.

To audit the old way anyway, print the original min channel of every lost pixel:
deficits from `min ∈ [120,150]` are edge jitter, `min < 100` is real loss.

Exit code 0 means all pages passed. Non-zero lists the specific pages.

### 5. Verify independently for big batches (≥ 50 pages)

```bash
python scripts/verify_batch.py <original folder>
python scripts/verify_batch.py <original.pdf> --output <out.pdf>
```

It recomputes retention and residue from scratch using the output naming rule,
so it catches what self-checks miss: wrong output filenames, silently lost
content, and header logos that survived. Always run it before telling the user
a large batch is done.

### 6. Spot-check 2–3 pages by eye

Confirm headings, page numbers, handwritten formulas and diagrams are intact,
and that no diagonal ghost lines remain on near-blank pages (back covers and
chapter dividers expose residue most readily).

## How it works

### Translucent text watermark

The watermark is a uniform colour at uniform opacity over paper white:

```
observed = α · watermark_colour + (1 - α) · paper
```

so every watermark pixel lies on a **ray from the white point** in chroma space.
Real content does not lie on that ray, which makes the split exact:

1. **Colour cone** — pink: `r-g ∈ [6,62]` and `|b-g| ≤ 10`; purple:
   `b-g ∈ [4,32]` and `|r-g| ≤ 10`. Cyan table rules (`r-g ≈ -20`) and grey
   figures (luma < 180) fall outside naturally.
2. **Paper neighbourhood** — a pixel counts as "on paper" when ≥ 50% of its 9×9
   window is bright (luma ≥ 225). Judging by luma rather than "near white"
   matters: pale watermark pixels must count as paper themselves, otherwise
   faint watermarks filter themselves out.
3. **Ink protection** — a pixel is skipped if its 5×5 window contains dark ink
   (min channel < 150) or saturated red (`r-g > 55`, `r > 110`). Where watermark
   crosses a stroke only a barely visible tint remains.
4. **Faint residue pass** — a second window (very high luma, weak chroma) clears
   the diagonal ghost lines that otherwise show on near-blank pages.

### Printed header logo

Not translucent at all — it is flat opaque colour, so colour alone is unsafe
(body illustrations can contain the same hue). Constraints matter:

1. **Header band only** — top 2%–15% of page height. A yellow illustration in
   the body will otherwise be erased.
2. **Colour wedge** — main colour (255,192,0): `r ≥ 240`, `g ∈ [150,235]`,
   `b ≤ 60`, `r-b ≥ 150`. A blue frame at (79,129,189) fails on `b`, so the
   decorative frame survives.
3. **Shape test** — the topmost cluster must be ≤ 70px tall, 120–420px wide,
   300–8000 px in area. If it fails, treat the page as having no logo. Missing a
   logo is acceptable; eating content is not.
4. **Antialias halo** — warm pixels (`r ≥ 200`, `r-b ≥ 8`) within 4px of the
   glyphs are whitened too. Cool colours (`b > r`) are untouched, so the frame
   and rule line stay.

Because the logo is opaque colour, it also counts as "red" and "dark" content.
The reported retention therefore **excludes the logo region** (dilated 5px);
without that exclusion a blank page would report 0% red after a correct removal.

## PDF specifics

PDF watermarks of this kind are **not PDF objects** — the page has no text layer
(`get_text()` returns empty) and the watermark is baked into the scan bitmap.
There is no object to delete, so the pipeline rasterises:

```
PDF ──render 300dpi──> bitmap ──pixel cleanup──> bitmap ──repackage──> PDF
```

Two gotchas worth remembering:

- Render every page with `get_pixmap()`. Do **not** grab the largest embedded
  image to save time — some pages are collages of several smaller images, and
  the largest one may be a figure rather than the page.
- Write back at the original physical page size and encode JPEG at quality 98.
  Measured on a 130-page bundle: q88 damaged pale-blue antialiased edges
  (blue retention 98.7%) and its noise landed inside the faint-watermark window
  producing ~1078 false residue px/page; q98 drops residue to ~21px, while q100
  saves 4px more for 18% extra size.

Output PDF is rasterised, so text is no longer selectable. For born-digital PDFs
prefer deleting the watermark object with a PDF editor instead.

## Tuning

| Symptom | Fix |
|---|---|
| Content touched, strokes thinned | raise `--near` to 7 (more conservative) |
| Watermark remains in patches | lower `--near` to 3–4, or widen the cone in `wmcore.py` |
| Residue on near-blank pages | `FAINT` window too narrow — widen `lo`/`hi` |
| Header logo untouched | colour differs from (255,192,0) — recalibrate `LOGO_CORE` in `wm_pdf.py` |
| Body colour illustration erased | header band too tall, or shape test too loose — tighten both |

## Resources

### scripts/
- `remove_watermark.py` — single entry point for images and PDF, with metrics.
- `wmcore.py` — colour-cone watermarks: masks, ink protection, batch driver,
  retention/residue metrics. Pure numpy + pillow, no scipy, no network.
- `wm_pdf.py` — PDF rasterise/repack plus header-logo detection and removal.
  `logo_only()` also cleans logos on plain images without pymupdf installed.
- `verify_batch.py` — independent verifier for images and PDF.

### references/
- `watermark-signature.md` — how to sample the colour, derive thresholds, and
  read the anomaly table (ghost lines, clipped content, pink residue on strokes).
- `pdf-and-logo.md` — PDF pipeline details and header-logo calibration
  worksheet.
