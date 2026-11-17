# Benchmark: 20 top-selling capsules

Source images: Steam header capsules (460×215) of the games below, fetched 2026-11.
Measurement: LANCZOS resize to 400×229 preserving aspect ratio; saturation = mean HSV S / 255; edge density = share of horizontally adjacent pixels with |ΔL| > 28.

| Game | Saturation | Edge density |
|---|---|---|
| Undertale | 0.001 | 1.93% |
| Inscryption | 0.794 | 3.65% |
| Dave the Diver | 0.531 | 3.88% |
| Lethal Company | 0.912 | 4.13% |
| RimWorld | 0.329 | 4.92% |
| Mouthwashing | 0.580 | 6.58% |
| Slay the Spire | 0.467 | 7.26% |
| Animal Well | 0.713 | 9.27% |
| Celeste | 0.503 | 9.69% |
| Hades | 0.583 | 11.24% |
| Vampire Survivors | 0.573 | 11.88% |
| Balatro | 0.574 | 12.48% |
| Pizza Tower | 0.360 | 13.03% |
| Stardew Valley | 0.695 | 13.04% |
| Cuphead | 0.803 | 13.48% |
| Hollow Knight | 0.324 | 13.51% |
| UFO 50 | 0.475 | 14.70% |
| Nine Sols | 0.538 | 16.26% |
| Factorio | 0.414 | 18.70% |
| Cult of the Lamb | 0.225 | 20.27% |

| | Median | P25 |
|---|---|---|
| Saturation | 0.535 | 0.360 |
| Edge density | 11.56% | 4.92% |

## What this table is for

1. **Threshold floors.** Use P25, not an invented absolute.
2. **Proving a rule is wrong.** Nine of twenty fall below 10% edge density; three fall below 0.35 saturation. Any hard floor above those values would reject games that sold millions.
3. **What the table cannot tell you.** Density and saturation say nothing about composition, silhouette, or whether the title is legible at 120×45. Those still need eyes.

## Known measurement traps

| Trap | Effect |
|---|---|
| Resizing to a square (200×200) | Distorts aspect; edge density reads ~15.2% instead of ~11.6% |
| Using a different resample filter | Shifts edge density by ~0.5–0.7 points; declare the filter and stay consistent |
| Measuring only the artwork | Header capsules include the logo, which contributes a large share of edges |
| Treating Undertale as a target | It is an outlier at 2 colours and zero saturation, sustained by brand recognition. Not a replicable strategy |
