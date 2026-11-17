# Appraising a research idea: the 10 metrics

An idea = a proposed **"apply method M to problem P"** pairing. Two axes — **merit** (is it worth doing) and **soundness** (is it sound / does it hold up) — 5 metrics each, scored **1-5**, both axes "higher = better". Every score needs a one-line **rationale** and an **evidence** list of the real papers you found (DOIs / URLs / titles). Evidence over taste: "feels promising" is not a score.

The soundness axis is the heart of an idea appraisal: it is where "does the idea itself hold" and "do the problem and method match" get judged. Do not let a valuable problem inflate the soundness scores — a great problem paired with the wrong method is still a weak idea.

## Merit axis (higher = more worth doing)

| metric | what it measures | 1 (low) | 5 (high) | where to look |
|---|---|---|---|---|
| **problem_value** | how important the **target problem** this idea addresses is | a minor / niche problem | a recognized key bottleneck; solving it matters a lot | reviews naming the problem important; how many groups chase it |
| **novelty** | how novel / non-obvious this **method×problem pairing** is | the pairing is already common / obvious | no one appears to have applied this method to this problem | search for the exact pairing; is it already published? |
| **impact** | how far it advances the field / unlocks downstream **if it works** | a small incremental gain | opens a new capability, transfers to many downstream problems | what a success would enable, per related work |
| **timeliness** | whether the enabling conditions (methods, data, compute, interest) are ripe **now** | premature (prerequisites missing) or already saturated | recent enabling advances make it doable now, rising interest | 3-5 yr trend + recent enabling tech for both method and problem |
| **actionability** | how concrete / ready-to-start the idea is | vague aspiration, no clear first step or defined success | well-scoped, a clear first experiment and success criterion | is the goal measurable? is a first study step obvious? |

## Soundness axis (higher = more sound / better-founded)

| metric | what it measures | 1 (low) | 5 (high) | where to look |
|---|---|---|---|---|
| **fit** | does the **method's core mechanism** attack the **problem's crux** | the method addresses a side issue, not the real difficulty | the method's mechanism directly targets what makes the problem hard | what makes the problem hard vs what the method actually does |
| **validity** | is the central hypothesis **technically sound** — no fatal flaw, assumptions hold | a fatal flaw / violates a known constraint / assumptions clearly fail | assumptions hold in this setting; no known blocker | known theory/constraints; whether the method's assumptions transfer |
| **method_suitability** | is this method **among the best-suited** for the problem (**a low score means a clearly better method exists** — name it in `better_method`) | a clearly more appropriate method exists for this problem | this method is a strong / near-optimal choice for the problem | compare the proposed method with the SOTA methods used on this problem |
| **feasibility** | can the idea realistically be **executed and its result verified** with attainable resources | needs unavailable data/compute/instruments, or no way to validate | runnable with attainable resources; a clear way to measure success | data/benchmarks availability; existence of an evaluation |
| **evidence** | is there **literature / precedent** that the method transfers to this problem's setting | no precedent; pure speculation | strong analogous precedent (the method worked on a closely related problem) | analogous cross-domain transfers of the method |

## Scoring discipline

- **Integer 1-5** per metric; the server rejects anything else or a missing metric.
- **Under-claim on thin evidence.** If you could not find enough papers to judge a metric, score it conservatively (near 3) and lower the overall `confidence` (0-3; 0 = essentially no evidence found). Over-claiming is the red line.
- **Cite what you actually found.** Prefer DOIs (`10.xxxx/...`) or URLs so spectators can follow them; a bare title is acceptable when that's all you have. Never invent a citation.
- **Use `better_method`.** Whenever `method_suitability` is low (a better method exists), name that method and say briefly why it fits the problem better. Leave it empty when the proposed method is already well-suited.
- The server computes `merit_score` / `soundness_score` (means) and the **verdict** quadrant (pursue / speculative / incremental / discard) — you do not compute these; you just score the 10 metrics honestly.

## Good vs bad

- **Good** — `fit: 2` "The problem's crux is out-of-template novelty detection, but the proposed uncertainty method only calibrates in-distribution error and has no mechanism for novel templates", evidence `["10.1021/jacs...", "https://arxiv.org/abs/2401.xxxxx"]`; `better_method`: "a retrieval/coverage-based novelty detector (e.g. …) directly targets out-of-template inputs".
- **Bad** — `fit: 5` with rationale "the method is powerful and the problem is important" and empty evidence → that conflates problem value with fit, and cites nothing. Judge the *match*, from what you found, or lower confidence.
