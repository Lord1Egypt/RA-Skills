"""Build the lyric video: ComfyUI art plate + audio-reactive spectrum + word-synced lyrics.

Frames are drawn with Pillow and piped to ffmpeg as rawvideo, which avoids writing
8000 PNGs to disk.

Three layers, back to front:
  1. the generated artwork, with a slow Ken Burns push and a soft crossfade at each
     scene change, dimmed so text stays readable;
  2. a mirrored spectrum that follows the music, plus a beat pulse on the art;
  3. the English lyric line, with the syllable being sung at this instant lit up.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from _env import LIBS, pil_font

sys.path.insert(0, str(LIBS))


import numpy as np
import soundfile as sf
import soxr
from PIL import Image, ImageDraw, ImageFont

FPS = 30
W, H = 1280, 720
SR = 44100


# Which picture belongs to which line. Keyword matching was tried first and failed:
# most lines contain none of the words you would guess, so nearly every span
# collapsed onto the title plate and the video sat on one image. The mapping is
# keyed on the lyric text itself and follows the song's own imagery -- fate and
# stars for the opening, the blade and lanterns for the vengeance verses, the lone
# isle for the lonely middle, the coffin for the end. Keying on text (rather than
# row index) matters because align.json repeats each chorus line, so the 52 rows
# hold only 28 distinct lyrics.
SCENE_BY_TEXT = {
    "Where will I find you": "title",
    "Was it written before": "stars",
    "Flying through time and space": "stars",
    "Caught in the blade's embrace": "blade",
    "March blooms wake one by one": "bloom",
    "Who grows old as years run": "bloom",
    "Ruin or fate for me": "stars",
    "With you no foe can touch me": "blade",
    "When the debt is half": "jianghu",
    "How do I hold back": "jianghu",
    "Lanterns glow with hate": "lantern",
    "Vengeance comes too late": "lantern",
    "Moonlit gate boy sighs": "gate",
    "Peaceful Chang'an lies": "gate",
    "When the stars set": "stars",
    "My fate is set": "stars",
    "Wait till ink dries": "title",
    "Nemesis arrives": "blade",
    "I borrowed all your pain": "isle",
    "Can't give it back again": "isle",
    "Snow haunts the lone isle": "isle",
    "Falling, mile by mile": "isle",
    "Pluck a star from sea": "isle",
    "Stay the night with me": "gate",
    "Coffin sleeps in the vale": "valley",
    "No secret can prevail": "valley",
    "Jianghu ends in pain": "jianghu",
    "No one breaks the chain": "jianghu",
}


def pick_scene(i: int, en: str) -> str:
    return SCENE_BY_TEXT.get(en.strip(), "title")


def build_spectrum(path: Path, n_frames: int, n_bands: int = 64):
    """Log-spaced band energies per video frame, normalized to 0..1."""
    y, sr = sf.read(str(path), dtype="float32", always_2d=True)
    y = y.mean(axis=1)
    if sr != SR:
        y = soxr.resample(y, sr, SR)
    hop = SR // FPS
    n_fft = 2048
    win = np.hanning(n_fft).astype(np.float32)

    pad = n_fft // 2
    yp = np.pad(y, (pad, pad))
    out = np.zeros((n_frames, n_bands), dtype=np.float32)
    freqs = np.fft.rfftfreq(n_fft, 1.0 / SR)
    # 55 Hz .. 12 kHz in log space; below 55 Hz just muddies a small screen
    edges = np.geomspace(55.0, 12000.0, n_bands + 1)
    idx = np.searchsorted(freqs, edges)
    for f in range(n_frames):
        s = f * hop
        if s + n_fft > len(yp):
            break
        mag = np.abs(np.fft.rfft(yp[s:s + n_fft] * win))
        db = 20.0 * np.log10(np.maximum(mag, 1e-7))
        for b in range(n_bands):
            lo, hi = idx[b], max(idx[b] + 1, idx[b + 1])
            out[f, b] = db[lo:hi].mean()
    # map -80..-10 dB onto 0..1, then smooth so bars glide instead of flicker
    out = np.clip((out + 80.0) / 70.0, 0.0, 1.0)
    # Convert to a fraction of each band's dynamic range above a fixed floor. The
    # floor keeps the strip visible during quiet passages instead of letting the
    # whole meter collapse to nothing, and the ceiling stops the bass bands from
    # sitting pegged at the top for the entire song.
    for b in range(out.shape[1]):
        col = out[:, b]
        lo = np.percentile(col, 8)
        hi = np.percentile(col, 98)
        if hi - lo > 0.05:
            out[:, b] = np.clip((col - lo) / (hi - lo) * 0.85 + 0.12, 0.0, 1.0)
        else:
            out[:, b] = 0.15
    for _ in range(2):
        out = 0.65 * out + 0.35 * np.vstack([out[:1], out[:-1]])
    return out


def load_fonts():
    return {
        "lyric": pil_font("en", 46),
        "small": pil_font("en_r", 26),
        "title": pil_font("en", 84),
        "cn": pil_font("cn", 34),
    }


def build_timeline(align, art: dict, duration: float):
    """Scene spans derived from what is being sung, so a picture never outlives its line."""
    spans = []
    for i, r in enumerate(align):
        key = pick_scene(i, r["en"])
        if key not in art:
            key = "title"
        start = r["t"] if i == 0 else max(r["t"], align[i - 1]["t"] + 0.1)
        end = align[i + 1]["t"] if i + 1 < len(align) else min(duration, r["t"] + r["sung_s"] + 3.0)
        if spans and spans[-1][2] == key and start - spans[-1][1] < 0.5:
            spans[-1][1] = end
        else:
            spans.append([start, end, key])
    spans.insert(0, [0.0, spans[0][0], "title"])
    if spans[-1][1] < duration:
        spans.append([spans[-1][1], duration, "title"])
    return spans


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--audio", default=None, help="defaults to 06/mix.wav")
    ap.add_argument("--out", default=None, help="defaults to 07/lyric_video.mp4")
    ap.add_argument("--fps", type=int, default=FPS)
    a = ap.parse_args()

    run = Path(a.run_dir)
    out_dir = run / "07"
    out_dir.mkdir(parents=True, exist_ok=True)

    audio = Path(a.audio) if a.audio else run / "06" / "mix.wav"
    y, sr = sf.read(str(audio), dtype="float32", always_2d=True)
    duration = y.shape[0] / sr
    n_frames = int(round(duration * a.fps))
    print(f"audio {audio.name}: {duration:.2f}s -> {n_frames} frames @ {a.fps}fps", flush=True)

    align = json.loads((run / "05" / "align.json").read_text(encoding="utf-8"))
    art = json.loads((out_dir / "art" / "art.json").read_text(encoding="utf-8"))
    art = {k: Image.open(v).convert("RGB").resize((W, H), Image.LANCZOS)
           for k, v in art.items()}
    print(f"art: {len(art)} scenes, lyrics: {len(align)} lines", flush=True)

    spans = build_timeline(align, art, duration)
    print(f"timeline: {len(spans)} scenes", flush=True)
    for s in spans:
        print(f"  {s[0]:7.2f}-{s[1]:7.2f}  {s[2]}", flush=True)

    spec = build_spectrum(audio, n_frames)
    print(f"spectrum: {spec.shape}", flush=True)

    fonts = load_fonts()
    # one flat list of (start, end) per word for the highlight test
    words = [(w["t0"], w["t1"], r["en"]) for r in align for w in r["words"]]
    # Line spans come from where the words are actually sung, not from the LRC
    # timestamps: the lyric file drifts from this recording by up to six seconds, so
    # using r["t"] would put a line on screen before (or after) the voice sings it.
    def _span(r):
        ws = r["words"]
        if ws:
            return ws[0]["t0"], ws[-1]["t1"]
        return r["t"], r["t"] + r["sung_s"]

    by_line = []
    for r in align:
        st, en = _span(r)
        by_line.append((st, en, r, [dict(w) for w in r["words"]]))

    from imageio_ffmpeg import get_ffmpeg_exe
    ffmpeg = get_ffmpeg_exe()
    dst = Path(a.out) if a.out else out_dir / "lyric_video.mp4"
    # mux the audio straight from the mix so picture and sound cannot drift
    cmd = [ffmpeg, "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(a.fps),
           "-i", "pipe:0",
           "-i", str(audio),
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-shortest", "-movflags", "+faststart", str(dst)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    bar_area = 78           # a thin strip along the very bottom, not a curtain over the art
    n_bands = spec.shape[1]
    bar_w = W / n_bands

    for f in range(n_frames):
        t = f / a.fps
        # --- scene plate with a slow push, crossfaded near boundaries
        cur = spans[-1]
        for s in spans:
            if s[0] <= t < s[1]:
                cur = s
                break
        img = art[cur[2]]
        zoom = 1.0 + 0.05 * ((t - cur[0]) / max(cur[1] - cur[0], 0.1))
        cw, ch = int(W / zoom), int(H / zoom)
        cx, cy = (W - cw) // 2, (H - ch) // 2
        frame = img.crop((cx, cy, cx + cw, cy + ch)).resize((W, H), Image.BILINEAR)

        nxt_i = spans.index(cur) + 1
        fade = 0.7
        if nxt_i < len(spans) and spans[nxt_i][0] - t < fade:
            k = 1.0 - (spans[nxt_i][0] - t) / fade
            frame = Image.blend(frame, art[spans[nxt_i][2]], k * 0.5)

        arr = np.asarray(frame).astype(np.float32)
        # dim + slight cool grade so white type always wins
        arr *= 0.42
        arr[:, :, 2] *= 1.06
        # beat pulse keeps the picture breathing with the music
        level = float(spec[min(f, len(spec) - 1)].mean())
        arr *= (1.0 + 0.16 * level)

        # --- reactive spectrum, as a thin glowing strip hugging the bottom edge
        s = spec[min(f, len(spec) - 1)]
        for b in range(n_bands):
            # gentle gamma so the strip keeps visible shape without vanishing
            hgt = int((s[b] ** 0.9) * (bar_area - 8))
            if hgt <= 1:
                continue
            x0 = b * bar_w
            xa, xb = int(x0) + 1, int(x0 + bar_w) - 1
            if xb <= xa:
                continue
            # glow falls off towards the top of each bar, which reads as light
            # rather than as a painted block
            for k in range(hgt):
                frac = 1.0 - k / max(hgt, 1)
                blend = 0.10 + 0.42 * frac * s[b]
                ya = H - 1 - k
                band = arr[ya:ya + 1, xa:xb]
                if not band.size:
                    continue
                tint = np.array((45 + 70 * s[b], 105 + 90 * s[b], 195 + 55 * s[b]),
                                dtype=np.float32)
                band[:] = band * (1 - blend) + tint * blend

        frame = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

        draw = ImageDraw.Draw(frame)        # --- lyrics: each line stays up until the next one begins, so the screen is
        # never empty between lines (a rest inside a song is not a gap in the words)
        cur_i = -1
        for i, (st, en, line, ws) in enumerate(by_line):
            if st - 0.30 <= t < en + 0.6:
                cur_i = i
                break
        if cur_i < 0:
            # between lines: hold the last one that has started
            for i, (st, en, line, ws) in enumerate(by_line):
                if st <= t:
                    cur_i = i
        if cur_i >= 0:
            st, en, line, ws = by_line[cur_i]
            nxt = by_line[cur_i + 1][0] if cur_i + 1 < len(by_line) else en + 4.0
            # fade the line in at its start and out as the next one takes over
            k = min(1.0, (t - (st - 0.30)) / 0.3) if t > st - 0.30 else 0.0
            k *= min(1.0, max(0.0, (nxt - t) / 0.45))
            if k > 0.02:
                widths = [draw.textlength(w["w"] + " ", font=fonts["lyric"]) for w in ws]
                total = sum(widths)
                x = (W - total) / 2
                y = H - 232
                for w, wd in zip(ws, widths):
                    # Word timings come from the syllable layout, so a word's span can
                    # be far longer than its sound (a held vowel spends whole seconds
                    # on one syllable). Light the word at its start and keep it lit
                    # until the next one begins, which matches what the ear hears and
                    # avoids mid-line flicker.
                    lit = w["t0"] - 0.05 <= t < w["t1"]
                    done = t >= w["t1"]
                    base = (255, 226, 138) if lit else ((236, 240, 248) if done else (168, 176, 194))
                    col = tuple(int(c * k) for c in base)
                    draw.text((x, y), w["w"], font=fonts["lyric"], fill=col,
                              stroke_width=2, stroke_fill=(0, 0, 0))
                    x += wd

        # --- title card over the intro
        if t < spans[1][0]:
            k = min(1.0, t / 1.2) * min(1.0, max(0.0, (spans[1][0] - t) / 1.5))
            col = tuple(int(c * k) for c in (245, 245, 250))
            title = "NEMESIS"
            tw = draw.textlength(title, font=fonts["title"])
            draw.text(((W - tw) / 2, H / 2 - 110), title, font=fonts["title"], fill=col)
            sub = "an English cover of Xu Song's Su Di"
            sw = draw.textlength(sub, font=fonts["small"])
            draw.text(((W - sw) / 2, H / 2 - 10), sub, font=fonts["small"], fill=col)
            cn = "宿敌 · 英文翻唱"
            cw = draw.textlength(cn, font=fonts["cn"])
            draw.text(((W - cw) / 2, H / 2 + 40), cn, font=fonts["cn"], fill=col)

        if f % 300 == 0:
            print(f"  frame {f}/{n_frames} ({t:.1f}s)", flush=True)
        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"wrote {dst}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
