"""QA: compare v1 (WORLD+grid), v2 (PSOLA), v3 (WORLD+singer contour).

Metrics per line, on the rendered vocal:
  pitch_err   median |sung midi - target note midi| in semitones
  jerk        mean |d2 log2 f0| - how much the pitch actually moves (robot proxy)
  hf          share of energy above 5 kHz - the "noisy / electric" proxy
  voiced      fraction of frames with pitch - how much tone survives
The original singer's own figures are printed as the reference.
"""
import sys
from pathlib import Path

from _env import ROOT, add_libs

sys.path.insert(0, str(Path(__file__).resolve().parent))
add_libs()

import numpy as np
import librosa
from common import SR, load_json, load_mono

run = ROOT / "runs" / "sudi"
HOP = 256
FPSF = SR / HOP


def stats(y):
    f0, _, _ = librosa.pyin(y, fmin=60, fmax=900, sr=SR, frame_length=1024,
                            hop_length=HOP, fill_na=0.0)
    v = f0 > 0
    if v.sum() < 5:
        return None
    lf = np.log2(np.maximum(f0[v], 1e-9))
    jerk = float(np.mean(np.abs(np.diff(lf, 2)))) if len(lf) > 3 else 0.0
    ny = y / (np.max(np.abs(y)) + 1e-9)
    S = np.abs(librosa.stft(ny, n_fft=1024, hop_length=256)) ** 2
    fr = librosa.fft_frequencies(sr=SR, n_fft=1024)
    hf = float(S[fr >= 5000].sum() / (S.sum() + 1e-12))
    return {"f0": f0, "jerk": jerk, "hf": hf, "voiced": float(v.mean())}


def eval_vocal(path, kind, oct_shift=0):
    if not Path(path).exists():
        print(f"{kind:<32} missing")
        return
    y = load_mono(path)
    en = load_json(run / "05" / "en_lines.json")
    res = []
    for ln in en["lines"]:
        t0, slot = float(ln["t0"]), float(ln["slot"])
        seg = y[int(t0 * SR):int((t0 + slot) * SR)]
        if len(seg) < SR * 0.2:
            continue
        if len(seg) < SR * 0.25:
            continue
        st = stats(seg)
        if st is None:
            continue
        errs = []
        for n in ln["notes"]:
            a = max(0.0, float(n["t0"]) - t0)
            b = min(slot, float(n["t1"]) - t0)
            f = st["f0"][int(a * FPSF):int(b * FPSF)]
            f = f[f > 0]
            if f.size < 3:
                continue
            midi = 69 + 12 * np.log2(np.median(f) / 440.0)
            errs.append(abs(midi - (float(n["midi"]) + oct_shift)))
        if errs:
            res.append({"pitch_err": float(np.median(errs)), "jerk": st["jerk"],
                        "hf": st["hf"], "voiced": st["voiced"]})
    if not res:
        print(f"{kind:<32} no measurable lines")
        return
    print(f"{kind:<32} pitch {np.median([r['pitch_err'] for r in res]):5.2f} st"
          f"   jerk {np.median([r['jerk'] for r in res]):.4f}"
          f"   hf {np.median([r['hf'] for r in res]):.4f}"
          f"   voiced {np.median([r['voiced'] for r in res]):.2f}"
          f"   ({len(res)} lines)")


print("=== reference ===")
voc = load_mono(run / "03" / "vocal.wav")
en = load_json(run / "05" / "en_lines.json")
js, hfs, vs = [], [], []
for ln in en["lines"][:24]:
    t0, slot = float(ln["t0"]), float(ln["slot"])
    st = stats(voc[int(t0 * SR):int((t0 + slot) * SR)])
    if st:
        js.append(st["jerk"])
        hfs.append(st["hf"])
        vs.append(st["voiced"])
print(f"{'original singer':<32} jerk {np.median(js):.4f}   hf {np.median(hfs):.4f}"
      f"   voiced {np.median(vs):.2f}")

print("\n=== covers ===")
for name, label in [("vocal_male.wav", "v3 male (singer contour)"),
                    ("vocal_female.wav", "v3 female (singer contour)"),
                    ("vocal_female_v1world.wav", "v1 female (old WORLD grid)")]:
    eval_vocal(run / "06" / name, label)
