"""Probe: is the model's 1-3 kHz content harmonic, or is it noise that our EQ amplifies?

The spectral match lifts 1-3 kHz by up to 18 dB to restore intelligibility. That is
only legitimate if the energy there is harmonic (formants). If it is breath noise,
the same boost turns hiss into a rasp -- which is exactly what "嘶哑沙哑" describes.

Harmonic-to-noise in a band is measured by taking the cepstrum: a strong peak at the
fundamental's quefrency means the band is periodic (a voice); a flat cepstrum means
it is noise.
"""
from __future__ import annotations

from _env import LIBS, RUNS, REF_HUMAN

sys.path.insert(0, str(LIBS))

import sys


import numpy as np
import soundfile as sf
import soxr
from scipy import signal as sg

SR = 24000
BANDS = {"500-1k": (500, 1000), "1-2k": (1000, 2000), "2-3k": (2000, 3000),
         "3-5k": (3000, 5000)}


def load(p: str) -> np.ndarray:
    y, sr = sf.read(p, dtype="float32", always_2d=True)
    y = y.mean(axis=1)
    if sr != SR:
        y = soxr.resample(y, sr, SR)
    return y


def harmonicity(y: np.ndarray, lo: float, hi: float) -> tuple[float, float, float]:
    """Return (harmonic share dB, flatness, energy share %) for band lo..hi."""
    sos = sg.butter(4, [lo / (SR / 2), min(hi, SR / 2 - 100) / (SR / 2)],
                    btype="band", output="sos")
    b = sg.sosfiltfilt(sos, y).astype(np.float32)
    # frame-wise cepstrum
    n_fft, hop = 2048, 512
    frames = np.lib.stride_tricks.sliding_window_view(b, n_fft)[::hop]
    rms = np.sqrt((frames ** 2).mean(axis=1))
    keep = frames[rms > np.percentile(rms, 55)]
    if len(keep) < 8:
        return 0.0, 0.0, 0.0
    win = np.hanning(n_fft).astype(np.float32)
    spec = np.abs(np.fft.rfft(keep * win, axis=1))
    logmag = np.log(spec + 1e-10)
    ceps = np.abs(np.fft.irfft(logmag, axis=1))
    # pitch period for a singing voice is 3..15 ms -> quefrency bins at 24000/2048
    qbin = SR / n_fft
    q_lo, q_hi = int(0.003 * SR / qbin), int(0.015 * SR / qbin)
    peak = ceps[:, q_lo:q_hi].max(axis=1)
    floor = np.median(ceps[:, q_lo:q_hi], axis=1) + 1e-9
    harm = float(np.median(20 * np.log10(peak / floor + 1e-9)))
    mag = spec + 1e-12
    flat = float(np.median(np.exp(np.log(mag).mean(1)) / mag.mean(1)))
    # energy share of this band in the whole signal
    f, p = sg.welch(y, SR, nperseg=4096)
    share = float(p[(f >= lo) & (f < hi)].sum() / (p.sum() + 1e-20) * 100)
    return harm, flat, share


def main() -> int:
    files = [
        (str(RUNS / "sudi" / "06" / "vocal_en.wav"), "raw model"),
        (str(RUNS / "sudi" / "06" / "vocal_en_matched.wav"), "spectral match"),
        (str(RUNS / "sudi" / "03" / "vocal.wav"), "CN original"),
        (str(REF_HUMAN), "human EN"),
    ]
    for path, label in files:
        y = load(path)
        print(f"\n{label}  ({len(y)/SR:.1f}s)", flush=True)
        for name, (lo, hi) in BANDS.items():
            h, fl, sh = harmonicity(y, lo, hi)
            print(f"   {name:8s} harmonic {h:5.1f} dB   flatness {fl:.3f}   share {sh:5.2f}%",
                  flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
