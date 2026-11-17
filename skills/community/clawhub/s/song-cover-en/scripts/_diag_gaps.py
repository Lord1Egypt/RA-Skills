"""Is the v3 vocal gappy? Look at the level contour inside each line."""
import sys
from pathlib import Path

from _env import ROOT, add_libs

sys.path.insert(0, str(Path(__file__).resolve().parent))
add_libs()

import numpy as np
import librosa
from common import SR, load_json, load_mono

run = ROOT / "runs" / "sudi"
en = load_json(run / "05" / "en_lines.json")

for name in ("vocal_male.wav", "vocal_female.wav", "vocal_female_v1world.wav"):
    p = run / "06" / name
    if not p.exists():
        continue
    y = load_mono(p)
    hop = 256
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=hop)[0]
    db = 20 * np.log10(rms + 1e-9)
    # only inside lyric slots
    fps = SR / hop
    ins = []
    for ln in en["lines"]:
        a, b = int(float(ln["t0"]) * fps), int((float(ln["t0"]) + float(ln["slot"])) * fps)
        ins.append(db[a:b])
    ins = np.concatenate([x for x in ins if x.size])
    print(f"{name:<28} inside-slot dB: p10 {np.percentile(ins,10):6.1f} "
          f"p50 {np.percentile(ins,50):6.1f} p90 {np.percentile(ins,90):6.1f}   "
          f"<-40dB {np.mean(ins < -40):.2f}   <-30dB {np.mean(ins < -30):.2f}")

# same for original vocal
y = load_mono(run / "03" / "vocal.wav")
hop = 256
rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=hop)[0]
db = 20 * np.log10(rms + 1e-9)
fps = SR / hop
ins = []
for ln in en["lines"]:
    a, b = int(float(ln["t0"]) * fps), int((float(ln["t0"]) + float(ln["slot"])) * fps)
    ins.append(db[a:b])
ins = np.concatenate([x for x in ins if x.size])
print(f"{'original vocal':<28} inside-slot dB: p10 {np.percentile(ins,10):6.1f} "
      f"p50 {np.percentile(ins,50):6.1f} p90 {np.percentile(ins,90):6.1f}   "
      f"<-40dB {np.mean(ins < -40):.2f}   <-30dB {np.mean(ins < -30):.2f}")
