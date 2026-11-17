# Wedding Toast Architect

**You have 3 minutes, one microphone, and both grandmothers listening.**

Every year, millions of people are drafted into giving a wedding speech with
zero training: best men, maids of honor, parents, siblings. The failure modes
are so universal they've become clichés — the rambling inside jokes, the
accidental mention of the bride's ex, the drunk-college story told in front
of a 7-year-old flower girl, the "ball and chain" joke that lands like a
judge's gavel.

## The problem
1. **No structure.** People write by vibe, produce 800 words, and speak for
   six minutes about themselves.
2. **No editor.** The friends who'd honestly say "cut the ex mention" aren't
   in the room while you write at 1 AM.
3. **No timing sense.** 600 words feels short on paper and eternal at the
   podium (600 words ≈ 5+ minutes with adrenaline pauses).

## What this toolkit does
- `build` — turns a 6-question interview (role, couple, years known, stories,
  qualities, minutes) into a section-by-section blueprint with word budgets
  tuned by role.
- `scan` — red-flags a draft across 16 danger patterns with CUT/SOFTEN/CHECK
  verdicts, enforces protected names, checks length and readability, and
  scores the draft 0-100.
- `time` — converts words to minutes at slow/normal/fast delivery paces.

## Quick start
```bash
# 1. Blueprint a 3-minute best man toast
python3 scripts/toast_architect.py build --role best-man \
    --couple "Alex & Sam" --partner Sam --years-known 9 \
    --stories "rafting capsize; chili cook-off disaster" \
    --qualities "loyal, calm in chaos" --minutes 3

# 2. Scan your draft (after writing against the budget)
python3 scripts/toast_architect.py scan --draft draft.txt \
    --protected "Jordan" --minutes 3

# 3. Fix every CUT, decide each SOFTEN, rehearse
python3 scripts/toast_architect.py time --words 410
```

Pure Python 3 stdlib. Offline. Your draft never leaves your machine.

## Who needs this
- Wedding party members (~8M speeches/year in the US alone at ~2M weddings)
- Parents of the couple (the highest-stakes speakers in the room)
- Anyone asked to speak at an engagement party or rehearsal dinner
- Speech-writers helping others (the scanner is a tireless junior editor)

## License
MIT — see LICENSE.
