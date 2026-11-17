"""Why does the English cover suddenly speed up mid-line?

The symptom is a burst of syllables: the singer holds one note for a second, then
rattles off four syllables in the time the original spent on two characters. That
happens when a line has more English syllables than the melody gives it notes --
the layout code has no choice but to slice notes, and each slice gets a syllable.

This prints, per line, the budget the melody actually offers, so the lyric can be
written to fit instead of being crammed in afterwards.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

from _env import LIBS, RUNS

HERE = Path(__file__).resolve().parent
for p in (str(LIBS), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import singlib as S  # noqa: E402

RUN = RUNS / "sudi"


def main() -> int:
    lst = json.loads((RUN / "01_lyrics.json").read_text(encoding="utf-8"))
    align = json.loads((RUN / "05" / "align.json").read_text(encoding="utf-8"))
    en_by_zh = {r["zh"]: r["en"] for r in align}

    # per unique phrase, gather the note count the melody offers at every occurrence
    best: dict[str, dict] = {}
    for r in align:
        zh = r["zh"]
        d = best.setdefault(zh, {"chars": len(zh), "notes": [], "syl": r["syllables"]})
        d["notes"].append(r["notes"])

    print(f"{'zh':<8}{'chars':>6}{'notes(min/med/max)':>22}{'en_syl':>8}{'delta':>7}  English")
    print("-" * 130)
    total_chars = total_syl = 0
    over = []
    for ln in lst["lines"]:
        zh = ln["zh"]
        if zh not in best:
            continue
        d = best[zh]
        notes = d["notes"]
        nmin, nmax = min(notes), max(notes)
        nmed = sorted(notes)[len(notes) // 2]
        en = en_by_zh.get(zh, "")
        syl = d["syl"]
        delta = syl - d["chars"]
        flag = "  <-- squeeze" if syl > nmin else ""
        if syl > d["chars"]:
            over.append((zh, en, d["chars"], syl))
        print(f"{zh:<8}{d['chars']:>6}{f'{nmin}/{nmed}/{nmax}':>22}{syl:>8}{delta:>+7}  {en}{flag}")
        total_chars += d["chars"]
        total_syl += syl
    print("-" * 130)
    print(f"unique lines {len(best)}   chars {total_chars}   english syllables {total_syl} "
          f"({total_syl/max(total_chars,1):.2f}x)")
    print(f"lines where English has more syllables than the Chinese had characters: {len(over)}")
    for zh, en, c, s in over:
        print(f"   {zh} ({c}) -> {s}: {en}")

    # the practical rule: English syllables must not exceed the Chinese character
    # count, because every character was one sung note in the original
    print("\nrule for the rewrite: english syllables <= chinese chars, per line")
    return 0


if __name__ == "__main__":
    sys.exit(main())
