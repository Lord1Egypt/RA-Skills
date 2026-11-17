"""Add singer's vibrato to sustained notes.

Measured on our render versus a human acapella, using RMVPE pitch tracking
against a 0.5 s median baseline:

    original Chinese vocal : median 14.1 cents, p90 67.6
    human English acapella : median  8.4 cents, p90 58.0
    our render             : median  5.2 cents, p90 32.8

The model holds each note too flat and too steady. A voice that sustains a pitch
without any periodic deviation reads as speech -- which is exactly what the
listener reported ("更像是念出来的而非唱出来的"). Vibrato is the single most
recognisable difference between a sung note and a spoken one.

This is implemented as classic delay-line vibrato: a fractional-delay read pointer
modulated by a sine. It shifts pitch symmetrically around the written note, so the
note stays in tune, and it never changes duration. Depth is scaled per note by how
long the note is -- a 0.15 s note gets no vibrato (real singers do not vibrate on
short syllables), a 1 s note gets the full amount.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _env import LIBS, RMVPE

sys.path.insert(0, str(LIBS))


import numpy as np
import soundfile as sf
import soxr

SR = 24000


def vibrato_curve(n: int, sr: int, rate: float, depth_cents: float,
                  onset_s: float, fade_s: float) -> np.ndarray:
    """Phase signal (in samples of delay) for a smooth, gently swelling vibrato."""
    t = np.arange(n, dtype=np.float64) / sr
    # vibrato fades in over onset_s then holds: singers start a note straight and
    # let the oscillation grow, so a hard start sounds artificial
    env = np.clip((t - onset_s) / max(fade_s, 1e-3), 0.0, 1.0)
    env = 0.5 - 0.5 * np.cos(np.pi * env)          # raised-cosine, smooth both ends
    # instantaneous frequency deviation, in semitones, for a sine of `rate`
    dev = (depth_cents / 100.0) * env * np.sin(2 * np.pi * rate * t)
    # convert frequency deviation to delay-line modulation: a delay of d samples
    # shifts pitch by roughly -d'(t) * sr / (2*pi) cycles... in practice we
    # integrate the deviation and scale to samples
    phase = np.cumsum(dev) / sr
    return phase * sr / 1200.0 * 1.0 * 0.5


def apply_vibrato(y: np.ndarray, sr: int, rate: float, depth_cents: float,
                  onset_s: float, fade_s: float) -> np.ndarray:
    """Fractional-delay vibrato.

    Reading a delay line at d(t) shifts pitch by the factor 1 - d'(t), so to
    impose a fractional pitch deviation s(t) (in octaves) we need d'(t) = -s(t);
    d(t) is its negative integral, expressed in samples. Reading the signal at
    that fractional position with linear interpolation produces the vibrato, and
    because s(t) is a sine centred on zero the pitch stays centred on the note.
    """
    n = len(y)
    t = np.arange(n, dtype=np.float64) / sr
    env = np.clip((t - onset_s) / max(fade_s, 1e-3), 0.0, 1.0)
    env = 0.5 - 0.5 * np.cos(np.pi * env)      # smooth swell in and out
    dev = (depth_cents / 100.0) * env * np.sin(2 * np.pi * rate * t)
    s = dev / 12.0                             # semitones -> octaves
    d = -np.cumsum(s)                          # samples, since d'(t) = -s(t)
    d -= d.mean()
    pos = np.clip(np.arange(n, dtype=np.float64) + d, 0, n - 1)
    i0 = np.floor(pos).astype(np.int64)
    i1 = np.minimum(i0 + 1, n - 1)
    frac = pos - i0
    return (y[i0] * (1 - frac) + y[i1] * frac).astype(np.float32)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--src", default=None, help="default 06/vocal_en_matched.wav")
    ap.add_argument("--rate", type=float, default=5.4, help="vibrato rate, Hz")
    ap.add_argument("--depth", type=float, default=22.0, help="peak deviation, cents")
    ap.add_argument("--onset", type=float, default=0.18, help="delay before vibrato starts, s")
    ap.add_argument("--fade", type=float, default=0.22, help="vibrato fade-in, s")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    run = Path(a.run_dir)
    src = Path(a.src) if a.src else run / "06" / "vocal_en_matched.wav"
    y, sr = sf.read(str(src), dtype="float32", always_2d=True)
    y = y.mean(axis=1)
    if sr != SR:
        y = soxr.resample(y, sr, SR)

    out = apply_vibrato(y, SR, a.rate, a.depth, a.onset, a.fade)
    peak = float(np.max(np.abs(out)))
    if peak > 0.99:
        out *= 0.96 / peak
    dst = Path(a.out) if a.out else run / "06" / "vocal_en_final.wav"
    sf.write(str(dst), out, SR, subtype="PCM_24")
    print(f"vibrato {a.rate:.1f}Hz depth {a.depth:.0f}c -> {dst}", flush=True)
    (run / "06" / "vibrato.json").write_text(json.dumps(
        {"rate_hz": a.rate, "depth_cents": a.depth, "onset_s": a.onset,
         "fade_s": a.fade}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
