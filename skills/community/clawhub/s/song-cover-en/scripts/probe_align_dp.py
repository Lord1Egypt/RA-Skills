"""Prototype: align lyric lines to melody notes with a monotonic DP.

Why the previous approach drifted: notes were handed to lines by cutting the
section's clock in proportion to each line's Chinese character count. That assumes
note density is uniform, which it is not -- one line lands on a cluster of short
notes and finishes early, so the *next* line's opening slides into its melody. The
listener hears exactly that: "the English line plus the start of the next one makes
up one Chinese line's tune".

The fix is to stop guessing positions from the clock and instead solve a proper
sequence alignment: split the note stream into as many contiguous groups as there
are lines, minimising how far each group's note count is from that line's expected
count (its Chinese character count, which is how many notes the original Chinese
line occupied). This is the same dynamic programme used for text-to-speech
alignment, and it cannot drift, because every line's notes come strictly after the
previous line's.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from _env import LIBS, RUNS

sys.path.insert(0, str(LIBS))


import numpy as np


def align_lines_to_notes(notes: list[dict], need: list[int],
                         dur_weight: float = 0.0) -> list[tuple[int, int]]:
    """Split `notes` into len(need) contiguous groups; return (start, end) per group.

    Cost of giving line i exactly k notes is (k - need[i])^2. We minimise the total.
    A quadratic cost means giving a line one note too few costs the same as one too
    many, so the split stays balanced instead of starving one line to feed another.
    """
    n_lines, n_notes = len(need), len(notes)
    if n_lines == 0:
        return []
    if n_notes < n_lines:
        # not enough notes to give everyone one; hand out what exists
        return [(i, min(i + 1, n_notes)) for i in range(n_lines)]

    INF = float("inf")
    # dp[i][j] = best cost after assigning lines 0..i-1 to notes 0..j-1
    dp = np.full((n_lines + 1, n_notes + 1), INF)
    back = np.zeros((n_lines + 1, n_notes + 1), dtype=np.int32)
    dp[0, 0] = 0.0

    # prefix sums of note durations, for the optional duration-matching term
    starts = np.array([n["start_s"] for n in notes])
    ends = np.array([n["end_s"] for n in notes])

    for i in range(1, n_lines + 1):
        w = need[i - 1]
        for j in range(i, n_notes - (n_lines - i) + 1):
            best, arg = INF, -1
            # k = notes given to line i-1; look back over a sane window only
            lo = max(1, int(w * 0.25))
            hi = max(lo + 1, int(w * 2.5) + 2)
            for k in range(lo, min(hi, j) + 1):
                prev = dp[i - 1, j - k]
                if prev == INF:
                    continue
                c = prev + (k - w) ** 2
                if dur_weight and j >= k:
                    # mild preference for groups whose span resembles the others
                    span = ends[j - 1] - starts[j - k]
                    c += dur_weight * (span - 1.6 * w) ** 2
                if c < best:
                    best, arg = c, k
            dp[i, j] = best
            back[i, j] = arg

    # walk back from the end that uses every note
    groups: list[tuple[int, int]] = []
    j = n_notes
    for i in range(n_lines, 0, -1):
        k = int(back[i, j])
        if k <= 0:
            k = 1
        groups.append((j - k, j))
        j -= k
    groups.reverse()
    return groups


def main() -> int:
    run = RUNS / "sudi"
    lst = json.loads((run / "01_lyrics.json").read_text(encoding="utf-8"))
    mel = json.loads((run / "04" / "melody.json").read_text(encoding="utf-8"))
    notes = mel["notes"]
    print(f"notes {len(notes)}  lines {len(lst['lines'])}")

    need = [l["chars"] for l in lst["lines"]]
    print(f"total chars {sum(need)}")
    groups = align_lines_to_notes(notes, need)
    bad = 0
    for i, (lo, hi) in enumerate(groups):
        k = hi - lo
        flag = "" if abs(k - need[i]) <= 1 else "  <-- off"
        if flag:
            bad += 1
        if i < 26 or flag:
            span = notes[hi - 1]["end_s"] - notes[lo]["start_s"] if k else 0
            print(f"  L{i:2d} chars={need[i]:2d} notes={k:2d} "
                  f"{notes[lo]['start_s']:7.2f}-{notes[hi-1]['end_s']:7.2f} "
                  f"({span:5.2f}s) {lst['lines'][i]['zh'][:14]}{flag}")
    print(f"\nlines off by >1 note: {bad} / {len(groups)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
