"""Measure voice quality with Praat: HNR and jitter.

HNR (harmonics-to-noise ratio) is the right measure for "sounds noisy / buzzy":
it compares periodic energy to everything else in the signal. A clean sung vowel
sits around 15-25 dB; a hoarse or vocoder-y one falls under 10 dB.

Also reports shimmer and CPPS-free local jitter, and the share of frames Praat
considers voiced.
"""
import sys
from pathlib import Path

from _env import ROOT, add_libs

sys.path.insert(0, str(Path(__file__).resolve().parent))
add_libs()

import numpy as np
import parselmouth
from parselmouth.praat import call
from common import SR, load_json, load_mono

run = ROOT / "runs" / "sudi"
en = load_json(run / "05" / "en_lines.json")


def hnr_of(path, label, max_lines=24):
    y = load_mono(path)
    vals, jits, vs = [], [], []
    for ln in en["lines"][:max_lines]:
        t0, slot = float(ln["t0"]), float(ln["slot"])
        seg = y[int(t0 * SR):int((t0 + slot) * SR)]
        if len(seg) < SR * 0.3:
            continue
        seg = np.asarray(seg, dtype=np.float64)
        if np.max(np.abs(seg)) < 1e-6:
            continue
        seg = seg / np.max(np.abs(seg)) * 0.9
        snd = parselmouth.Sound(seg, sampling_frequency=SR)
        try:
            harm = call(snd, "To Harmonicity (cc)", 0.01, 75.0, 0.1, 1.0)
            v = harm.values[0]
            v = v[~np.isnan(v)]
            v = v[v > 0]
            if v.size:
                vals.append(float(np.median(v)))
            pt = call(snd, "To PointProcess (periodic, cc)", 75.0, 600.0)
            j = call(pt, "Get jitter (local)", 0.0, 0.0, 0.0001, 0.02, 1.3)
            if np.isfinite(j):
                jits.append(float(j) * 100)
            vo = snd.to_pitch(0.01, 75.0, 600.0)
            f = vo.selected_array["frequency"]
            vs.append(float((f > 0).mean()))
        except Exception:
            continue
    if not vals:
        print(f"{label:<34} no measurement")
        return
    print(f"{label:<34} HNR {np.median(vals):5.1f} dB   "
          f"jitter {np.median(jits) if jits else 0:5.2f}%   "
          f"voiced {np.median(vs) if vs else 0:.2f}   ({len(vals)} lines)")


print("=== voice quality (Praat) ===")
hnr_of(run / "03" / "vocal.wav", "original singer (isolated vocal)")
hnr_of(run / "06" / "vocal_male.wav", "v3 male (singer contour)")
hnr_of(run / "06" / "vocal_female.wav", "v3 female (singer contour)")
hnr_of(run / "06" / "vocal_female_v1world.wav", "v1 female (old)")
for extra in ("vocal_male_v2psola.wav", "vocal_male_v1world.wav"):
    p = run / "06" / extra
    if p.exists():
        hnr_of(p, extra.replace(".wav", ""))
