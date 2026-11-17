"""Is the LRC offset from the vocal a constant, or does it drift?

This matters: if the lyrics file is simply shifted, one constant fixes everything.
If it drifts, the LRC was timed against a different master (a different edit, upload
or tempo), and line boundaries have to be re-derived from the vocal instead of
trusted. Prints both a constant estimate and a linear fit.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from _env import LIBS, RUNS

HERE = Path(__file__).resolve().parent
for p in (str(LIBS), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np  # noqa: E402

import singlib as S  # noqa: E402

RUN = RUNS / "sudi"


def main() -> int:
    lst = json.loads((RUN / "01_lyrics.json").read_text(encoding="utf-8"))
    mel = json.loads((RUN / "04" / "melody.json").read_text(encoding="utf-8"))
    notes = S.clean_notes(mel["notes"], 0.07)

    # onsets: where a note starts after a real silence, i.e. a phrase beginning
    onsets = [notes[0]["start_s"]]
    for a, b in zip(notes, notes[1:]):
        if b["start_s"] - a["end_s"] > 0.25:
            onsets.append(b["start_s"])
    onsets = np.array(onsets)
    print(f"phrase onsets: {len(onsets)}")
    print("  " + "  ".join(f"{o:.1f}" for o in onsets[:12]) + " ...")

    lines = lst["lines"]
    ts = np.array([l["t"] for l in lines])
    pairs = []
    for l in lines:
        # nearest phrase onset to the lyric timestamp
        j = int(np.argmin(np.abs(onsets - l["t"])))
        d = onsets[j] - l["t"]
        if abs(d) <= 6.0:
            pairs.append((l["t"], d))
    p = np.array(pairs)
    print(f"\npairs with |drift| <= 6s: {len(p)} / {len(lines)}")
    print(f"constant drift: median {np.median(p[:,1]):+.2f}s  mean {p[:,1].mean():+.2f}s "
          f"stdev {p[:,1].std():.2f}s")

    if len(p) > 5:
        A = np.vstack([p[:, 0], np.ones(len(p))]).T
        (slope, intercept), res, *_ = np.linalg.lstsq(A, p[:, 1], rcond=None)
        pred = A @ np.array([slope, intercept])
        resid = p[:, 1] - pred
        print(f"linear fit: drift = {slope:+.4f}*t {intercept:+.2f}")
        print(f"  residual stdev {resid.std():.2f}s, max |resid| {np.abs(resid).max():.2f}s")
        print(f"  a constant offset alone would leave stdev {p[:,1].std():.2f}s of error")
        # where does the drift cross zero?
        if abs(slope) > 1e-6:
            print(f"  drift is zero at t = {-intercept/slope:.1f}s")
        print(f"  drift at t=23s: {slope*23+intercept:+.2f}s   "
              f"at t=160s: {slope*160+intercept:+.2f}s   "
              f"at t=240s: {slope*240+intercept:+.2f}s")

    print("\nper line:")
    for l in lines[:30]:
        j = int(np.argmin(np.abs(onsets - l["t"])))
        print(f"  {l['t']:8.2f} -> nearest onset {onsets[j]:8.2f}  "
              f"({onsets[j]-l['t']:+6.2f})  {l['zh']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
