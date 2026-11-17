import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import load_mono, load_json, SR

import librosa
import numpy as np

run = Path(sys.argv[1])
v = load_mono(run / "03" / "vocal.wav")
f0, _, _ = librosa.pyin(v, fmin=110, fmax=900, sr=SR, frame_length=2048,
                        hop_length=256, fill_na=0.0)
t = librosa.times_like(f0, sr=SR, hop_length=256)
mid = np.where(f0 > 0, 69 + 12 * np.log2(np.maximum(f0, 1e-6) / 440.0), np.nan)
ly = load_json(run / "01_lyrics.json")
inl = np.zeros(len(t), bool)
for ln in ly["lines"]:
    inl |= (t >= ln["t"]) & (t < ln["t"] + ln["slot"])
lo = (mid > 44) & (mid < 49)
print("frames 44-49 semitones:", int(lo.sum()))
print("  inside lyric windows:", int((lo & inl).sum()),
      " outside:", int((lo & ~inl).sum()))
print("total frames:", len(t), " in-line:", int(inl.sum()))
runs, c = [], 0
for x in lo:
    if x:
        c += 1
    elif c:
        runs.append(c)
        c = 0
if c:
    runs.append(c)
print("low-band runs:", len(runs), "max", max(runs), "median", np.median(runs))
rh, ch = [], 0
for x in ~lo:
    if x:
        ch += 1
    elif ch:
        rh.append(ch)
        ch = 0
print("gaps between low runs: median", np.median(rh) if rh else 0, "max", max(rh) if rh else 0)
