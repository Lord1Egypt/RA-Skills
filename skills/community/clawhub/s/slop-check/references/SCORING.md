# SCORING.md — how the Slop Percentage is computed

One number, seven categories, no vibes-only deductions.

## Categories and weights

| Category | Weight | Scored by | Source |
|---|---|---|---|
| Architecture & Modularity | 25% | Judgment (taste pass) | HEURISTICS.md |
| Coupling & Dependencies | 15% | Script | `metrics.json → subscores.coupling` |
| Duplication | 15% | Script | `metrics.json → subscores.duplication` |
| AI Tells & Comment Slop | 15% | Script ± your 15-pt adjustment | `metrics.json → subscores.aiTells` |
| Naming & Domain Language | 10% | Judgment (taste pass) | HEURISTICS.md |
| Consistency | 10% | Judgment (taste pass) | HEURISTICS.md |
| Dead Weight | 10% | Script | `metrics.json → subscores.deadWeight` |

Each category subscore is 0–100 where **0 = pristine, 100 = maximum slop**.

```
slopPercent = round( Σ (weight × subscore) / 100 )
```

## Scoring the judgment categories

Subscore = sum of finding points in that category, clamped to 0–100.
Finding points: minor 1–3, moderate 4–7, major 8–12.

Calibration anchors so different runs land in the same place:

- **0–15** — You went looking for problems and mostly failed to find them.
- **16–35** — Real smells exist but the structure is sound. A reviewer would request changes, not rewrite.
- **36–60** — Smells are the norm rather than the exception in the sampled files.
- **61–85** — The category's failure mode is the codebase's defining characteristic.
- **86–100** — Reserved. You should be able to defend this score to the code's author, in person.

Small-project fairness: a flat 200-line script does not lose Architecture points for
having no layers — it loses points only for problems it *actually has at its size*.
What never gets a size discount: naming, duplication, AI tells, consistency.

## Tier bands

| Slop % | Tier | Badge blurb |
|---|---|---|
| 0–10% | **Senior Engineer** | A real, competent human clearly cared about this. |
| 11–25% | **Mid-Level Engineer** | Genuinely fine. Also, slightly mid. |
| 26–45% | **Advanced Vibe Coder** | AI-assisted, but you know what good looks like. |
| 46–65% | **Somehow, It Works** | It runs. Don't ask how. |
| 66–85% | **Zoned-Out Vibe Coder** | You were on your phone for at least three of these files. |
| 86–100% | **GPT-3.5, Unsupervised** | Nobody read anything. Ever. |

**Easter egg:** slopPercent ≤ 3 additionally awards the **🏆 Cracked 10x Engineer** badge
(set `tier.easterEgg = true` in the report data). It should be rare enough to brag about.

## Verdict copy guidelines

- One short paragraph. Deadpan, specific, quotable. Roast the code, never the coder.
- It must contain the single most damning (or most impressive) concrete fact you found —
  "four utils folders," "a 1,400-line index.ts," "zero circular dependencies in 300 files."
- High scores deserve real praise with the same specificity as the roasts.
- The "fastest tier climb" line names ONE fix and the approximate slop points it's worth
  (weight × subscore reduction ÷ 100). Be honest about the math.
