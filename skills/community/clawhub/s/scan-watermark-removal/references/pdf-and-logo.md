# PDF pipeline and header-logo calibration

## Why rasterise

Course PDFs of this kind have no text layer — `page.get_text()` returns `''` —
and the watermark is baked into the scan bitmap. There is no object to delete, so
the only deterministic route is raster:

```
PDF ──render 300dpi──> bitmap ──pixel cleanup──> bitmap ──repackage──> PDF
```

Consequences to state up front to the user:

- output pages are images, so text is no longer selectable or searchable
- file size grows (roughly 1 MB/page at quality 98 for A4 at 300 dpi)
- page geometry is preserved exactly (A4 = 595.276 × 841.89 pt)

If the PDF *is* born-digital, skip this entirely and delete the watermark object
with a PDF editor.

## Render, do not extract

Always use `page.get_pixmap(dpi=300)`.

Tempting shortcut: grab the largest embedded image via
`page.get_images()` + `doc.extract_image()`, which is lossless and faster. It
breaks on collage pages — a page built from a background plus several figure
images will hand you the largest figure instead of the page. Observed failure: a
page came back as a 1390×1530 crop of a yellow aeroplane illustration rather than
the 2481×3508 page, and the logo detector then erased part of the aeroplane.

Rendering costs about 0.14 s/page at 300 dpi, i.e. ~18 s for 130 pages, plus
about 1.4 s/page for the pixel work. Acceptable.

## Repack and encode

Write each page as a full-page image at the original `page.rect` size. Encode
JPEG; quality matters more than expected:

| quality | size/page | residue px | blue retention |
|---|---|---|---|
| 88 | 602 KB | 1078 | 98.7% |
| 95 | 795 KB | 151 | 99.4% |
| **98** | **981 KB** | **21** | **101.9%** |
| 100 | 1164 KB | 17 | 100.7% |

q88 is a trap on two counts: it damages pale-blue antialiased edges enough to
drop blue retention below 100%, and its ringing noise lands inside the faint
watermark window, producing over a thousand false residue pixels per page. q98 is
the knee; q100 buys 4 px for 18% more size.

## Header logo calibration

The header logo is flat opaque colour, not a translucent overlay, so it needs its
own detector.

### Why colour alone is not enough

Body illustrations can contain the same hue. A page in the sample bundle has a
yellow aeroplane at y ≈ 1200 of 3508. A whole-page orange filter would erase it.
Two constraints make it safe:

1. **Header band** — restrict to `y/H ∈ [0.02, 0.15]`.
2. **Shape test** — the cluster must look like a short word, not a drawing.

### Measure the logo colour

```python
import numpy as np
from PIL import Image

a = np.asarray(Image.open(page_png).convert("RGB")).astype(int)
band = a[int(0.02 * a.shape[0]):int(0.15 * a.shape[0])]
r, g, b = band[:, :, 0], band[:, :, 1], band[:, :, 2]

# saturated warm wedge
m = (r >= 240) & (g >= 150) & (g <= 235) & (b <= 60) & ((r - b) >= 150)
px = band[m]
print("count", m.sum(), "mean", px.mean(axis=0).round(1))

ys = np.nonzero(m.any(axis=1))[0]
print("rows", ys.min(), ys.max(), "height", ys.max() - ys.min() + 1)
xs = np.nonzero(m.any(axis=0))[0]
print("cols", xs.min(), xs.max(), "width", xs.max() - xs.min() + 1)
```

Measured on the reference bundle (300 dpi A4, 2481×3508):

| Quantity | Value |
|---|---|
| logo colour | (255,192,0) |
| cluster height | 40–45 px |
| cluster width | 210–233 px |
| cluster pixel count | 2000–2620 |
| vertical position | y/H 0.066–0.109 |
| pages carrying it | 128 of 130 (one blank, one vector-only) |

Note the position varies between pages — odd and even pages place the logo on
opposite sides, and merged documents put it at different heights. Never hardcode
coordinates; detect by content.

### Constants in `wm_pdf.py`

Shape limits are **fractions of the page**, not absolute pixels. The same scan at
150 dpi puts the logo at 116×22 px instead of 232×45 — an absolute rule calibrated
at 300 dpi silently misses it.

