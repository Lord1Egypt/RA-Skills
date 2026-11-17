"""Stage 6 (v2) - sing the English lyrics with SoulX-Singer.

This replaces the old edge-tts + WORLD route entirely. That route synthesised a
*speaking* voice and then bent it onto notes with a vocoder, which is where the
buzzy, robotic timbre came from; it also had to guess note boundaries, which is
why the melody drifted. Here a flow-matching singing model is given the exact
notes of the original melody plus the phonemes of each English syllable, so both
the timbre and the tune come from the model rather than from a vocoder.

`control="score"` is what pins the tune: note_pitch fully determines pitch and no
f0 contour is needed. `auto_shift` aligns the prompt singer's register to the
target notes so the reference timbre is not transposed into a growl.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from _env import LIBS, SRC, CKPT, CFG

for p in (str(LIBS), str(SRC)):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
import torch  # noqa: E402
from omegaconf import OmegaConf  # noqa: E402

from soulxsinger.models.soulxsinger import SoulXSinger  # noqa: E402
from soulxsinger.utils.data_processor import DataProcessor  # noqa: E402

PHONESET = SRC / "soulxsinger" / "utils" / "phoneme" / "phone_set.json"
SR_OUT = 24000


def build_model(cfg, use_fp16: bool = True):
    model = SoulXSinger(cfg)
    ck = torch.load(str(CKPT), weights_only=False, map_location="cpu")
    model.load_state_dict(ck["state_dict"], strict=True)
    del ck
    if use_fp16:
        model.half()
        model.mel.float()      # the mel front end must stay fp32, upstream does this too
    return model.to("cuda").eval()


def split_segment(seg: dict, max_s: float = 24.0) -> list[dict]:
    """Cut one target section into chunks of at most `max_s` seconds.

    The model's cost grows much faster than linearly with sequence length: a 79 s
    section renders in 43 s, while a 118 s section took 1909 s. Rendering in ~24 s
    chunks keeps every pass in the cheap regime and, as a bonus, bounds the damage
    if one chunk fails.

    Cuts are made at rests when possible so no syllable is sliced in half; a cut is
    never made inside a word, because the two halves are rendered in separate model
    passes and the word comes out garbled.
    """
    pitches = [int(x) for x in seg["note_pitch"].split()]
    durs = [float(x) for x in seg["duration"].split()]
    types = [int(x) for x in seg["note_type"].split()]
    phons = seg["phoneme"].split()
    wstarts = seg.get("word_start")
    wst = ([int(x) for x in wstarts.split()] if wstarts else [0] * len(durs))
    if len(wst) != len(durs):
        wst = [0] * len(durs)
    if len(durs) <= 1:
        return [dict(seg)]

    bounds = [0]
    n = len(durs)
    i = 0
    while i < n:
        # Pick the cut only where note k *begins* a word: the next chunk then starts
        # on a word onset, so no word is ever split across two model passes.
        # Melisma notes repeat the previous syllable with word_start=0 and are never
        # chosen; a rest is fine to start on, but the cut point still has to be a
        # word onset so the chunk after it begins at a word.
        acc = 0.0
        last_ok = None          # latest word onset that still fits in max_s
        first_over = None       # earliest word onset that does not fit
        for j in range(i, n):
            acc += durs[j]
            if j > i and wst[j] == 1:
                if acc <= max_s:
                    last_ok = j
                elif first_over is None:
                    first_over = j
                    break
        if last_ok is None and first_over is None:
            break                      # no word boundary left: one final chunk
        nxt = last_ok if last_ok is not None else first_over
        if nxt is None or nxt <= i or nxt >= n:
            break
        bounds.append(nxt)
        i = nxt
    bounds.append(n)

    out = []
    for a, b in zip(bounds, bounds[1:]):
        if b <= a:
            continue
        t0 = seg["time"][0] + int(round(sum(durs[:a]) * 1000))
        t1 = seg["time"][0] + int(round(sum(durs[:b]) * 1000))
        out.append({
            "time": [t0, t1],
            "duration": " ".join(f"{x:.3f}" for x in durs[a:b]),
            "phoneme": " ".join(phons[a:b]),
            "note_pitch": " ".join(str(x) for x in pitches[a:b]),
            "note_type": " ".join(str(x) for x in types[a:b]),
            "word_start": " ".join(str(x) for x in wst[a:b]),
        })
    return out or [dict(seg)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--control", default="score", choices=["score", "melody"])
    ap.add_argument("--pitch-shift", type=int, default=0)
    ap.add_argument("--auto-shift", action="store_true",
                    help="let the model transpose every note by median(prompt) - "
                         "median(target). Off by default: with control='score' the notes "
                         "already pin the pitch, and shifting per section introduces a "
                         "different offset in each section, which detunes the cover "
                         "against the original key")
    ap.add_argument("--fp32", action="store_true")
    ap.add_argument("--chunk-s", type=float, default=24.0,
                    help="render in chunks of at most this many seconds; cost per "
                         "second of audio rises steeply with sequence length")
    ap.add_argument("--only", type=int, default=None, help="render a single section index")
    ap.add_argument("--seed", type=int, default=42,
                    help="torch.manual_seed before each infer; diffusion starts from "
                         "random noise so an unseeded run is a new sample every time")
    a = ap.parse_args()

    run = Path(a.run_dir)
    out = run / "06"
    out.mkdir(parents=True, exist_ok=True)

    prompts = json.loads((run / "05" / "prompt.json").read_text(encoding="utf-8"))
    targets = json.loads((run / "05" / "target.json").read_text(encoding="utf-8"))
    if not prompts or not targets:
        print("missing 05/prompt.json or 05/target.json", file=sys.stderr)
        return 2

    cfg = OmegaConf.load(str(CFG))
    t0 = time.time()
    model = build_model(cfg, use_fp16=not a.fp32)
    print(f"model ready in {time.time()-t0:.1f}s", flush=True)
    dp = DataProcessor(hop_size=cfg.audio.hop_size, sample_rate=cfg.audio.sample_rate,
                       phoneset_path=str(PHONESET), device="cuda")

    # The prompt is the original singer's phrase cut from the isolated vocal, so the
    # cover keeps that artist's timbre instead of borrowing a stock voice.
    p = prompts[0]
    span = p.get("_wav_span")
    voc, vsr = sf.read(str(run / "03" / "vocal.wav"), dtype="float32", always_2d=True)
    voc = voc[:, 0]
    if span:
        seg = voc[int(span[0] * vsr): int(span[1] * vsr)]
    else:
        seg = voc[: int(3.0 * vsr)]
    import soxr
    seg = soxr.resample(seg, vsr, SR_OUT).astype(np.float32)
    prompt_wav = out / "prompt_ref.wav"
    sf.write(str(prompt_wav), seg, SR_OUT)
    prompt_data = dp.process(p, str(prompt_wav))
    print(f"prompt: {len(seg)/SR_OUT:.2f}s, mel2note {tuple(prompt_data['mel2note'].shape)}",
          flush=True)

    # total length is the end of the last section, so silences between sections survive
    total_s = max(t["time"][1] for t in targets) / 1000.0
    merged = np.zeros(int(round(total_s * SR_OUT)), dtype=np.float32)
    weight = np.zeros_like(merged)      # accumulate with fades so joins do not click

    idxs = [a.only] if a.only is not None else list(range(len(targets)))
    chunks: list[dict] = []
    for i in idxs:
        for ci, ch in enumerate(split_segment(targets[i], a.chunk_s)):
            ch["_group"] = i
            ch["_chunk"] = ci
            chunks.append(ch)
    print(f"rendering {len(chunks)} chunks (max {a.chunk_s:.0f}s each)", flush=True)

    for ci, t in enumerate(chunks):
        tgt = dp.process(t, None)
        st = time.time()
        with torch.no_grad():
            torch.manual_seed(a.seed + ci)  # deterministic: diffusion starts from noise
            audio = model.infer({"prompt": prompt_data, "target": tgt},
                                auto_shift=a.auto_shift, pitch_shift=a.pitch_shift,
                                n_steps=cfg.infer.n_steps, cfg=cfg.infer.cfg,
                                control=a.control, use_fp16=not a.fp32)
        el = time.time() - st
        y = audio.squeeze().float().cpu().numpy().astype(np.float32)
        s0 = int(round(t["time"][0] / 1000.0 * SR_OUT))
        n = min(len(y), len(merged) - s0)
        if n <= 0:
            print(f"chunk {ci}: skipped (outside buffer)", flush=True)
            continue
        w = np.ones(n, dtype=np.float32)
        fade = min(int(0.03 * SR_OUT), n // 2)
        if fade > 2:
            w[:fade] = np.linspace(0, 1, fade, dtype=np.float32)
            w[-fade:] = np.linspace(1, 0, fade, dtype=np.float32)
        merged[s0:s0 + n] += y[:n] * w
        weight[s0:s0 + n] += w
        dur = (t["time"][1] - t["time"][0]) / 1000.0
        print(f"chunk {ci} (sec {t['_group']}): {dur:.1f}s text, {len(y)/SR_OUT:.2f}s audio, "
              f"{el:.1f}s (rtf {el/dur:.2f})", flush=True)

    nz = weight > 1e-6
    merged[nz] /= weight[nz]

    # simple declick, then write
    merged = np.nan_to_num(merged, nan=0.0, posinf=0.0, neginf=0.0)
    peak = float(np.abs(merged).max())
    if peak > 0:
        merged = merged / peak * 0.89
    path = out / "vocal_en.wav"
    sf.write(str(path), merged, SR_OUT)
    print(f"\nwrote {path} ({len(merged)/SR_OUT:.2f}s, peak was {peak:.3f})", flush=True)

    (out / "sing.json").write_text(json.dumps({
        "control": a.control, "pitch_shift": a.pitch_shift,
        "sections": len(idxs), "duration_s": round(len(merged) / SR_OUT, 2),
        "peak_in": round(peak, 4),
    }, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
