"""Do the sung phrases line up with the lyric lines at all?

Proven earlier: the isolated vocal splits into ~27 phrases at a 0.25 s silence gap,
and the song has 28 unique lyric lines. That is a suspiciously exact match, and it
means the LRC timestamps are the unreliable part: one LRC "line" can span an
instrumental break, so a window around it grabs the wrong number of notes (2 notes
for one line, 15 for the next). This prints both views side by side.
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
    print(f"clean notes: {len(notes)}", flush=True)

    # --- view A: phrase segmentation by silence
    phrases = []
    cur = [notes[0]]
    for n in notes[1:]:
        if n["start_s"] - cur[-1]["end_s"] > 0.25:
            phrases.append(cur)
            cur = [n]
        else:
            cur.append(n)
    phrases.append(cur)
    print(f"\nphrases at 0.25s gap: {len(phrases)}", flush=True)
    print(f"{'#':>3} {'start':>8} {'end':>8} {'dur':>6} {'notes':>6}")
    for i, ph in enumerate(phrases):
        s, e = ph[0]["start_s"], ph[-1]["end_s"]
        print(f"{i:>3} {s:8.2f} {e:8.2f} {e-s:6.2f} {len(ph):6d}")

    # --- view B: LRC lines and how many notes their window grabs
    lines = lst["lines"]
    print(f"\nLRC lines: {len(lines)}   unique: {len({l['zh'] for l in lines})}", flush=True)
    print(f"{'#':>3} {'t':>8} {'next':>8} {'chars':>6} {'notes@6s':>9} {'notes@next':>11}  zh")
    for ln in lines:
        t, nx = ln["t"], ln["next_t"]
        w6 = sum(1 for n in notes if t - 0.25 <= n["start_s"] < min(nx, t + 6.0))
        wn = sum(1 for n in notes if t - 0.25 <= n["start_s"] < nx)
        print(f"{ln['i']:>3} {t:8.2f} {min(nx, t+99.99):8.2f} {ln['chars']:6d} "
              f"{w6:9d} {wn:11d}  {ln['zh']}")

    # --- view C: do phrases and lines agree on count?
    print(f"\nphrases {len(phrases)} vs unique lines {len({l['zh'] for l in lines})} "
          f"vs all lines {len(lines)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
