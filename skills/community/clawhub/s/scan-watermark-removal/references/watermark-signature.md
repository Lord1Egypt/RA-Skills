# Watermark colour calibration

Default constants in `scripts/wmcore.py` are calibrated on pale pink and pale
purple translucent text over white paper. When a new source deviates, measure
first, then adjust — never guess.

## 1. Sample the watermark colour

Take a patch of paper that carries watermark but no content (back cover, chapter
divider, or a blank margin). Stats on the glyph pixels:

```python
from PIL import Image
import numpy as np

a = np.asarray(Image.open(path).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# pale but not pure white
cand = (r > 190) & (np.minimum(np.minimum(r, g), b) > 150) & (r < 253)
px = a[cand]
print("mean", px.mean(axis=0).round(1))
print("min ", px.min(axis=0))
print("r-g p5/p50/p95", np.percentile(px[:, 0] - px[:, 1], [5, 50, 95]).round(1))
print("b-g p5/p50/p95", np.percentile(px[:, 2] - px[:, 1], [5, 50, 95]).round(1))
```

Also confirm the paper base, which should be pure white on a clean scan:

```python
white = a[(r > 250) & (g > 250) & (b > 250)]
print("paper", white.mean(axis=0).round(1))
```

## 2. Derive thresholds

The watermark is a uniform colour `W` at uniform opacity `α` over white:

```
observed = α · W + (1 - α) · 255
```

which means **chroma differences** (`r-g`, `b-g`) are nearly independent of `α` —
that is why the cones are expressed in differences rather than absolute RGB. The
opacity only scales how far the pixel travels along the ray.

| Quantity | Meaning | How to set |
|---|---|---|
| `lo`, `hi` | window on the cone's own axis (`r-g` for pink, `b-g` for purple) | median ±20, widened until the darkest glyph pixels are included |
| `perp` | tolerance on the orthogonal axis | keep 10; glyphs have `g≈b` (pink) or `r≈g` (purple) |
| `mx_min` | max-channel floor | 70–80% of the darkest glyph pixel's max channel |
| `mn_min` | min-channel floor | 70–80% of the darkest glyph pixel's min channel |

Measured reference points (300 dpi scans, white paper):

| Watermark | Typical glyph colour | `r-g` | `b-g` |
|---|---|---|---|
| pink | (244,191,191) | 53 | 0 |
| pink, faint edge | (255,229,229) | 26 | 0 |
| purple | (200,190,215) | 10 | 25 |
| header logo | (255,192,0) | 63 | 192 |

Content-protection constants rarely need changing: dark ink is `min < 150`,
saturated red is `r-g > 55` with `r > 110`. If the source is written in blue-black
ink, extend the ink test with something like `|r-b| > 55 and b > 110` measured
from the actual strokes.

## 3. Anomaly table

| Symptom | Cause | Fix |
|---|---|---|
| Faint diagonal ghost lines on near-blank pages | the lowest-opacity edge of the watermark falls below the main window | the `FAINT` window covers this; if any survives, lower its `lo` from 3 to 2 and `mn_min` from 230 to 228 |
| `residue` still > 50 on some pages | that page's watermark colour deviates from calibration | re-measure that page, nudge the window |
| Red pen thinned (`red` < 100%) | antialiased stroke edges entered the pink cone | raise the pink `lo` from 6 to 10, or check whether the pen itself is pale pink (then it is genuinely ambiguous — prefer keeping content) |
| Pink fringe where watermark crosses handwriting | by design — pixels adjacent to ink are skipped | normal and invisible at 100%; only use `--near 1` for a specific page if the user insists, then re-check `red` |
| Yellowed or grey old scan | paper base is not 255 white, so the luma floor misses the watermark | measure paper base and scale all `mx_min` / `mn_min` down proportionally; lower `FAINT.mx_min` toward the brightest paper value |
| Whole page unchanged | watermark is actually opaque printed text, not translucent | that is the header-logo family — see `pdf-and-logo.md` |

## 4. Post-change checklist

1. Re-run the full batch. `red%` / `dark%` must be ≥ 99.0, `residue` ≤ 50.
2. Eyeball one near-blank page (ghost lines) and one densest handwriting page.
3. Diff the output against the previous run to confirm only intended regions
   changed.
4. Re-run `verify_batch.py` — it does not reuse the remover's own metrics.
