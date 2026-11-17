"""Mix the synthesized English vocal with the original instrumental.

The vocal is rendered against the same timeline as the backing track, so a plain
sample-aligned sum is correct -- no shifting needed. We only balance levels and
normalize, because the model's output level depends on how much silence the
segment happened to contain.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _env import LIBS

sys.path.insert(0, str(LIBS))


import numpy as np
import soundfile as sf
import soxr

SR = 44100


def load(path: Path, sr: int = SR) -> np.ndarray:
    y, got = sf.read(str(path), dtype="float32", always_2d=True)
    y = y.mean(axis=1)
    if got != sr:
        y = soxr.resample(y, got, sr)
    return y.astype(np.float32)


def active_rms(y: np.ndarray) -> float:
    # ignore digital silence: the vocal track is mostly rests before the first line
    live = y[np.abs(y) > 1e-4]
    return float(np.sqrt(np.mean(live ** 2))) if live.size else 0.0


def limit(y: np.ndarray, sr: int, ceiling: float = 0.85,
          attack_s: float = 0.004, release_s: float = 0.15) -> np.ndarray:
    """Peak-hold limiter.

    The vocal arrives with a crest factor near 22 dB: the spectral match lifted a
    narrow band and left tall transients. Scaling the whole mix down to clear those
    transients would bury the voice under the backing, so we tame just the vocal.
    A forward peak-hold finds every overshoot; a slow minimum-filtered release
    keeps the gain down long enough to avoid chattering; neither step bends the
    waveform, so -- unlike tanh soft clipping -- nothing gets distorted.
    """
    from scipy import ndimage

    win_a = max(3, int(attack_s * sr) | 1)
    held = ndimage.maximum_filter1d(np.abs(y), size=win_a, mode="nearest")
    need = np.minimum(1.0, ceiling / np.maximum(held, 1e-9))
    # hold the reduction across the release window so gain never pops back up
    win_r = max(3, int(release_s * sr) | 1)
    need = ndimage.minimum_filter1d(need, size=win_r, mode="nearest")
    # then smooth the edges of the gain curve
    need = ndimage.uniform_filter1d(need, size=win_a, mode="nearest")
    # smoothing can raise the curve slightly; clamp again against the raw peaks
    need = np.minimum(need, np.minimum(1.0, ceiling / np.maximum(held, 1e-9)))
    return (y * need).astype(np.float32)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--vocal", default=None, help="defaults to 06/vocal_en.wav")
    ap.add_argument("--inst", default=None, help="defaults to 02/inst.wav")
    ap.add_argument("--vocal-over", type=float, default=1.35,
                    help="lead level above the backing, in linear gain")
    ap.add_argument("--ceiling", type=float, default=0.85,
                    help="limiter ceiling applied to the vocal before summing")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    run = Path(a.run_dir)
    voc = load(Path(a.vocal) if a.vocal else run / "06" / "vocal_en.wav")
    inst = load(Path(a.inst) if a.inst else run / "02" / "inst.wav")

    n = max(voc.size, inst.size)
    voc = np.pad(voc, (0, n - voc.size))
    inst = np.pad(inst, (0, n - inst.size))

    rv, ri = active_rms(voc), active_rms(inst)
    gain = (ri / max(rv, 1e-6)) * a.vocal_over
    print(f"vocal rms {rv:.4f}  inst rms {ri:.4f}  -> vocal gain {gain:.2f}", flush=True)

    voc = voc * gain
    # tame the vocal's transient overshoot before summing so the backing does not
    # have to be turned down to make room for it
    voc = limit(voc, SR, ceiling=a.ceiling)
    mix = voc + inst
    peak = float(np.max(np.abs(mix)))
    if peak > 0.95:
        mix *= 0.95 / peak
        print(f"normalized: peak {peak:.3f} -> {float(np.max(np.abs(mix))):.3f}", flush=True)

    out = Path(a.out) if a.out else run / "06" / "mix.wav"
    sf.write(str(out), mix, SR, subtype="PCM_24")
    print(f"wrote {out} ({mix.size / SR:.2f}s, rms {active_rms(mix):.4f})", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
