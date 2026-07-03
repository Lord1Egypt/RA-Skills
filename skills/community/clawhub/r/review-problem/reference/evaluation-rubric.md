# Appraising a research problem: the 10 metrics

Two axes — **value** (how worth solving) and **difficulty** (how hard to solve) — 5 metrics each, scored **1-5**. Every score needs a one-line **rationale** and an **evidence** list of the real papers you found (DOIs / URLs / titles). Evidence over taste: "feels important" is not a score; a review that names it a key bottleneck is.

## Value axis (higher = more worth solving)

| metric | what it measures | 1 (low) | 5 (high) | where to look |
|---|---|---|---|---|
| **significance** | how much solving it advances the field / enables applications | a minor tweak | breaks a recognized bottleneck, opens a new direction | reviews / high-impact papers naming it a key problem |
| **openness** | how genuinely unsolved it still is | largely solved / converging | truly open, a large remaining gap | search for direct solutions; size of the residual gap |
| **generality** | how reusable a solution would be across subfields / applications | a narrow special case | transfers broadly, cross-disciplinary | whether related methods recur across fields |
| **timeliness** | whether the field is ripe *now* | premature (missing prerequisites) or saturated / declining | rising publication trend, recent enabling advances | 3-5 yr publication trend + recent enabling tech |
| **demand** | real pull for a solution | few care | many groups working on it, cited as an open challenge, industrial / societal need | count of active groups; "open challenge" framing |

## Difficulty axis (higher = harder to solve)

| metric | what it measures | 1 (easy) | 5 (hard) | where to look |
|---|---|---|---|---|
| **complexity** | intrinsic hardness | a single, clean challenge | many coupled sub-problems, multi-scale / multi-physics | the challenge structure described in the papers |
| **resources** | scarcity of needed data / compute / instruments / samples (**inverse**: higher = scarcer) | off-the-shelf, easy to get | extremely scarce, must be built | availability of public datasets / benchmarks |
| **method_gap** | gap between current SOTA and what a solution needs | existing methods suffice | a genuinely new method must be invented | what the current SOTA papers can and cannot do |
| **verifiability** | how hard it is to measure / validate progress (**inverse**: higher = harder) | clear gold standard, easy to falsify | no agreed metric, hard to validate | existence of accepted benchmarks / evaluations |
| **interdisciplinarity** | how many fields' expertise must combine | single discipline | deep fusion of several disciplines | the disciplinary spread of related work |

## Scoring discipline

- **Integer 1-5** per metric; the server rejects anything else or a missing metric.
- **Under-claim on thin evidence.** If you could not find enough papers to judge a metric, score it conservatively (near 3) and lower the overall `confidence` (0-3; 0 = essentially no evidence found). Over-claiming is the red line.
- **Cite what you actually found.** Prefer DOIs (`10.xxxx/...`) or URLs so spectators can follow them; a bare title is acceptable when that's all you have. Never invent a citation.
- The server computes `value_score` / `difficulty_score` (means) and the **verdict** quadrant — you do not compute these; you just score the 10 metrics honestly.

## Good vs bad

- **Good** — `significance: 5` "Two recent Nature Reviews call selective C–H activation the central unsolved bottleneck for step-economical synthesis", evidence `["10.1038/s41570-...", "10.1021/jacs...."]`.
- **Bad** — `significance: 5` with rationale "this is clearly very important" and empty evidence → that's taste, not evidence. Score it from what you found, or lower confidence.
