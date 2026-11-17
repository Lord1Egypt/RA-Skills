# scan-watermark-removal

Deterministically remove light translucent text watermarks from scanned paper
pages — lecture notes, handouts, exam papers, workbooks — as **images or PDF**,
plus printed coloured **header logos**.

No model. No generative redraw. No network. Red pen, black print, blue table
rules, grey figures and colour illustrations survive intact, verified by pixel
accounting on every page.

```
input scan ─┬─ translucent watermark  → colour-cone isolation
            └─ printed header logo     → colour wedge + shape test (header band)
```

## Why deterministic

The watermark is a uniform colour at uniform opacity over paper white:

```
observed = α · watermark_colour + (1 - α) · paper
```

Every watermark pixel therefore lies on a **ray from the white point** in chroma
space, and real content does not. That makes the separation exact instead of
approximate — no generative model, no redrawing, no per-page review.

Contrast with generative image editing on the same material: on a dense
handwriting page it repaints the page and swallowed about 75% of the red ink, then
left pink fringes around the surviving strokes. That is why this tool exists.

## Install

```bash
pip install numpy pillow          # core
pip install pymupdf               # only for PDF input
```

Use it as an agent skill: copy the folder into your skills directory, or

```bash
clawhub install scan-watermark-removal
```

## Use

```bash
# image folder or single image
python scripts/remove_watermark.py <folder_or_image>

# PDF
python scripts/remove_watermark.py notes.pdf --output notes_clean.pdf

# keep the header logo
python scripts/remove_watermark.py notes.pdf --no-logo
```

Defaults: images go to `<input>/去水印输出/` with suffix `_去水印`; PDF goes to
`<name>_去水印.pdf`. **Originals are never modified.**

| Flag | Meaning |
|---|---|
| `--output` | output folder (images) or output `.pdf` (PDF) |
| `--near N` | ink-protection window in px, default 5. Smaller = more aggressive |
| `--suffix S` | output filename suffix, default `_去水印` |
| `--no-pink` / `--no-purple` | disable one watermark family |
| `--no-logo` | keep the printed header logo |
| `--all` | also reprocess files already carrying the suffix |

Exit code `0` = every page passed; `1` = specific pages are listed for review.

## Verify independently

Self-checks can be wrong, so there is a second opinion that recomputes
everything from scratch:

```bash
python scripts/verify_batch.py <original folder>
python scripts/verify_batch.py <original.pdf> --output <out.pdf>
```

It re-derives retention and residue from the output naming rule and flags wrong
filenames, silently lost content, and surviving logos.

## Acceptance gate

Every page reports:

- `erased` px → **must be 0.** Pixels that were unambiguously content (dark
  `min < 120`, saturated red, saturated blue) and are now near-white. This is the
  real safety metric.
- `residue` px + `visible` in parentheses → watermark pixels on clean paper, and
  how many are dark enough to see. **Visible must be ~0.** Raw count reaches the
  thousands on a JPEG page purely from ringing and means nothing.
- `red / dark / blue` retention % → coverage reference, expected ≥ 90.

`erased` beats a retention-percentage gate. JPEG re-encoding shifts the palest
antialiased edges a few units, pushing 1–2% of them below the "is this content"
threshold, so retention can read 91% on a page that lost zero real pixels. A
percentage threshold either fails correct output or gets loosened until it hides
real damage. Counting *documented content that vanished* has neither failure mode.

To audit the old way anyway: for each lost pixel, print its original min channel.
Deficits from `min ∈ [120,150]` are edge jitter; `min < 100` is real loss.

## Measured results

| Source | Pages | Watermark | Header logo | Residue | Retention |
|---|---|---|---|---|---|
| Course-note PDF bundle | 130 | pink diagonal | 128 pages cleared | ~21 px/page | 100 / 100 / 100 % |
| Lecture handouts, scans | 487 | pink | — | 0 | 100.0% |
| Handouts, later chapters | 213 | pink | — | 0 | 100.0% |
| PDF-extracted pages | 41 | purple + pink | — | 0 | 100.0% |

## Scope and limits

- Translucent **light** overlays only. Dark, saturated or photographic logos are
  out of scope.
- Header-logo detection is tuned to flat opaque colour. A differently coloured
  logo needs `LOGO_CORE` recalibrated in `scripts/wm_pdf.py`.
- Where watermark colour approaches content colour, ink protection bails out and
  leaves a faint tint. That is the intended trade — never trade content for a
  cleaner background.
- PDF output is rasterised, so text is no longer selectable. For born-digital
  PDFs, delete the watermark object with a PDF editor instead.
- Output PDF is larger than the source (~1 MB/page at quality 98).

## Layout

```
SKILL.md                      agent-facing instructions and acceptance gate
scripts/remove_watermark.py   single entry point, images and PDF
scripts/wmcore.py             colour cones, ink protection, batch driver, metrics
scripts/wm_pdf.py             PDF rasterise/repack, header-logo detector
scripts/verify_batch.py       independent verifier
references/watermark-signature.md   colour calibration and anomaly table
references/pdf-and-logo.md          PDF pipeline and logo calibration worksheet
```

## License

MIT
