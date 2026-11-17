"""Restore the intelligibility band of the synthesized vocal with a matching EQ.

The singer model is intrinsically darker than a human. Measured on its own
official example, singing the very same notes as the supplied human acapella:

    band         human    model
    80-300 Hz     1.4%     7.8%
    300-1k Hz    64.0%    84.4%
    1-3 kHz      30.5%     3.9%
    3-8 kHz       3.3%     3.1%

Everything that makes a word intelligible -- consonant bursts and the second and
third formants of vowels -- lives in 1-3 kHz, and the model puts 8x less energy
there than a human does. That deficit is what a listener hears as mumbling, and
the excess at 80-300 Hz is what makes it sound like a synthetic instrument rather
than a throat.

This is the same correction a mix engineer applies to a dull vocal: a low shelf to
remove the boom, a presence lift where the consonants sit, and a touch of air.
Gains are derived from the measured deficit and then verified by re-measuring.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _env import LIBS

sys.path.insert(0, str(LIBS))


import numpy as np
import soundfile as sf
import soxr
from scipy import signal as sg

SR = 44100


def shelves(y: np.ndarray, sr: int, low_db: float, pres_db: float, air_db: float,
            low_hz: float = 220.0, pres_hz: float = 2200.0, air_hz: float = 7000.0,
            pres_q: float = 0.7) -> np.ndarray:
    out = y.astype(np.float64)

    def apply(x, sos):
        return sg.sosfilt(sos, x)

    if abs(low_db) > 0.01:
        sos = sg.butter(2, low_hz / (sr / 2), btype="low", output="sos")
        out = out + (10 ** (low_db / 20) - 1.0) * apply(out, sos)
    if abs(pres_db) > 0.01:
        # a peaking bell sits better on a voice than a shelf: it lifts the
        # consonant region without brightening the whole top end
        b, a = sg.iirpeak(pres_hz / (sr / 2), pres_q)
        out = out + (10 ** (pres_db / 20) - 1.0) * sg.lfilter(b, a, out)
    if abs(air_db) > 0.01:
        sos = sg.butter(2, air_hz / (sr / 2), btype="high", output="sos")
        out = out + (10 ** (air_db / 20) - 1.0) * apply(out, sos)
    return out.astype(np.float32)


def band_share(y: np.ndarray, sr: int) -> dict[str, float]:
    f, p = sg.welch(y, sr, nperseg=4096)
    tot = float(p.sum()) + 1e-20
    bands = {"low": (80, 300), "lowmid": (300, 1000), "mid": (1000, 3000),
             "presence": (3000, 8000), "air": (8000, 12000)}
    return {k: float(p[(f >= lo) & (f < hi)].sum() / tot * 100)
            for k, (lo, hi) in bands.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--src", default=None, help="default 06/vocal_en.wav")
    ap.add_argument("--low", type=float, default=-5.0, help="low shelf gain, dB")
    ap.add_argument("--presence", type=float, default=8.0, help="presence bell gain, dB")
    ap.add_argument("--air", type=float, default=2.5, help="air shelf gain, dB")
    ap.add_argument("--presence-hz", type=float, default=2200.0)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    run = Path(a.run_dir)
    src = Path(a.src) if a.src else run / "06" / "vocal_en.wav"
    y, sr = sf.read(str(src), dtype="float32", always_2d=True)
    y = y.mean(axis=1)
    if sr != SR:
        y = soxr.resample(y, sr, SR)

    before = band_share(y, SR)
    print(f"before: " + "  ".join(f"{k}={v:.1f}%" for k, v in before.items()), flush=True)

    fixed = shelves(y, SR, a.low, a.presence, a.air, pres_hz=a.presence_hz)
    after = band_share(fixed, SR)
    print(f"after:  " + "  ".join(f"{k}={v:.1f}%" for k, v in after.items()), flush=True)

    peak = float(np.max(np.abs(fixed)))
    if peak > 0.99:
        fixed *= 0.96 / peak
    out = Path(a.out) if a.out else run / "06" / "vocal_en_eq.wav"
    sf.write(str(out), fixed, SR, subtype="PCM_24")
    print(f"wrote {out} (peak {float(np.max(np.abs(fixed))):.3f})", flush=True)
    (run / "06" / "post_eq.json").write_text(json.dumps(
        {"low_db": a.low, "presence_db": a.presence, "air_db": a.air,
         "presence_hz": a.presence_hz, "before": before, "after": after}, indent=1),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
