"""Vocal separation with UVR MDX-Net at the model's native 44.1 kHz.

The original skill ran this at 22.05 kHz, which is not a cosmetic difference:
MDX-Net takes N_FFT=6144 and 3072 frequency bins, i.e. a 7.17 Hz bin spacing that
only means anything at 44100 Hz. Feeding it 22050 Hz squeezes the content into
the lower half of its expected spectrum, so every vowel harmonic the model was
trained to keep presents as instrumental and is masked away. The separated vocal
then sounds band-limited to a few hundred Hz, and any singer cloned from it
inherits that muffled, electronic timbre.

We also lift the sample rate of the *instrumental* to 44.1 kHz so the two stems
of the mix stay sample-aligned with each other.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from _env import LIBS, UVR_MODEL

sys.path.insert(0, str(LIBS))


import numpy as np
import soundfile as sf

N_FFT, HOP, DIM_F, DIM_T = 6144, 1024, 3072, 256
SR = 44100


def load(path: Path, sr: int = SR) -> np.ndarray:
    import soxr
    y, got = sf.read(str(path), dtype="float32", always_2d=True)
    y = y.mean(axis=1)
    if got != sr:
        y = soxr.resample(y, got, sr)
    return np.ascontiguousarray(y.astype(np.float32))


def separate(model_path: Path, y: np.ndarray) -> np.ndarray:
    import librosa
    import onnxruntime as ort

    so = ort.SessionOptions()
    so.intra_op_num_threads = 8
    sess = ort.InferenceSession(str(model_path), sess_options=so,
                                providers=["CPUExecutionProvider"])
    nch = sess.get_inputs()[0].shape[1]
    ch = max(1, nch // 2)
    # librosa.stft keeps centre=False padding by default here, matching the
    # reference implementation's framing
    stft = librosa.stft(y, n_fft=N_FFT, hop_length=HOP)[:DIM_F]
    nfr = stft.shape[1]

    voc = np.zeros_like(stft, dtype=np.complex64)
    win = DIM_T
    for s in range(0, nfr, win):
        e = min(s + win, nfr)
        w = e - s
        inp = np.zeros((1, nch, DIM_F, win), dtype=np.float32)
        for c in range(ch):
            inp[0, c * 2 + 0, :, :w] = stft[:, s:e].real
            inp[0, c * 2 + 1, :, :w] = stft[:, s:e].imag
        y_out = sess.run(None, {sess.get_inputs()[0].name: inp})[0]
        for c in range(ch):
            mr = y_out[0, c * 2 + 0, :, :w]
            mi = y_out[0, c * 2 + 1, :, :w]
            a = stft[:, s:e].real
            b = stft[:, s:e].imag
            # the network predicts a complex ratio mask, so the vocal is the
            # product of the mask with the mix, not the raw network output
            voc[:, s:s + w] = (a * mr - b * mi) + 1j * (a * mi + b * mr)

    return librosa.istft(voc, hop_length=HOP, n_fft=N_FFT, length=len(y))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--src", default=None)
    ap.add_argument("--model", default=str(UVR_MODEL))
    a = ap.parse_args()

    run = Path(a.run_dir)
    out = run / "03"
    out.mkdir(parents=True, exist_ok=True)
    src = Path(a.src) if a.src else run / "02" / "orig.wav"

    y = load(src)
    print(f"src {src.name}: {len(y)/SR:.2f}s @ {SR}Hz", flush=True)
    t0 = time.time()
    voc = separate(Path(a.model), y)
    el = time.time() - t0
    # the network returns an unscaled mask product; bring the stem back to the
    # mix's own RMS so it neither clips nor needs guessing downstream
    rv = float(np.sqrt(np.mean(voc ** 2)))
    rm = float(np.sqrt(np.mean(y ** 2)))
    gain = (rm / rv) if rv > 1e-9 else 0.0
    voc = voc * min(gain, 6.0)
    resid = y[:len(voc)] - voc[:len(y)]

    sf.write(str(out / "vocal.wav"), voc, SR, subtype="PCM_24")
    sf.write(str(out / "resid.wav"), resid, SR, subtype="PCM_24")
    import json
    (out / "separate.json").write_text(json.dumps(
        {"src": str(src), "model": Path(a.model).name, "sr": SR,
         "n_fft": N_FFT, "hop": HOP, "dim_f": DIM_F, "dim_t": DIM_T,
         "gain": round(gain, 4),
         "rms_in": round(rm, 5),
         "rms_vocal": round(float(np.sqrt(np.mean(voc ** 2))), 5),
         "rms_resid": round(float(np.sqrt(np.mean(resid ** 2))), 5),
         "seconds": round(el, 1),
         "rtf": round(el / (len(y) / SR), 3)}, indent=1), encoding="utf-8")
    print(f"vocal rms {float(np.sqrt(np.mean(voc**2))):.4f} (gain {gain:.2f}), "
          f"{el:.0f}s (rtf {el/(len(y)/SR):.2f})", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
