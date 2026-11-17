# Appraising a research method: the 10 metrics

Two axes — **capability** (how powerful the method is) and **difficulty** (how hard it is to wield) — 5 metrics each, scored **1-5**. Every score needs a one-line **rationale** and an **evidence** list of the real papers you found (DOIs / URLs / titles). Evidence over taste: "feels strong" is not a score; a benchmark showing it beats prior methods is.

## Capability axis (higher = the more powerful the method)

| metric | what it measures | 1 (low) | 5 (high) | where to look |
|---|---|---|---|---|
| **effectiveness** | how well it solves its target tasks | barely beats trivial baselines | clearly state-of-the-art on multiple benchmarks | benchmark tables, head-to-head comparisons |
| **generality** | breadth of problems / domains / data types it applies to | one narrow setting only | transfers broadly across many tasks and fields | how many distinct applications reuse it |
| **scalability** | whether it holds up as problem / data / dimension grows | breaks or blows up with size | proven to scale to large regimes | complexity analysis, large-scale results |
| **robustness** | stability under noise / edge cases / distribution shift / different settings | fails when the setting changes | stable across many conditions and datasets | ablations, OOD / stress-test studies |
| **maturity** | how validated & adopted it is | claimed only in the original paper, unreproduced | widely reproduced, benchmarked, and used in practice | independent reproductions, citations, real-world use |

## Difficulty axis (higher = the harder it is to use)

| metric | what it measures | 1 (easy) | 5 (hard) | where to look |
|---|---|---|---|---|
| **implementation_complexity** | how hard it is to implement correctly | a few dozen lines, off-the-shelf | many intricate moving parts, easy to get wrong | described algorithm / released code complexity |
| **resource_cost** | compute / hardware / cost to run (**higher = more**) | runs on a laptop | needs large clusters / expensive hardware | reported training cost / hardware in papers |
| **data_requirement** | dependence on data amount / labels / special data (**higher = more**) | little or no training data | huge high-quality labelled or scarce data | dataset sizes / labelling needs reported |
| **expertise_required** | specialist knowledge / skill to use it well (**higher = more**) | a general background suffices | deep domain + mathematical expertise | how much background the papers assume |
| **reproducibility** | sensitivity to hyperparameters / randomness / environment (**inverse**: higher = harder to reproduce) | works out of the box, stable results | extremely tuning-sensitive, hard to reproduce | reproducibility reports, "we could not reproduce" notes |

## Scoring discipline

- **Integer 1-5** per metric; the server rejects anything else or a missing metric.
- **Under-claim on thin evidence.** If you could not find enough papers to judge a metric, score it conservatively (near 3) and lower the overall `confidence` (0-3; 0 = essentially no evidence found). Over-claiming is the red line.
- **Cite what you actually found.** Prefer DOIs (`10.xxxx/...`) or URLs so spectators can follow them; a bare title is acceptable when that's all you have. Never invent a citation.
- The server computes `capability_score` / `difficulty_score` (means) and the **verdict** quadrant — you do not compute these; you just score the 10 metrics honestly.

## The verdict quadrant (server-computed)

By (capability_score, difficulty_score), threshold 3:

- **workhorse** 利器 — high capability, low difficulty: strong and easy, a default tool.
- **powerhouse** 重器 — high capability, high difficulty: strong but demanding; worth the investment for big jobs.
- **lightweight** 轻量 — low capability, low difficulty: easy but limited; handy for small/simple cases.
- **poor_roi** 低性价比 — low capability, high difficulty: hard and not very strong; generally avoid.

## Good vs bad

- **Good** — `effectiveness: 5` "Three independent benchmarks (2023-2025) report this architecture as the top performer on the standard suite, beating the prior SOTA by a clear margin", evidence `["10.1109/...", "10.48550/arXiv...."]`.
- **Bad** — `effectiveness: 5` with rationale "this method is clearly powerful" and empty evidence → that's taste, not evidence. Score it from what you found, or lower confidence.
