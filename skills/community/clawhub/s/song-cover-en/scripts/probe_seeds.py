"""The diffusion starts from fresh `torch.randn`, so every render is a new draw.

`flow_matching.py::reverse_diffusion` initialises `z = torch.randn(...)` and nothing
in the repository ever calls `torch.manual_seed`. Two renders of the *same* input
therefore differ, and my measurement of fp16 vs fp32 came out at corr 0.05 -- not a
precision effect, just two unrelated draws.

That reframes the "hoarse / robotic" complaint: it may be sampling luck rather than a
property of the model. This script renders one fixed span under a range of seeds and
scores each result on the cues that separate a natural voice from a breathy synth:

  * cepstral harmonicity in 1-3 kHz -- a real voice is periodic there; hiss is not
  * share of energy in 300 Hz-3 kHz -- human singing sits there, the model is bass-heavy
  * spectral flatness in 0.8-4 kHz -- noise raises it
  * level jitter -- unstable renders wobble in loudness

Higher harmonicity and mid share, lower flatness and jitter is better.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _env import LIBS, RUNS, SRC, CKPT, CFG

for p in (str(LIBS), str(SRC)):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np
import soundfile as sf
import soxr
import torch
from omegaconf import OmegaConf

from soulxsinger.models.soulxsinger import SoulXSinger
from soulxsinger.utils.data_processor import DataProcessor

RUN = RUNS / "sudi"
PHONESET = SRC / "soulxsinger/utils/phoneme/phone_set.json"
SR = 24000


def build_model(cfg, use_fp16=True):
    m = SoulXSinger(cfg)
    ck = torch.load(str(CKPT), weights_only=False, map_location="cpu")
    m.load_state_dict(ck["state_dict"], strict=True)
    del ck
    if use_fp16:
        m.half()
        m.mel.float()
    m.to("cuda").eval()
    return m


def slice_target(t: dict, max_ms: int = 20000) -> dict:
    """Cut a target segment down to ~20 s so a seed sweep stays affordable."""
    durs = [int(float(x) * 1000) for x in t["duration"].split()]
    acc, cut = 0, len(durs)
    for i, d in enumerate(durs):
        acc += d
        if acc >= max_ms:
            cut = i + 1
            break
    out = {"time": [0, acc]}
    for k in ("phoneme", "note_pitch", "note_type"):
        out[k] = " ".join(t[k].split()[:cut])
    out["duration"] = " ".join(f"{d/1000:.4f}" for d in durs[:cut])
    return out


def harmonicity(y: np.ndarray, lo: float, hi: float) -> float:
    from scipy import signal as sg
    sos = sg.butter(4, [lo / (SR / 2), min(hi, SR / 2 - 100) / (SR / 2)],
                    btype="band", output="sos")
    b = sg.sosfiltfilt(sos, y).astype(np.float32)
    n_fft, hop = 2048, 512
    frames = np.lib.stride_tricks.sliding_window_view(b, n_fft)[::hop]
    rms = np.sqrt((frames ** 2).mean(axis=1))
    keep = frames[rms > np.percentile(rms, 55)]
    if len(keep) < 8:
        return 0.0
    win = np.hanning(n_fft).astype(np.float32)
    spec = np.abs(np.fft.rfft(keep * win, axis=1))
    ceps = np.abs(np.fft.irfft(np.log(spec + 1e-10), axis=1))
    qbin = SR / n_fft
    q_lo, q_hi = int(0.003 * SR / qbin), int(0.015 * SR / qbin)
    peak = ceps[:, q_lo:q_hi].max(axis=1)
    floor = np.median(ceps[:, q_lo:q_hi], axis=1) + 1e-9
    return float(np.median(20 * np.log10(peak / floor + 1e-9)))


def score(y: np.ndarray) -> dict:
    from scipy import signal as sg
    # score a 6 s excerpt: the full 20 s render needs ~30 MB per STFT of complex128
    # and this machine is already close to its RAM ceiling with the model loaded
    y = y[: SR * 6]
    f, p = sg.welch(y, SR, nperseg=2048)
    tot = p.sum() + 1e-20
    low = p[(f >= 80) & (f < 300)].sum() / tot * 100
    lowmid = p[(f >= 300) & (f < 1000)].sum() / tot * 100
    mid = p[(f >= 1000) & (f < 3000)].sum() / tot * 100
    pres = p[(f >= 3000) & (f < 8000)].sum() / tot * 100
    f2, t, S = sg.stft(y, SR, nperseg=512, noverlap=384)
    band = (f2 >= 800) & (f2 < 4000)
    mag = np.abs(S[band]) + 1e-12
    flat = float(np.median(np.exp(np.log(mag).mean(0)) / mag.mean(0)))
    # level jitter across 20 ms frames
    env = np.sqrt(np.convolve(y ** 2, np.ones(480) / 480, "same"))[::480]
    live = env[env > 1e-3]
    jitter = float(np.std(np.diff(20 * np.log10(live + 1e-9)))) if live.size > 4 else 99.0
    harm = harmonicity(y, 1000, 3000)
    a = np.abs(y)
    crest = float(20 * np.log10(a.max() / (np.sqrt((y ** 2).mean()) + 1e-12)))
    # higher is better for harm and mid; lower is better for flat and jitter
    composite = harm * 1.0 + mid * 0.35 + lowmid * 0.05 - flat * 40.0 - jitter * 1.2
    return {"low": low, "lowmid": lowmid, "mid": mid, "pres": pres,
            "flat": flat, "jitter": jitter, "harm": harm, "crest": crest,
            "composite": composite}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", default=str(RUN))
    ap.add_argument("--seeds", default="0,1,2,3,4,5,6,7,8,9,10,11")
    ap.add_argument("--steps", type=int, default=32)
    ap.add_argument("--max-ms", type=int, default=20000)
    ap.add_argument("--fp32", action="store_true")
    a = ap.parse_args()

    run = Path(a.run_dir)
    out = run / "06" / "seed_probe"
    out.mkdir(parents=True, exist_ok=True)
    cfg = OmegaConf.load(CFG)
    model = build_model(cfg, use_fp16=not a.fp32)
    print("model ready", flush=True)

    dp = DataProcessor(hop_size=cfg.audio.hop_size, sample_rate=cfg.audio.sample_rate,
                       phoneset_path=str(PHONESET), device="cuda")
    prompt = json.loads((run / "05" / "prompt.json").read_text(encoding="utf-8"))[0]
    targets = json.loads((run / "05" / "target.json").read_text(encoding="utf-8"))

    p = dict(prompt)
    span = p.pop("_wav_span")
    p.pop("_median_note", None)
    p.pop("_song_median_note", None)
    vocal, vsr = sf.read(str(run / "03" / "vocal.wav"), dtype="float32", always_2d=True)
    vocal = vocal.mean(axis=1)
    seg = soxr.resample(vocal[int(span[0] * vsr):int(span[1] * vsr)], vsr, SR)
    ref = out / "prompt_ref.wav"
    sf.write(str(ref), seg, SR)
    pd = dp.process(json.loads(json.dumps(p)), str(ref))

    tgt = slice_target(targets[0], a.max_ms)
    td = dp.process(json.loads(json.dumps(tgt)))
    print(f"target slice {tgt['time'][1]/1000:.2f}s, n_steps={a.steps}", flush=True)

    rows = []
    for s in [int(x) for x in a.seeds.split(",") if x.strip()]:
        torch.manual_seed(s)
        gen = model.infer({"prompt": pd, "target": td}, auto_shift=False, pitch_shift=0,
                          n_steps=a.steps, cfg=cfg.infer.cfg, control="score",
                          use_fp16=not a.fp32)
        y = gen.squeeze().float().cpu().numpy()
        pk = float(np.max(np.abs(y)))
        if pk > 0:
            y = y / pk * 0.9
        sf.write(str(out / f"seed{s:02d}.wav"), y, SR)
        sc = score(y)
        sc["seed"] = s
        rows.append(sc)
        print(f"  seed {s:2d} harm {sc['harm']:5.1f} mid {sc['mid']:5.1f}% "
              f"flat {sc['flat']:.3f} jitter {sc['jitter']:5.2f} "
              f"-> {sc['composite']:7.2f}", flush=True)

    rows.sort(key=lambda r: -r["composite"])
    print("\nranked:", flush=True)
    for i, r in enumerate(rows, 1):
        print(f"  {i:2d}. seed {r['seed']:2d}  composite {r['composite']:7.2f} "
              f"harm {r['harm']:5.1f} mid {r['mid']:5.1f}", flush=True)
    # numpy scalars are not JSON serialisable; coerce every metric to a plain float
    clean = [{k: (int(v) if isinstance(v, (int, np.integer)) else float(v))
              for k, v in r.items()} for r in rows]
    (out / "seed_scores.json").write_text(json.dumps(clean, indent=1), encoding="utf-8")
    print(f"\nbest seed: {rows[0]['seed']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
