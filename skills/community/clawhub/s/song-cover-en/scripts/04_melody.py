"""Stage 4 (v2) - real melody extraction with RMVPE, then note segmentation.

Differences from the old pipeline, and why each mattered:

  * RMVPE instead of librosa.pyin.  pyin's Viterbi smoothing drags onsets by
    tens of milliseconds and invents vibrato; RMVPE is what RVC uses for the
    same job.  Its mel front end was calibrated against a known-answer example
    (0.28 semitone median error), see probe_mel_frontend.py.
  * NO forced note count.  The old code computed `k = chinese characters` and
    ran a fixed-k DP, which is why the melody did not line up with the record.
    Here note boundaries come from actual pitch movement.
  * NO scale snapping and NO hard-coded key.  The old code snapped every note
    into a fixed F#-major pitch-class set with a 42-cent window, destroying
    accidentals and any real intonation.

Outputs in <run-dir>/04:
  melody.json   {fps, notes:[{start_s,end_s,dur_s,midi}], segments, bpm}
  f0.csv        frame-level f0 for inspection
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from _env import LIBS, RMVPE

if str(LIBS) not in sys.path:
    sys.path.insert(0, str(LIBS))

import librosa  # noqa: E402
import numpy as np  # noqa: E402
import onnxruntime as ort  # noqa: E402
import soundfile as sf  # noqa: E402
import soxr  # noqa: E402


SR = 16000          # rmvpe's native rate
HOP = 160           # 10 ms frames
N_FFT = 1024
N_MELS = 128
FMIN = 30.0
FMAX = 8000.0
PAD_MULT = 32
CENTS = 20.0 * np.arange(360) + 1997.3794084376191
CONF_TH = 0.10


class RMVPE:
    def __init__(self, path: Path = RMVPE, device: str = "cpu"):
        so = ort.SessionOptions()
        so.log_severity_level = 3
        providers = (["CUDAExecutionProvider", "CPUExecutionProvider"] if device == "cuda"
                     else ["CPUExecutionProvider"])
        self.sess = ort.InferenceSession(str(path), sess_options=so, providers=providers)
        self.name = self.sess.get_inputs()[0].name

    def mel(self, y: np.ndarray) -> np.ndarray:
        """(128, T) natural-log mel - the transform rmvpe was trained with.

        Getting this wrong is invisible in the *shape* of the pitch contour but
        shifts every value by a constant, so the model's confidence collapses and
        most sung frames get dropped. Calibrated against the shipped example,
        whose notes are known: natural log + htk=True + slaney norm gives 0.28
        semitone median error, while dB scaling gave 5.5 and log with htk=False
        also 5.7. See probe_frontend2.py and calib_rmvpe.py.
        """
        pad = N_FFT // 2
        yp = np.pad(y.astype(np.float32), (pad, pad), mode="reflect")
        spec = np.abs(librosa.stft(yp, n_fft=N_FFT, hop_length=HOP, window="hann", center=False))
        fb = librosa.filters.mel(sr=SR, n_fft=N_FFT, n_mels=N_MELS,
                                 fmin=FMIN, fmax=FMAX, htk=True, norm="slaney")
        return np.log(np.maximum(fb @ spec, 1e-5)).astype(np.float32)

    def __call__(self, y: np.ndarray, chunk_s: float = 30.0) -> tuple[np.ndarray, np.ndarray]:
        """Frame-wise f0 + salience, chunked so long songs do not blow up memory."""
        hop_s = HOP / SR
        step = int(chunk_s / hop_s)
        f0_all, conf_all = [], []
        n = len(y)
        for start in range(0, n, step * HOP):
            seg = y[start:start + step * HOP + N_FFT]
            if len(seg) < N_FFT * 2:
                break
            m = self.mel(seg)
            t = m.shape[1]
            pad_t = PAD_MULT * ((t - 1) // PAD_MULT + 1) - t
            if pad_t:
                m = np.pad(m, ((0, 0), (0, pad_t)), mode="constant")
            sal = self.sess.run(None, {self.name: m[None]})[0][0][:t]
            conf = sal.max(axis=1)
            idx = sal.argmax(axis=1)
            cents = CENTS[idx]
            lo, hi = np.clip(idx - 1, 0, 359), np.clip(idx + 1, 0, 359)
            ar = np.arange(len(idx))
            a, b, c = sal[ar, lo], conf, sal[ar, hi]
            den = a - 2 * b + c
            with np.errstate(divide="ignore", invalid="ignore"):
                d = np.where(np.abs(den) > 1e-9, 0.5 * (a - c) / den, 0.0)
            cents = cents + 20.0 * np.clip(d, -0.5, 0.5)
            f0 = 10.0 * (2.0 ** (cents / 1200.0))
            keep = min(len(f0), step)
            f0_all.append(np.where(conf > CONF_TH, f0, 0.0)[:keep])
            conf_all.append(conf[:keep])
        return np.concatenate(f0_all), np.concatenate(conf_all)


def to_midi(f0: np.ndarray) -> np.ndarray:
    m = np.full(len(f0), np.nan)
    v = f0 > 0
    m[v] = 69.0 + 12.0 * np.log2(f0[v] / 440.0)
    return m


def median_filter(x: np.ndarray, k: int = 5) -> np.ndarray:
    """Kill single-frame octave jumps without moving real onsets."""
    if len(x) < k:
        return x
    pad = k // 2
    xp = np.pad(x, pad, mode="edge")
    win = np.lib.stride_tricks.sliding_window_view(xp, k)
    with np.errstate(invalid="ignore"):
        out = np.nanmedian(win, axis=1)
    out[np.isnan(x)] = np.nan
    return out


def fix_octaves(midi: np.ndarray, window: int = 80) -> np.ndarray:
    """Fold obvious octave errors toward a local median."""
    out = midi.copy()
    n = len(out)
    for i in range(0, n, window // 2):
        seg = out[i:i + window]
        v = seg[~np.isnan(seg)]
        if len(v) < 5:
            continue
        ref = np.median(v)
        for j in range(len(seg)):
            if np.isnan(seg[j]):
                continue
            for shift in (-24, -12, 12, 24):
                cand = seg[j] + shift
                if abs(cand - ref) < abs(seg[j] - ref) - 1.0:
                    seg[j] = cand
        out[i:i + window] = seg
    return out


def detrend_vibrato(midi: np.ndarray, fps: float, win_s: float = 0.20) -> np.ndarray:
    """Median-filter the singer's vibrato away so segmentation sees notes, not wobble.

    A trained singer oscillates ~5-7 Hz, one full cycle every ~0.15-0.20 s. Any
    smoother than that leaves the wobble intact, and the segmenter then cuts a
    single held note into a dozen 80 ms shards. That is the root cause of the
    granular, unintelligible delivery: a neural singer needs tens of milliseconds
    to establish a vowel formant, so an 80 ms shard comes out as a click rather
    than a word. Median filtering is the right tool here -- it removes the
    symmetric oscillation while leaving genuine step changes to a new pitch sharp.
    """
    if len(midi) < 3:
        return midi
    k = int(round(win_s * fps))
    if k % 2 == 0:
        k += 1
    k = max(3, k)
    if k >= len(midi):
        return midi
    pad = k // 2
    xp = np.pad(midi, pad, mode="edge")
    win = np.lib.stride_tricks.sliding_window_view(xp, k)
    with np.errstate(invalid="ignore"):
        out = np.nanmedian(win, axis=1)
    out[np.isnan(midi)] = np.nan
    return out


def absorb_shards(notes: list[dict], min_sung: float = 0.12) -> list[dict]:
    """Fold notes too short to voice into whichever neighbour is closer in pitch.

    Dropping them (what this used to do) punches holes in the melody and makes the
    singer skip syllables; absorbing them keeps the line continuous.
    """
    if not notes:
        return []
    out = [dict(n) for n in notes]
    while True:
        short = next((i for i, n in enumerate(out) if n["dur_s"] < min_sung), None)
        if short is None or len(out) < 2:
            break
        n = out[short]
        cands = [k for k in (short - 1, short + 1) if 0 <= k < len(out)]
        j = min(cands, key=lambda k: abs(out[k]["midi"] - n["midi"]))
        if j < short:
            out[j]["end_s"] = n["end_s"]
        else:
            out[j]["start_s"] = n["start_s"]
        out[j]["dur_s"] = out[j]["end_s"] - out[j]["start_s"]
        del out[short]
    # absorbing leaves neighbours that now share a pitch: fold them too
    merged: list[dict] = []
    for note in out:
        if (merged and abs(note["midi"] - merged[-1]["midi"]) < 0.9
                and note["start_s"] - merged[-1]["end_s"] <= 0.03):
            merged[-1]["end_s"] = note["end_s"]
            merged[-1]["dur_s"] = merged[-1]["end_s"] - merged[-1]["start_s"]
        else:
            merged.append(note)
    return merged


def segment_notes(midi: np.ndarray, fps: float, min_dur: float = 0.05,
                  pitch_jump: float = 0.85, merge_gap: float = 0.03,
                  min_sung: float = 0.12) -> list[dict]:
    """Pitch-movement segmentation. No note count is assumed anywhere."""
    notes: list[dict] = []
    n = len(midi)
    i = 0
    while i < n:
        if np.isnan(midi[i]):
            i += 1
            continue
        ref = midi[i]
        j = i + 1
        while j < n and not np.isnan(midi[j]):
            # a note ends when the tracker clearly moves to another pitch
            if abs(midi[j] - ref) > pitch_jump:
                break
            ref = np.median(midi[i:j + 1])
            j += 1
        seg = midi[i:j][~np.isnan(midi[i:j])]
        if len(seg) / fps >= min_dur:
            notes.append({"start_s": i / fps, "end_s": j / fps,
                          "dur_s": (j - i) / fps, "midi": float(np.median(seg))})
        i = j
    # merge same-pitch neighbours split by a one-frame dropout
    merged: list[dict] = []
    for note in notes:
        if (merged and abs(note["midi"] - merged[-1]["midi"]) < 0.6
                and note["start_s"] - merged[-1]["end_s"] <= merge_gap):
            merged[-1]["end_s"] = note["end_s"]
            merged[-1]["dur_s"] = merged[-1]["end_s"] - merged[-1]["start_s"]
            merged[-1]["midi"] = (merged[-1]["midi"] * 0.5 + note["midi"] * 0.5)
        else:
            merged.append(note)
    for note in merged:
        note["start_s"] = round(note["start_s"], 3)
        note["end_s"] = round(note["end_s"], 3)
        note["dur_s"] = round(note["dur_s"], 3)
        note["midi"] = round(note["midi"], 2)
        note["midi_int"] = int(round(note["midi"]))
    return [x for x in merged if x["dur_s"] >= min_dur]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--vocal", default=None, help="default <run>/03/vocal.wav")
    ap.add_argument("--min-dur", type=float, default=0.05)
    ap.add_argument("--pitch-jump", type=float, default=0.85)
    ap.add_argument("--min-sung", type=float, default=0.12,
                    help="notes shorter than this cannot carry a vowel; absorb them")
    ap.add_argument("--vibrato-win", type=float, default=0.20,
                    help="median window covering one vibrato cycle, in seconds")
    a = ap.parse_args()

    run = Path(a.run_dir)
    out = run / "04"
    out.mkdir(parents=True, exist_ok=True)
    vocal = Path(a.vocal) if a.vocal else run / "03" / "vocal.wav"

    y, sr = sf.read(str(vocal), dtype="float32", always_2d=True)
    y = y[:, 0]
    if sr != SR:
        y = soxr.resample(y, sr, SR).astype(np.float32)
    dur = len(y) / SR
    print(f"vocal {dur:.1f}s @ {SR}Hz -> {vocal.name}", flush=True)

    t0 = time.time()
    engine = RMVPE()
    f0, conf = engine(y)
    fps = SR / HOP
    print(f"rmvpe {len(f0)} frames in {time.time()-t0:.1f}s "
          f"(rtf {(time.time()-t0)/dur:.2f}), voiced {np.mean(f0>0):.0%}", flush=True)

    midi = to_midi(f0)
    midi = median_filter(midi, 5)
    midi = fix_octaves(midi)
    midi = detrend_vibrato(midi, fps, win_s=a.vibrato_win)
    voiced = float(np.mean(~np.isnan(midi)))
    print(f"after clean: voiced {voiced:.0%}", flush=True)

    notes = segment_notes(midi, fps, min_dur=a.min_dur, pitch_jump=a.pitch_jump)
    n_raw = len(notes)
    notes = absorb_shards(notes, min_sung=a.min_sung)
    for note in notes:
        note["start_s"] = round(note["start_s"], 3)
        note["end_s"] = round(note["end_s"], 3)
        note["dur_s"] = round(note["dur_s"], 3)
        note["midi"] = round(note["midi"], 2)
        note["midi_int"] = int(round(note["midi"]))
    print(f"notes: {n_raw} -> {len(notes)} after absorbing shards "
          f"(<{a.min_sung:.2f}s); covered {sum(n['dur_s'] for n in notes):.1f}s "
          f"of {dur:.1f}s", flush=True)
    if notes:
        import collections
        hist = collections.Counter(n["midi_int"] for n in notes)
        print("pitch histogram:", dict(sorted(hist.items())), flush=True)

    np.savetxt(out / "f0.csv", np.c_[np.arange(len(midi)) / fps, midi],
               delimiter=",", header="time_s,midi", comments="")

    # tempo/beats come from the instrumental (same timeline), for the visuals
    inst = run / "02" / "inst.wav"
    tempo, beats = None, []
    if inst.exists():
        yi, _ = librosa.load(str(inst), sr=22050, mono=True)
        tempo, beat_f = librosa.beat.beat_track(y=yi, sr=22050, hop_length=512, units="frames")
        beats = (beat_f * 512 / 22050).tolist()
        tempo = float(np.atleast_1d(tempo)[0])

    payload = {"fps": fps, "duration_s": round(dur, 3), "vnv_rate": round(voiced, 3),
               "n_notes": len(notes), "notes": notes,
               "tempo": round(tempo, 2) if tempo else None,
               "beats": [round(b, 3) for b in beats]}
    (out / "melody.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                                     encoding="utf-8")
    print(f"-> {out/'melody.json'}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
