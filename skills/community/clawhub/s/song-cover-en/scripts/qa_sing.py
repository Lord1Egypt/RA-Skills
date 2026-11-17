"""Objective QA for the v2 cover: is it intelligible, and is it on the melody?

Two things can go wrong that ear alone catches late:
  * the singing model mangles the English into mush -> ASR word recall
  * the notes we fed it did not actually land -> compare the sung f0 against the
    notes we asked for, in semitones

Nothing here replaces listening, but both metrics catch real faults early.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from _env import LIBS, SRC, RMVPE, WHISPER

for p in (str(LIBS), str(SRC), str(Path(__file__).resolve().parent)):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
import soxr  # noqa: E402



def load_whisper():
    from transformers import WhisperForConditionalGeneration, WhisperProcessor
    proc = WhisperProcessor.from_pretrained(str(WHISPER))
    model = WhisperForConditionalGeneration.from_pretrained(str(WHISPER)).eval()
    return proc, model


def transcribe(proc, model, y, sr: int = 24000) -> str:
    import torch
    y16 = soxr.resample(y.astype(np.float32), sr, 16000)
    out = []
    # 30 s windows, which is what whisper expects
    for i in range(0, max(len(y16), 1), 16000 * 30):
        chunk = y16[i:i + 16000 * 30]
        if len(chunk) < 1600:
            continue
        feats = proc(chunk, sampling_rate=16000, return_tensors="pt").input_features
        with torch.no_grad():
            ids = model.generate(feats, max_new_tokens=200)
        out.append(proc.batch_decode(ids, skip_special_tokens=True)[0].strip())
    return " ".join(out)


def words(s: str) -> list[str]:
    return re.findall(r"[a-z']+", s.lower())


def recall(expected: str, got: str) -> float:
    exp, gotw = words(expected), words(got)
    if not exp:
        return 0.0
    pool: dict[str, int] = {}
    for w in gotw:
        pool[w] = pool.get(w, 0) + 1
    hit = 0
    for w in exp:
        if pool.get(w, 0) > 0:
            pool[w] -= 1
            hit += 1
    return hit / len(exp)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--vocal", default=None)
    ap.add_argument("--no-asr", action="store_true")
    a = ap.parse_args()

    run = Path(a.run_dir)
    path = Path(a.vocal) if a.vocal else run / "06" / "vocal_en.wav"
    y, sr = sf.read(str(path), dtype="float32", always_2d=True)
    y = y[:, 0]
    print(f"{path.name}: {len(y)/sr:.2f}s @ {sr}Hz, rms {np.sqrt((y**2).mean()):.4f}, "
          f"peak {np.abs(y).max():.3f}", flush=True)

    # silence is expected where the original had none: sections were rendered separately
    frame = int(0.02 * sr)
    nf = len(y) // frame
    rms = np.sqrt((y[:nf * frame].reshape(nf, frame) ** 2).mean(axis=1))
    voiced = rms > max(0.01, np.percentile(rms, 90) * 0.06)
    print(f"voiced frames {voiced.mean():.1%} (rest is instrumental space)", flush=True)

    report = {"path": str(path), "duration_s": round(len(y) / sr, 2),
              "voiced_ratio": round(float(voiced.mean()), 3)}

    # ---- did the notes land? compare sung f0 against the notes we asked for
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "mel", str(Path(__file__).resolve().parent / "04_melody.py"))
    mel = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mel)
    eng = mel.RMVPE()
    # RMVPE's front end is calibrated for 16 kHz and does no resampling of its own,
    # so hand it 16 kHz. Feeding the 24 kHz mixstraight in shifts every pitch by
    # 12*log2(24/16) = -7.02 semitones and looks exactly like a transposed vocal.
    f0, conf = eng(soxr.resample(y.astype(np.float32), sr, mel.SR))
    fps = mel.SR / mel.HOP
    midi = np.full(len(f0), np.nan)
    v = (conf > 0.10) & (f0 > 0)
    midi[v] = 69.0 + 12.0 * np.log2(f0[v] / 440.0)

    targets = json.loads((run / "05" / "target.json").read_text(encoding="utf-8"))
    errs, pairs = [], []
    for t in targets:
        pitches = [int(x) for x in t["note_pitch"].split()]
        durs = [float(x) for x in t["duration"].split()]
        # events are laid end to end from time[0]; recover each note's own window
        cursor = t["time"][0] / 1000.0
        for p, d in zip(pitches, durs):
            s, e = cursor, cursor + d
            cursor = e
            if p <= 0:
                continue
            seg = midi[int(s * fps):int(e * fps)]
            seg = seg[~np.isnan(seg)]
            if len(seg) < 4:
                continue
            sung = float(np.median(seg))
            pairs.append((p, sung))
            errs.append(abs(sung - p))
    if errs:
        e = np.array(errs)
        print(f"\nnote landing: {len(e)} notes matched, median |err| {np.median(e):.2f} st, "
              f"within 50c {np.mean(e <= 0.5):.0%}, p90 {np.percentile(e, 90):.2f}", flush=True)
        report.update(note_matched=len(e), note_median_err=round(float(np.median(e)), 3),
                      note_within_50c=round(float(np.mean(e <= 0.5)), 3))
        if len(pairs) > 8:
            pp = np.array(pairs)
            off = float(np.median(pp[:, 1] - pp[:, 0]))
            resid = pp[:, 1] - pp[:, 0] - off
            corr = float(np.corrcoef(pp[:, 0], pp[:, 1])[0, 1])
            print(f"  constant offset {off:+.2f} st (auto_shift transposing the whole tune); "
                  f"after removing it median |err| {np.median(np.abs(resid)):.2f} st, "
                  f"within 50c {np.mean(np.abs(resid) <= 0.5):.0%}, corr {corr:.3f}", flush=True)
            report.update(pitch_offset_st=round(off, 3),
                          note_median_err_detrended=round(float(np.median(np.abs(resid))), 3),
                          pitch_corr=round(corr, 3))

    # ---- can a listener understand it?
    if not a.no_asr:
        words_obj = json.loads((Path(__file__).resolve().parents[1] / "assets" / "lyrics_en.json")
                               .read_text(encoding="utf-8"))
        # only score lines that were actually rendered; otherwise the denominator
        # includes lines we never asked the model to sing
        sung_until = max(t["time"][1] / 1000.0 for t in targets)
        lines_meta = json.loads((run / "05" / "align.json").read_text(encoding="utf-8"))
        rendered = [r["en"] for r in lines_meta if r["t"] <= sung_until]
        expect = " ".join(rendered)
        proc, model = load_whisper()
        got = transcribe(proc, model, y, sr)
        r = recall(expect, got)
        print(f"\nASR word recall {r:.0%} over {len(rendered)} rendered lines", flush=True)
        print("heard:", got[:600], flush=True)
        report.update(asr_recall=round(r, 3), asr_lines=len(rendered), asr_text=got[:2000])
        per = []
        for r_ in lines_meta:
            if r_["t"] > sung_until:
                continue
            per.append({"en": r_["en"], "recall": round(recall(r_["en"], got), 2)})
        zero = [p for p in per if p["recall"] == 0]
        print(f"  lines with no word recovered: {len(zero)}/{len(per)}", flush=True)
        report["per_line"] = per

    (run / "06" / "qa_sing.json").write_text(json.dumps(report, ensure_ascii=False, indent=1),
                                             encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
