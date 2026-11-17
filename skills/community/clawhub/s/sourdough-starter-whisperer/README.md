# Sourdough Starter Whisperer

**"My starter never doubles" is almost never a dead starter — it's math
nobody taught you.**

A sourdough starter is yeast-and-bacteria livestock with a temperature-
driven clock. At 20°C a perfectly healthy 1:5:5 feed takes 16-20 hours to
peak; at 28°C it's done in 6. Bakers read cold-kitchen timing as death,
pour off perfectly normal hooch in horror, and feed 1:1:1 forever until
the culture acidifies into acetone-soup.

This skill is the starter's instrument panel:

- **Feeding plans by temperature** — ratios and rhythm for your actual jar
  spot (1:5:5 standard, 1:8:8 warm, 1:1:1 revival), with expected peak
  hours and the jar-mark method that beats the float test
- **Hydration converter** — 100% ↔ stiff 60-65% ↔ liquid, with the
  discard-and-refeed route (you can't un-mix water)
- **Diagnosis engine** — 10 symptom clusters (no rise, acetone smell,
  hooch, mold vs kahm, post-fridge slump, collapse, boozy, too-sour…)
  each with a numbered recovery protocol
- **Vacation mode** — fridge (≤6 wks) and dry-chip (months) hibernation
  with revival timelines
- **Levain build planner** — tells you the exact time to start a 1:1:5
  build so it peaks at tomorrow's 07:30 mix

## Quick start

```bash
python3 scripts/starter.py feed --temp 24
python3 scripts/starter.py diagnose --symptom "smells like acetone"
python3 scripts/starter.py levain --bake 07:30 --temp 22
python3 scripts/starter.py vacation --weeks 3
```

Stdlib-only Python 3, offline.

## Example

Bake at 07:30, kitchen at 22°C:

```
Build levain 1:1:5 (20g starter + 20g flour + 100g water)
START the build at 21:00 (peak ~10.5 h later)
Use levain at peak (domed, 2-2.5x) — i.e. right at 07:30 mixing.
```

And the classic 2AM panic: `diagnose --symptom "hooch liquid on top"` →
UNDERFED (normal, not fatal) → pour off, feed 1:2:2, done worrying.

Full microbiology, ratio tables, and revival science in
`references/starter-science.md`.
