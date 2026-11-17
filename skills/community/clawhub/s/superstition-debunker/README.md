# Superstition Debunker — Folklore Fingerprinting

**Chain messages and viral myths carry structural fingerprints — unnamed experts, forwarding quotas, "they don't want you to know." Real information doesn't.**

"Harvard doctors confirmed 90% of people... share with 10 friends
before this is taken down." This doesn't need a fact-check — its
*rhetorical structure* announces it. The skill scores claims against
a catalog of 19 folklore patterns across 6 families (authority
mimicry, urgency & suppression, unfalsifiable structure, causal
sleight of hand, numeric theater, emotional amplifiers) and
generates the exact question that would settle each claim.

## What it does

- **analyze** — score a pasted claim (or .txt file): myth-signature
  score, matched patterns with the matched text, verdict ladder
  (STRONG / MODERATE / WEAK / NONE), and per-pattern settling
  questions; `--log` records the analysis
- **list** — the full pattern catalog with weights and rationale
- **stats** — what families dominate everything you've analyzed —
  a media-diet readout (and a great teaching tool)

## Calibration

| Input | Score | Verdict |
|-------|------:|---------|
| Chain myth (Harvard + quota + energy frequencies + cousin) | 10 | STRONG |
| Dry science report (40,000-nurse cohort, adjusted) | 0 | NONE |

The tool reads rhetoric, not truth — a high score means
folklore-shaped, never "false."

## Quick start

```bash
python3 scripts/myth_analyzer.py analyze "URGENT: NASA confirmed...
forward to 10 people before it's deleted" --log
python3 scripts/myth_analyzer.py stats
```

## Why it matters

Misinformation spreads 6x faster than corrections (MIT Science, 
2018) not because people are dumb, but because myth-shaped content
is *engineered* for sharing: urgency preempts checking, suppression
framing pre-explains missing sources, and luck mechanics reward
forwarding. Teaching the patterns — not "don't believe things" — is
the intervention that actually scales.

## License

MIT © Denis Voronin
