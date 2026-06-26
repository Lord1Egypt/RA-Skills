# ffmpeg pipeline (postprocess.js internals)

What `node postprocess.js` actually does to turn `raw.webm + events.json` into `final.mp4`. Read this if you need to tune visuals or debug overlay timing.

## Big picture

```
raw.webm        ─┐
cursor.png      ─┤── ffmpeg filter_complex ──→ final.mp4
ripple.png      ─┤
subs.srt        ─┘
```

Layers (bottom to top in the composition):

1. **raw.webm** (cursorless playwright recording)
2. **Ripple overlays** at every click point (2 staggered rings)
3. **Ghost cursor trail** (2 trailing copies of cursor.png, lower alpha)
4. **Main cursor** (full alpha cursor.png)
5. **Burned subtitles** (libass via `subtitles=` filter)
6. **Persistent masks** (split → crop+boxblur → overlay; one per mask region; ALWAYS top layer so masks cover cursor and subtitles within the masked area)

## Cursor lerp model

Cursor position is a piecewise linear function of video time, built from `move` + `click` events.

Pseudo-code:

```
events = [{t: 0,    pos: (120, 179)},   // first cursor event sets start position
          {t: 1.5,  pos: (428, 659)},   // lerp from (120,179) to (428,659) over 1.5s
          {t: 3.0,  pos: (428, 659)},   // click at same position — lerp endpoint
          {t: 5.5,  pos: (428, 659)},   // [REST event injected at next.t - 0.45s]
          {t: 6.0,  pos: (1022, 748)},  // lerp from rest to next move over 0.45s
          ...]
```

The REST events injected by `addRestEvents` are crucial: without them, cursor would drift slowly across the entire 2-3s gap between clicks. With them, cursor sits still then lerps quickly (450ms) into the next position right before the click — much more like a real user.

## Ripple structure

Each `click` event spawns 2 ring overlays at the click point:

| Frame | Size | Alpha | Time window |
|---|---|---|---|
| Inner pulse | 32×32 | 0.92 | `[t, t+0.28s]` |
| Outer expanding fade | 80×80 | 0.30 | `[t+0.08s, t+0.42s]` |

The two-ring trick approximates a Material expanding ripple: a bright snap at the click point, plus a wider, fainter fade outward.

If you want to retune the ripple visuals, edit `RIPPLE_FRAMES` in `postprocess.js`. Adding more frames (e.g. a third 120×120 ring at alpha 0.12) increases ffmpeg complexity quadratically with click count, so beware on long recordings.

## Subtitle rendering

Subtitles use libass (compiled into ffmpeg-static). Style is set via `force_style` in the `subtitles=` filter:

```
FontName=<platform-detected>,Fontsize=16,
PrimaryColour=&Hffffff&,        # white text
OutlineColour=&H00000000&,      # transparent outline
BackColour=&H99000000&,         # 60% opaque black box (BorderStyle=4)
BorderStyle=4,                  # opaque box behind text
Outline=1.5,
Shadow=0,
MarginV=42,                     # 42px from bottom
Alignment=2                     # bottom-center
```

To change font / size / position, edit `subStyle` in `postprocess.js`. To use a different font for one specific run, set `SUBTITLE_FONT="<font name>"` env var.

## CALIBRATION constant

`CALIBRATION = 0.65` is the offset between Playwright's `newPage()` and the script's `tStart = Date.now()`. Empirically measured to be 600-700ms. Without this, every event in the final video would appear ~0.65s late.

If you change Playwright versions or run on a much slower machine, this may need recalibration. Symptoms of bad calibration:
- Subtitles appear before the action they describe → `CALIBRATION` too low
- Subtitles appear after the action → `CALIBRATION` too high

To recalibrate: do a manual recording with a known landmark event (e.g. a click that triggers a visible state change), measure the offset between event timestamp and visible state change in `final.mp4`, adjust `CALIBRATION` to match.

## REST_LEAD constant

`REST_LEAD = 0.45` controls how long before the next move the cursor "wakes up" and starts lerping. Smaller = cursor moves later but faster (snappy); larger = cursor moves earlier and slower (drifty).

0.45s is a sweet spot tested over a 2-minute demo with ~22 clicks. Below 0.3 the cursor feels jerky; above 0.6 it visibly drifts.

## Why pre-compose ripple frames

The ripple section uses ffmpeg `split` to make N copies of each ripple frame stream (one per click). This is because ffmpeg filter pads are single-use — overlay-ing the same input N times in different time windows would error. The `split=N[rf0_0][rf0_1]...[rf0_N-1]` trick gives each click its own fresh copy.

Side effect: the filter graph length scales linearly with click count × ripple frames. A 100-click recording with 2 ripple frames produces a 200-overlay chain, which ffmpeg handles fine but is slow to parse on startup (~2s overhead).

## Persistent mask filter chain

Each `mask_persistent` event becomes 3 filter steps:

```
[in]  split=2  [main][crop_input]
[crop_input]  crop=W:H:X:Y, boxblur=lr=20:lp=2:cr=15:cp=2  [blurred]
[main][blurred]  overlay=x=X:y=Y  [out_i]
```

`split=2` is required because ffmpeg filter pads are single-use — you can't both keep the original stream as the base AND consume it for the cropped region in one chain.

Layered mask order: masks earlier in `PERSISTENT_MASKS` are applied first, so later entries paint over earlier ones if regions overlap. In practice, mask regions don't overlap, so order doesn't matter.

`boxblur=lr=20:lp=2:cr=15:cp=2` settings:
- `lr=20` = luma radius (higher = blurrier; subjective sweet spot is 15-30)
- `lp=2` = luma power / iterations (more iterations smooth out the box pattern; 2 is enough)
- `cr=15` = chroma radius (ffmpeg caps this at 15 — that's why we set lr/cr separately rather than `boxblur=20:2`)
- `cp=2` = chroma power, matching luma for consistency

For tighter blur (when small text is still readable): try `lr=40:lp=3:cr=15:cp=3` or replace with `gblur=sigma=15` (proper Gaussian; somewhat slower).

For "mosaic block" effect instead of smooth blur, replace the `boxblur=...` with `pixelize=20:20` (where 20 is the block size). Less convex visually but unmistakable as deliberate.

The mask layer is inserted AFTER `subtitles=`, so the masked area is unconditionally unreadable regardless of cursor / ripple / subtitle activity beneath.

## Output codec

```
-c:v libx264
-pix_fmt yuv420p
-preset medium
-crf 20
-r 30
```

CRF 20 is "visually lossless for screencasts". Preset medium is the speed/quality sweet spot. Output is 30fps regardless of input fps (Playwright records at variable rate; this normalizes).

For smaller files: bump `-crf` to 23 (~30% smaller, slight banding in dark gradients).
For higher quality: `-crf 18` and `-preset slow`.
