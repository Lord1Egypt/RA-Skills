#!/usr/bin/env python3
"""fridge_sound_analyzer.py — diagnose refrigerator health from a recording.

A healthy fridge is a quiet machine with a boring, predictable voice:
a low 50/60 Hz compressor hum (with 120/240 Hz harmonics) that cycles on
30-50% of the time, and near-silence in between. When something fails,
the SOUND changes before the temperature does:

  - failed door seal / dirty coils / low refrigerant → compressor runs
    almost constantly (duty cycle creeps 70%+)
  - worn mounts / unlevel feet / fan hitting ice → the hum acquires an
    amplitude-modulated rattle (4-15 Hz flutter)
  - ice-builder-upper or dying evaporator fan → sustained broadband hiss
  - hard-starting relay/capacitor → frequent loud clicks, short cycles

This tool analyzes a WAV recording (mono/stereo, any common bit depth the
stdlib wave module reads; phone voice-memo WAVs after conversion) with a
pure-Python DSP chain — frame energies, zero-crossing rate, lag
autocorrelation for the hum fundamental, envelope modulation spectrum —
and prints a verdict with likely causes and a technician brief.

Usage:
  python3 fridge_sound_analyzer.py analyze recording.wav [--duration 30]
  python3 fridge_sound_analyzer.py demo        # generates + analyzes two synthetic samples

No third-party dependencies. Relative loudness only (phone mics are not
calibrated) — the diagnostic value is in PATTERN, not absolute dB.
"""
from __future__ import annotations

import array
import io
import math
import sys
import wave
from pathlib import Path

TARGET_SR = 11025  # downsample target: enough for 5 kHz analysis
FRAME_MS = 10      # analysis frame


# ---------- loading ----------

def read_wav(path: str):
    with wave.open(path, "rb") as w:
        nch, sw, sr, nfr = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(nfr)
    if sw == 2:
        samples = array.array("h"); samples.frombytes(raw)
    elif sw == 4:
        a = array("i"); a.frombytes(raw); samples = a
    elif sw == 1:
        samples = array.array("h", [(b - 128) * 256 for b in raw])
    else:
        raise SystemExit(f"unsupported sample width {sw}")
    # mixdown to mono
    if nch > 1:
        samples = array.array("h", [samples[i] for i in range(0, len(samples), nch)])
    # decimate to TARGET_SR by boxcar average
    ratio = sr / TARGET_SR
    if ratio > 1.01:
        step = int(round(ratio))
        out = array.array("h")
        for i in range(0, len(samples) - step, step):
            out.append(int(sum(samples[i:i + step]) / step))
        samples, sr = out, sr // step
    return samples, sr


# ---------- features ----------