```python
LOGO_CORE = dict(r_min=240, g_min=150, g_max=235, b_max=60,
                 rb_min=150, gb_min=90)
LOGO_H_FRAC     = (0.005, 0.030)   # cluster height / page height
LOGO_W_FRAC     = (0.040, 0.220)   # cluster width  / page width
LOGO_FILL       = (0.10, 0.45)     # core px / bbox area — text is sparse strokes
LOGO_MIN_PIXELS = 100              # absolute floor, rejects noise
LOGO_MAX_PIXELS = 8000             # absolute ceiling (a figure has ~24k)
HEADER_BAND_TOP = 0.02
HEADER_BAND_BOT = 0.15
```

The fill-ratio test is what separates lettering from solid shapes: measured text
fill is 0.21–0.25, while a filled glyph block or illustration sits well above.

If the logo fails to be removed, it is almost always because its colour is not in
the wedge — measure and adjust `LOGO_CORE` first, before touching the shape test.

### Removal is three passes, not one

1. **Core** — pixels inside the wedge are whitened.
2. **Halo** — warm pixels within 4 px of the core are whitened (antialias fringe).
3. **Bbox sweep** — inside the glyph cluster's bounding box (+6 px), every pixel
   that is warm (`r-b ≥ 8`, `r ≥ g-2`), not dark (`min > 140`) and not
   blue-dominant (`b ≤ r`) is whitened.

The third pass exists for low resolution. At 150 dpi the glyph core is blended
enough that much of it fails the `b ≤ 60` wedge test, and passes 1–2 leave a pale
tan ghost of the whole word. The bbox interior contains only white paper and the
blue frame, and the frame is cool (`b > r`), so the sweep cannot damage it.

### Metrics must exclude the logo region

The logo is opaque orange, so it satisfies both the "red content" test
(`r-g = 63 > 60`, `r-b > 60`) and the "dark content" test (`min channel = 0 <
150`). Removing it therefore *lowers* reported retention unless the region is
excluded. Exclude the dilated mask (5 px) on both sides of the comparison.

Without that exclusion, a blank page that correctly lost its logo reports
`red = 0%` — a terrifying-looking number that means nothing. With it, the same
page reports 100%.

### Interpreting retention below 100%

**Do not gate on the percentage.** The shipped gate is `erased_content()`: pixels
that were unambiguously content (dark `min < 120`, saturated red, saturated blue)
and are now near-white. That must be 0.

Retention percentages are a coverage reference only, because JPEG re-encoding
shifts the palest antialiased edges by a few units, pushing 1–2% of them below the
"is this content" threshold. This is a counting artefact, not damage — and it is
large enough that a percentage gate either fails correct output (as it did here:
91.6% on a page with zero loss) or gets loosened until it stops catching anything.

When you do want to audit the percentage, print the original min channel of every
pixel that lost a category:

- deficit from pixels with `min ∈ [120,150]` → antialiased edges shifted a few
  units by JPEG re-encoding; content is visually intact
- deficit from pixels with `min < 100` → real content loss, investigate

On the reference bundle the worst pages reported 91.6% dark retention; every
single lost pixel had `min ∈ [143,149]`, and `erased_content()` returned 0.

### Residue: count is the wrong gate for JPEG

`residue_count` asks "are there watermark-coloured pixels sitting on clean
paper?" On a PNG output a positive count means a real leftover. On a JPEG output
it does not: ringing around text produces 1–15 unit chroma jitter on white paper,
which lands inside the faint-watermark window. Measured on a 130-page bundle:

| page | raw residue | residue with `min < 240` |
|---|---|---|
| 77 | 6803 | 0 |
| 83 | 5600 | 0 |
| 106 | 14747 | 0 |

Thousands of pixels, none of them darker than 240 — completely invisible. So gate
on `residue_profile()`, which returns `(total, visible)` where visible counts
pixels with `min < 235`. **Visible should be 0.** Raw count is only useful as a
trend signal within one output format.

This is why the CLI and verifier use different retention thresholds for images and
PDF, and why both gate on visible residue rather than raw count.
