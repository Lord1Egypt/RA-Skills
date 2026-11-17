"""Compare timbre references: does a clean studio acapella prompt fix the muffled,
electronic-sounding output?

Renders the same short lyric window twice -- once cloning the timbre of the
separated Chinese vocal (current pipeline), once cloning the official example
acapella -- so the two outputs differ only in the prompt audio.
"""
from __future__ import annotations

import sys

sys.path.insert(0, str(SRC))

import json
from pathlib import Path

from _env import LIBS, RUNS, SRC, CKPT, CFG

sys.path.insert(0, str(LIBS))

import numpy as np
import soundfile as sf
import soxr
import torch
from omegaconf import OmegaConf

from soulxsinger.models.soulxsinger import SoulXSinger
from soulxsinger.utils.data_processor import DataProcessor

RUN = RUNS / "sudi"
PHONESET = SRC / "soulxsinger" / "utils" / "phoneme" / "phone_set.json"
EX = SRC / "example" / "audio"
SR = 24000


def build(cfg):
    m = SoulXSinger(cfg)
    ck = torch.load(CKPT, map_location="cpu", weights_only=False)
    m.load_state_dict(ck["state_dict"], strict=True)
    del ck
    m.half()
    m.mel.float()
    return m.to("cuda").eval()


def main() -> int:
    cfg = OmegaConf.load(CFG)
    model = build(cfg)
    dp = DataProcessor(hop_size=cfg.audio.hop_size, sample_rate=cfg.audio.sample_rate,
                       phoneset_path=str(PHONESET), device="cuda")

    targets = json.loads((RUN / "05" / "target.json").read_text(encoding="utf-8"))
    prompts = json.loads((RUN / "05" / "prompt.json").read_text(encoding="utf-8"))
    tgt = targets[0]
    # keep the probe short: first ~12s of the first section
    want = 12.0
    durs = [float(x) for x in tgt["duration"].split()]
    ph = tgt["phoneme"].split()
    pz = tgt["note_pitch"].split()
    ty = tgt["note_type"].split()
    acc, cut = 0.0, len(durs)
    for i, d in enumerate(durs):
        acc += d
        if acc >= want:
            cut = i + 1
            break
    short = {"time": [0, int(round(acc * 1000))],
             "duration": " ".join(f"{x:.3f}" for x in durs[:cut]),
             "phoneme": " ".join(ph[:cut]),
             "note_pitch": " ".join(pz[:cut]),
             "note_type": " ".join(ty[:cut])}
    print(f"probe {acc:.1f}s, {cut} notes", flush=True)

    out = RUN / "06" / "probe"
    out.mkdir(parents=True, exist_ok=True)

    # A: separated Chinese vocal, as the pipeline currently does
    p = prompts[0]
    span = p.get("_wav_span")
    voc, vsr = sf.read(str(RUN / "03" / "vocal.wav"), dtype="float32", always_2d=True)
    voc = voc[:, 0]
    a_seg = voc[int(span[0] * vsr): int(span[1] * vsr)] if span else voc[: 3 * vsr]
    a_seg = soxr.resample(a_seg, vsr, SR).astype(np.float32)
    sf.write(str(out / "prompt_A.wav"), a_seg, SR)
    pa = dp.process(p, str(out / "prompt_A.wav"))

    # B: official studio acapella (different singer, clean full-band)
    pb_meta = json.loads((EX / "en_prompt.json").read_text(encoding="utf-8"))[0]
    yb, ysr = sf.read(str(EX / "en_prompt.mp3"), dtype="float32", always_2d=True)
    yb = yb.mean(axis=1)
    s0, s1 = pb_meta["time"][0] / 1000.0, pb_meta["time"][1] / 1000.0
    yb = yb[int(s0 * ysr): int(s1 * ysr)]
    yb = soxr.resample(yb, ysr, SR).astype(np.float32)
    sf.write(str(out / "prompt_B.wav"), yb, SR)
    pb = dp.process(pb_meta, str(out / "prompt_B.wav"))

    for name, pd in (("A_separated", pa), ("B_official", pb)):
        # dp.process mutates its meta in place (strings -> lists), so each render
        # needs a pristine copy or the second call fails
        audio = model.infer({"prompt": pd,
                             "target": dp.process(json.loads(json.dumps(short)), None)},
                            auto_shift=False, pitch_shift=0,
                            n_steps=cfg.infer.n_steps, cfg=cfg.infer.cfg,
                            control="score", use_fp16=True)
        y = audio.detach().float().cpu().numpy().reshape(-1)
        y = y / (np.abs(y).max() + 1e-9) * 0.89
        sf.write(str(out / f"{name}.wav"), y, SR)
        print(f"{name}: {len(y)/SR:.2f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