def frames(samples, sr, ms=FRAME_MS):
    n = max(1, sr * ms // 1000)
    for i in range(0, len(samples) - n, n):
        yield samples[i:i + n]


def rms_db(frame) -> float:
    if not frame:
        return -120.0
    e = sum(s * s for s in frame) / len(frame)
    return 10 * math.log10(e + 1) - 60.0 if e > 0 else -120.0  # rough dBFS-ish


def zcr(frame) -> float:
    if len(frame) < 2:
        return 0.0
    z = sum(1 for a, b in zip(frame, frame[1:]) if (a >= 0) != (b >= 0))
    return z / (len(frame) - 1)


def autocorr_f0(samples, sr, fmin=40, fmax=500) -> tuple[float, float]:
    """Dominant periodicity via normalized autocorrelation on the loudest window."""
    win = sr // 5  # 200 ms
    if len(samples) < win * 3:
        return 0.0, 0.0
    # loudest window
    best_i, best_e = 0, -1
    for i in range(0, len(samples) - win, win):
        e = sum(s * s for s in samples[i:i + win])
        if e > best_e:
            best_e, best_i = e, i
    w = samples[best_i:best_i + win]
    m = sum(w) / len(w)
    w = [s - m for s in w]
    denom = sum(s * s for s in w) or 1.0
    lag_min, lag_max = sr // fmax, sr // fmin
    best_lag, best_r = 0, 0.0
    for lag in range(lag_min, min(lag_max, len(w) // 2)):
        r = sum(w[i] * w[i + lag] for i in range(len(w) - lag)) / denom
        if r > best_r:
            best_r, best_lag = r, lag
    return (sr / best_lag if best_lag else 0.0), best_r


def envelope_modulation(db_series, fps) -> tuple[float, float]:
    """Peak flutter rate (Hz) and depth (%) of the loudness envelope."""
    m = sum(db_series) / len(db_series)
    detrended = [x - m for x in db_series]
    peaks = 0
    for a, b, c in zip(detrended, detrended[1:], detrended[2:]):
        if a < b >= c and b > 1.0:
            peaks += 1
    dur = len(db_series) / fps
    rate = peaks / dur if dur > 0 else 0.0
    depth = (max(db_series) - min(db_series))
    return rate, depth


# ---------- analysis ----------

def analyze(path: str) -> dict:
    samples, sr = read_wav(path)
    fps = 1000 // FRAME_MS
    dbs, zcrs = [], []
    for fr in frames(samples, sr):
        dbs.append(rms_db(fr))
        zcrs.append(zcr(fr))
    dur = len(dbs) / fps

    # noise floor = 10th percentile; active = 2x above it in dB terms (+3 dB)
    srt = sorted(dbs)
    floor = srt[len(srt) // 10]
    active_thr = floor + 3.0
    active = [d > active_thr for d in dbs]
    duty = sum(active) / len(active) if active else 0.0

    # energy stats while active
    act_db = [d for d, a in zip(dbs, active) if a] or [floor]
    mean_active = sum(act_db) / len(act_db)
    loud_frames = sum(1 for d in act_db if d > floor + 20)

    # transient clicks: isolated loud spikes (rise >12 dB over neighbors, <100 ms)
    clicks = 0
    for i in range(2, len(dbs) - 2):
        if dbs[i] > dbs[i - 2] + 12 and dbs[i] > dbs[i + 2] + 12:
            clicks += 1

    # broadband hiss: high ZCR while active
    hiss_frac = sum(1 for z, a in zip(zcrs, active) if a and z > 0.25) / max(1, sum(active))

    f0, r = autocorr_f0(samples, sr)
    am_rate, am_depth = envelope_modulation(
        [d for d, a in zip(dbs, active) if a] or dbs, fps
    )

    return {
        "file": Path(path).name, "seconds": round(dur, 1), "sr": sr,
        "noise_floor_db": round(floor, 1), "mean_active_db": round(mean_active, 1),
        "duty": duty, "loud_frames_pct": round(100 * loud_frames / max(1, len(act_db)), 1),
        "clicks_per_min": round(clicks / dur * 60, 1) if dur else 0.0,
        "hiss_frac": round(hiss_frac, 2), "hum_f0": round(f0, 1),
        "hum_strength": round(r, 2), "am_rate_hz": round(am_rate, 1),
        "am_depth_db": round(am_depth, 1),
    }


def verdict(m: dict) -> list[str]:
    out = []
    if m["duty"] > 0.70:
        out.append(f"COMPRESSOR OVER-RUNNING: active {m['duty']*100:.0f}% of the recording "
                   f"(healthy: 30-50%). Causes: door seal leak, dirty condenser coils, "
                   "low refrigerant, hot/enclosed installation, or thermostat stuck.")
    elif m["duty"] < 0.10 and m["seconds"] > 60:
        out.append(f"VERY QUIET: active only {m['duty']*100:.0f}% of the time. If the fridge "
                   "is warm inside, suspect the compressor not starting (see clicks) — "
                   "otherwise this may just be an efficient unit.")
    else:
        out.append(f"Cycle pattern: active {m['duty']*100:.0f}% of the time (normal band 30-50%).")

    if m["am_rate_hz"] >= 4 and m["am_rate_hz"] <= 15 and m["am_depth_db"] > 6:
        out.append(f"RATTLE DETECTED: loudness flutters ~{m['am_rate_hz']} Hz with "
                   f"{m['am_depth_db']} dB depth. Classic mechanical vibration — compressor "
                   "mount springs worn, feet unlevel, or a panel/line touching the frame. "
                   "Level the feet first (free), then check mounts.")
    if m["hiss_frac"] > 0.30:
        out.append(f"BROADBAND NOISE: {m['hiss_frac']*100:.0f}% of active time is hiss-like "
                   "(no tonal hum). Suspect evaporator/condenser fan — blade hitting ice or "
                   "bearing wear. Manual defrost first; if it returns within days, fan.")
    if m["clicks_per_min"] > 6:
        out.append(f"CLICKING {m['clicks_per_min']}/min: relay/overload chattering — hard "
                   "starts. Compressor may still start (weak capacitor) or be seized "
                   "(start-relay clicks, compressor hums, thermal cutoff).")
    if m["hum_f0"] >= 40 and m["hum_f0"] <= 130 and m["hum_strength"] > 0.5:
        out.append(f"Healthy tonal hum at {m['hum_f0']:.0f} Hz (mains harmonic) — "
                   "compressor voice itself sounds normal.")
    if not any(("OVER-RUNNING" in o or "RATTLE" in o or "BROADBAND" in o or "CLICKING" in o) for o in out):
        out.append("VERDICT: SOUND PROFILE NORMAL — no failure signature found. "
                   "If you still suspect a problem, record 10+ minutes and re-run.")
    return out


def report(m: dict) -> None:
    print(f"=== {m['file']} — {m['seconds']}s @ {m['sr']} Hz ===")
    for k in ("noise_floor_db", "mean_active_db", "duty", "hum_f0", "hum_strength",
              "am_rate_hz", "am_depth_db", "hiss_frac", "clicks_per_min"):
        print(f"  {k:16} {m[k]}")
    print()
    for line in verdict(m):
        print(" •", line)
    print()


# ---------- synthetic demo ----------

def synth(path: str, kind: str, seconds=20, sr=48000) -> None:
    import random
    random.seed(7)
    n = seconds * sr
    out = array.array("h")
    for i in range(n):
        t = i / sr
        v = 0.0
        running = (t % 20) < 14 if kind == "overrun" else (t % 20) < 8  # duty 70% vs 40%
        if running:
            hum = math.sin(2 * math.pi * 120 * t) + 0.5 * math.sin(2 * math.pi * 240 * t)
            v = 2500 * hum
            if kind == "rattle":
                v *= (1 + 0.6 * math.sin(2 * math.pi * 9 * t))  # 9 Hz flutter
        v += random.uniform(-60, 60)  # room noise
        out.append(int(max(-32767, min(32767, v))))
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(out.tobytes())


def demo() -> None:
    here = Path(__file__).parent
    for kind, label in (("overrun", "constant-running"), ("rattle", "rattling")):
        p = here / f"demo_{label}.wav"
        synth(str(p), kind)
        m = analyze(str(p))
        report(m)
        p.unlink(missing_ok=True)
    print("(demo wavs generated in-memory, analyzed, then removed)")


def main() -> None:
    if len(sys.argv) >= 2 and sys.argv[1] == "demo":
        demo()
        return
    if len(sys.argv) < 3 or sys.argv[1] != "analyze":
        print(__doc__)
        return
    report(analyze(sys.argv[2]))


if __name__ == "__main__":
    main()
