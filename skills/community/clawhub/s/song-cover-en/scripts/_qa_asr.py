"""QA with ASR: is the English still intelligible after the PSOLA rewrite?"""
import os
import sys
from pathlib import Path

from _env import ROOT, add_libs

sys.path.insert(0, str(Path(__file__).resolve().parent))
add_libs()

import numpy as np
import librosa
from faster_whisper import WhisperModel
from common import SR, load_json, load_mono, save_wav

run = ROOT / "runs" / "sudi"
en = load_json(run / "05" / "en_lines.json")

model = WhisperModel(os.environ.get("SONG_COVER_ASR_MODEL",
                              str(ROOT / ".asr" / "models" / "fw-small")),
                     device="cpu", compute_type="int8")


def transcribe(y):
    y16 = librosa.resample(y, orig_sr=SR, target_sr=16000)
    segs, _ = model.transcribe(y16.astype(np.float32), language="en",
                               beam_size=5, vad_filter=False)
    return " ".join(s.text.strip() for s in segs)


for name in ("vocal_male", "vocal_female"):
    p = run / "06" / f"{name}.wav"
    if not p.exists():
        print(f"{name}: missing")
        continue
    y = load_mono(p)
    print(f"\n=== {name} ===")
    hit = tot = 0
    for ln in en["lines"][:12]:
        t0, slot = float(ln["t0"]), float(ln["slot"])
        seg = y[int(t0 * SR):int((t0 + slot) * SR)]
        if len(seg) < SR * 0.3:
            continue
        seg = seg / max(1e-9, float(np.max(np.abs(seg)))) * 0.9
        got = transcribe(seg).lower().strip()
        want = ln["en"].lower().strip()
        # rough word recall
        w = [x for x in want.replace(",", "").replace("?", "").split() if len(x) > 2]
        h = sum(1 for x in w if x in got)
        tot += len(w)
        hit += h
        print(f"[{ln['i']:2d}] want {want}")
        print(f"     got  {got}")
    print(f"word recall {hit}/{tot} = {hit/max(1,tot):.0%}")
