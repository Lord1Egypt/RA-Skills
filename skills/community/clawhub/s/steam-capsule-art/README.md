# steam-capsule-art

Agent skill for making **Steam store capsule images** that survive both Valve's rules and a 120×45 thumbnail.

It encodes the parts that are usually guessed wrong:

- **Exact 2024-08 asset sizes** — Valve no longer accepts the old dimensions.
- **Content red lines** effective 2022-09-01 (no review scores, awards, discount copy, calls to action, or any other text).
- **The arithmetic that kills the crop chain** — one illustration cannot be resized into every capsule, because the small capsule needs the logo at ≥85% width while the main capsule needs 60–75%. Those two are mutually exclusive.
- **Negative space must carry content** — "leave it clean and empty" produces a flat colour field. The brief has to name three or more light/edge events.
- **Thresholds from measurement, not taste** — saturation and edge-density floors taken at P25 of 20 top-selling capsules, not invented absolutes.

## Install

Drop this folder into your skills directory, or point your agent at `SKILL.md`.

## Use

```bash
python scripts/capsule_audit.py capsule.png --target 1232x706 --logo-zone left
```

```
file  capsule.png  (1232x704)
  exact size           1232x704                1232x706               FAIL
  saturation           0.398                    >= 0.360               PASS
  edge density         8.47%                    >= 4.92%               PASS
  left zone liveness   lumSD 58.9 / warm 4.37%  lumSD>=8 or warm>=0.5% PASS
  thumbnail            capsule_120x45.png
  FAIL: size 1232x704 != 1232x706
result: FAIL
```

Exit code 1 on any hard failure, so it drops straight into CI or a render gate.

## Why the numbers look odd

They are not opinions. Twenty top-selling capsules measured at a normalised 400×229:

| | median | P25 |
|---|---|---|
| saturation | 0.535 | 0.360 |
| edge density | 11.56% | 4.92% |

Nine of those twenty sit below 10% edge density — Undertale, Inscryption, Dave the Diver, Lethal Company, RimWorld, Mouthwashing, Slay the Spire, Animal Well, Celeste. Any "≥10%" rule would fail half the reference set. Full table in `references/benchmarks.md`.

**Measurement caveat:** always resize to the source aspect ratio. Squashing a 460×215 header to 200×200 inflates edge density from ~11.6% to ~15.2% and will give you a threshold that fails good work.

## Licence

MIT. See `LICENSE`.
