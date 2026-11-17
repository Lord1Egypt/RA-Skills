"""Compare the two control modes on the same 20 s of our English lyric.

`control="score"` feeds the model quantised note pitches (one integer per note). That
throws away everything a singer does *between* the notes: the vibrato on a held vowel,
the slide when moving between two pitches, the micro-drift that keeps a long note
alive. What comes back is a correct but stiff pitch ladder -- the "machine" quality.

`control="melody"` instead feeds a continuous f0 curve sampled every 20 ms. If we
give it the *original singer's own* f0 track, the model inherits the real vibrato and
glides verbatim, and the tune is guaranteed to match the original because it is
literally the original's pitch. Only the words change.

This script renders the same lyric span both ways so they can be compared by ear and
by the same pitch/vibrato metrics we have been using.
"""
from __future__ import annotations

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
SR_OUT = 24000


def build_model(cfg, use_fp16=True):
    model = SoulXSinger(cfg)
    ck = torch.load(str(CKPT), weights_only=False, map_location="cpu")
    model.load_state_dict(ck["state_dict"], strict=True)
    del ck
    if use_fp16:
        model.half()
        model.mel.float()
    model.to("cuda").eval()
    return model


def load_f0_curve() -> tuple[np.ndarray, np.ndarray]:
    """Read 04/f0.csv (10 ms frames, MIDI or NaN) and return (times_s, midi)."""
    rows = (RUN / "04" / "f0.csv").read_text(encoding="utf-8").strip().splitlines()[1:]
    t, m = [], []
    for r in rows:
        a, b = r.split(",")
        t.append(float(a))
        m.append(float(b))
    return np.array(t), np.array(m)


def f0_for_span(times: np.ndarray, midi: np.ndarray, t0: float, t1: float,
                n_frames: int) -> np.ndarray:
    """Sample the singer's pitch track at the model's 50 fps frame grid, in Hz.

    The model's mel2note grid is 20 ms; our track is 10 ms, so we average the two
    frames that fall inside each model frame. NaN (unvoiced) becomes 0.0, which is
    the model's own convention for silence.
    """
    out = np.zeros(n_frames, dtype=np.float32)
    for i in range(n_frames):
        a = t0 + i * 0.02
        b = a + 0.02
        lo = np.searchsorted(times, a, side="left")
        hi = np.searchsorted(times, b, side="left")
        seg = midi[lo:hi] if hi > lo else midi[max(0, lo - 1):lo + 1]
        seg = seg[np.isfinite(seg)]
        if seg.size:
            out[i] = float(10.0 * 2 ** ((np.median(seg) - 69.0) / 12.0))
    return out


def main() -> int:
    cfg = OmegaConf.load(CFG)
    model = build_model(cfg)
    print("model ready", flush=True)
    dp = DataProcessor(hop_size=cfg.audio.hop_size, sample_rate=cfg.audio.sample_rate,
                       phoneset_path=str(PHONESET), device="cuda")

    prompt = json.loads((RUN / "05" / "prompt.json").read_text(encoding="utf-8"))[0]
    targets = json.loads((RUN / "05" / "target.json").read_text(encoding="utf-8"))
    # use the first ~20 s of the song as the test bed
    tgt = targets[0]
    times, midi = load_f0_curve()

    # prompt audio
    vocal, vsr = sf.read(str(RUN / "03" / "vocal.wav"), dtype="float32", always_2d=True)
    vocal = vocal.mean(axis=1)
    sp0, sp1 = prompt["_wav_span"]
    seg = vocal[int(sp0 * vsr):int(sp1 * vsr)]
    seg = soxr.resample(seg, vsr, SR_OUT)
    out_dir = RUN / "06" / "melody_probe"
    out_dir.mkdir(parents=True, exist_ok=True)
    sf.write(str(out_dir / "prompt_ref.wav"), seg, SR_OUT)
    p_dur = f"{len(seg)/SR_OUT:.3f}"

    n_p = int(round(len(seg) / SR_OUT * 50))
    pf0 = f0_for_span(times, midi, sp0, sp1, n_p)
    print(f"prompt f0: {int((pf0>0).sum())}/{n_p} voiced frames", flush=True)

    for mode in ("score", "melody"):
        p = dict(prompt)
        # keep the model's own per-note duration list; overwriting it with a single
        # number is what made merge_phoneme index past the end of the arrays
        p.pop("_wav_span", None)
        p.pop("_median_note", None)
        p.pop("_song_median_note", None)
        t = dict(tgt)

        if mode == "melody":
            p["f0"] = " ".join(f"{v:.2f}" for v in pf0)
            n_t = int(round((t["time"][1] - t["time"][0]) / 1000.0 * 50))
            tf0 = f0_for_span(times, midi, t["time"][0] / 1000.0,
                              t["time"][1] / 1000.0, n_t)
            t["f0"] = " ".join(f"{v:.2f}" for v in tf0)
            print(f"  {mode}: target f0 {int((tf0>0).sum())}/{n_t} voiced", flush=True)

        pd = dp.process(json.loads(json.dumps(p)), str(out_dir / "prompt_ref.wav"))
        td = dp.process(json.loads(json.dumps(t)))
        gen = model.infer({"prompt": pd, "target": td}, auto_shift=False, pitch_shift=0,
                          n_steps=cfg.infer.n_steps, cfg=cfg.infer.cfg,
                          control=mode, use_fp16=True)
        y = gen.squeeze().float().cpu().numpy()
        pk = float(np.max(np.abs(y)))
        if pk > 0:
            y = y / pk * 0.9
        sf.write(str(out_dir / f"{mode}.wav"), y, SR_OUT)
        print(f"  {mode}: {len(y)/SR_OUT:.2f}s -> {mode}.wav", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
