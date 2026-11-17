"""Match the synthesized vocal's long-term spectrum to a human recording.

The singer model is intrinsically darker than a human throat: measured on its own
official example, singing the *same notes* as the supplied human acapella, the
model puts 3.9% of its energy in 1-3 kHz where the human puts 30.5%, and 84.4% in
300-1000 Hz where the human puts 64.0%. Consonant bursts and the upper formants --
everything that makes a word intelligible -- live in that missing band, so the
singer sounds like it is mumbling through a synth patch.

A fixed EQ guess cannot fix a deficit that large without either leaving it half
solved or sounding harsh. Instead we measure: take the long-term average spectrum
(LTAS) of both signals, smooth them on a log-frequency axis, and apply the
smoothed ratio as a zero-phase gain curve. This is the same idea as matching a
vocal to a reference during mastering, applied numerically instead of by ear.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _env import LIBS, REF_HUMAN

sys.path.insert(0, str(LIBS))


import numpy as np
import soundfile as sf
import soxr

SR = 24000
N_FFT = 2048
HOP = 512


def ltas(y: np.ndarray, sr: int, n_fft: int = N_FFT, hop: int = HOP):
    """Long-term average spectrum, computed only over voiced frames."""
    win = np.hanning(n_fft).astype(np.float32)
    n = 1 + (len(y) - n_fft) // hop
    if n < 2:
        return np.ones(n_fft // 2 + 1), np.fft.rfftfreq(n_fft, 1 / sr)
    idx = np.arange(n) * hop
    frames = np.lib.stride_tricks.sliding_window_view(y, n_fft)[idx] * win
    rms = np.sqrt((frames ** 2).mean(axis=1))
    keep = rms > max(0.01, np.percentile(rms, 40))
    if keep.sum() < 4:
        keep = rms > 0.005
    spec = np.abs(np.fft.rfft(frames[keep], axis=1)).mean(axis=0)
    return spec, np.fft.rfftfreq(n_fft, 1 / sr)


def smooth_log(freqs: np.ndarray, curve: np.ndarray, points: int = 96) -> np.ndarray:
    """Smooth a spectrum on a log-frequency axis so it becomes a usable EQ curve."""
    eps = 1e-12
    logf = np.log(np.maximum(freqs, 20.0))
    grid = np.linspace(logf.min(), logf.max(), points)
    vals = np.interp(grid, logf, np.log(np.maximum(curve, eps)))
    k = max(3, points // 12) | 1
    pad = k // 2
    vp = np.pad(vals, pad, mode="edge")
    sm = np.array([np.median(vp[i:i + k]) for i in range(points)])
    # back to the original frequency grid
    return np.exp(np.interp(logf, grid, sm))


def apply_curve(y: np.ndarray, freqs: np.ndarray, gain_db: np.ndarray,
                n_fft: int = N_FFT, hop: int = HOP) -> np.ndarray:
    """Zero-phase overlap-add filtering with the gain curve applied per bin."""
    win = np.hanning(n_fft).astype(np.float32)
    g = (10 ** (gain_db / 20.0)).astype(np.float32)
    pad = n_fft
    yp = np.pad(y, (pad, pad)).astype(np.float32)
    out = np.zeros_like(yp)
    wsum = np.zeros_like(yp)
    for s in range(0, len(yp) - n_fft, hop):
        fr = yp[s:s + n_fft] * win
        spec = np.fft.rfft(fr) * g
        rec = np.fft.irfft(spec, n=n_fft).astype(np.float32) * win
        out[s:s + n_fft] += rec
        wsum[s:s + n_fft] += win ** 2
    good = wsum > 1e-6
    out[good] /= wsum[good]
    return out[pad:pad + len(y)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--src", default=None, help="default 06/vocal_en.wav")
    ap.add_argument("--ref", default=str(REF_HUMAN))
    ap.add_argument("--max-boost", type=float, default=14.0, help="cap on any bin boost, dB")
    ap.add_argument("--max-cut", type=float, default=9.0, help="cap on any bin cut, dB")
    ap.add_argument("--strength", type=float, default=1.0)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    run = Path(a.run_dir)
    src = Path(a.src) if a.src else run / "06" / "vocal_en.wav"
    y, sr = sf.read(str(src), dtype="float32", always_2d=True)
    y = y.mean(axis=1)
    if sr != SR:
        y = soxr.resample(y, sr, SR)

    r, rsr = sf.read(a.ref, dtype="float32", always_2d=True)
    r = r.mean(axis=1)
    if rsr != SR:
        r = soxr.resample(r, rsr, SR)

    s_src, freqs = ltas(y, SR)
    s_ref, _ = ltas(r, SR)
    src_s = smooth_log(freqs, s_src)
    ref_s = smooth_log(freqs, s_ref)

    ratio_db = 20.0 * np.log10(np.maximum(ref_s, 1e-12) / np.maximum(src_s, 1e-12))
    ratio_db = np.clip(ratio_db * a.strength, -a.max_cut, a.max_boost)
    # never touch the extreme bottom: nothing musical is down there, and boosting
    # it would only add rumble
    ratio_db[freqs < 90] = np.minimum(ratio_db[freqs < 90], 0.0)

    out = apply_curve(y, freqs, ratio_db)
    peak = float(np.max(np.abs(out)))
    if peak > 0.99:
        out *= 0.96 / peak

    dst = Path(a.out) if a.out else run / "06" / "vocal_en_matched.wav"
    sf.write(str(dst), out, SR, subtype="PCM_24")

    def share(x):
        spec, fr = ltas(x, SR)
        tot = spec.sum() + 1e-20
        return {k: float(spec[(fr >= lo) & (fr < hi)].sum() / tot * 100)
                for k, (lo, hi) in {"low": (80, 300), "lowmid": (300, 1000),
                                    "mid": (1000, 3000), "presence": (3000, 8000),
                                    "air": (8000, 12000)}.items()}

    print("before: " + "  ".join(f"{k}={v:.1f}%" for k, v in share(y).items()), flush=True)
    print("after : " + "  ".join(f"{k}={v:.1f}%" for k, v in share(out).items()), flush=True)
    print("human : " + "  ".join(f"{k}={v:.1f}%" for k, v in share(r).items()), flush=True)
    print(f"wrote {dst}", flush=True)
    (run / "06" / "spectral_match.json").write_text(json.dumps(
        {"ref": str(a.ref), "strength": a.strength,
         "curve_db": [round(float(v), 2) for v in ratio_db[:: max(1, len(ratio_db) // 40)]]},
        indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
