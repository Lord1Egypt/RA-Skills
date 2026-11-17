# windows-region-exact-record

Record an exact-length clip of a fixed screen rectangle on Windows. Three things actually go wrong, and this solves all three: **coordinates that are off by a factor of two under display scaling**, **duration that drifts by seconds**, and **the recording indicator ending up inside the video**.

## The high-DPI trap

A process that has not declared DPI awareness receives **logical** pixels from `GetCursorPos` and window rectangles. `ffmpeg -f gdigrab` wants **physical** pixels for `-offset_x`, `-offset_y` and `-video_size`.

At 200% scaling, a region that looks like 1200×800 records as **600×400** and shifts toward the top-left. The fix is one call at process start:

```python
ctypes.windll.shcore.SetProcessDpiAwareness(2)   # per-monitor, Win8.1+
```

Test it: a 1200×800 selection must produce a 1200×800 video, pixel for pixel. Getting 600×400 means logical pixels leaked in — that is not an ffmpeg tuning problem.

## Recording

```
ffmpeg -f gdigrab -offset_x X -offset_y Y -video_size WxH -framerate 30 -i desktop \
       -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p out.mp4
```

Stop by writing `q` to the stdin of ffmpeg. Never kill it, or the `moov` box stays incomplete and the file reads as zero seconds.

## Measured on 3840×2160 at 200% scaling

| Case | Result |
|---|---|
| Self-test, 1200×800, 4 s | 1200×800 / 30 fps / 4.13 s / 123 frames |
| `--sec 5` auto-stop | 5.20 s |
| Manual stop at about 25 s | 25.30 s |
| Outer 6 px band mean colour | (248,243,249) / (255,255,255), not the red (234,31,33) ⇒ indicator not in frame |

## What you get

- `scripts/rec_region.py` — CLI with `--pick`, `--region`, `--sec`, `--check` and `--countdown`
- `scripts/pick_region.py` — two-click picker and the sole owner of `set_dpi_aware()`
- `scripts/rec10s.bat` — double-click: pick two corners, countdown, record 10 seconds
- `scripts/region_rec_gui.py` — pure `ctypes` GUI with zero tkinter or PyQt dependency, including a mouse-free `--selftest`

## Known limits

Single monitor only; gdigrab offsets are measured from the top-left of the primary display. No audio capture.

MIT.
