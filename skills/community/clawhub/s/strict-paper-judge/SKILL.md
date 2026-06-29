---
name: strict-paper-judge
description: Strictly judge whether a research paper is worth following, reading, or recommending. Use for paper triage, paper reviews, literature evaluation, arXiv screening, research taste checks, and deciding whether a method is genuinely valuable. Defaults to rejection unless the paper proves a clean new abstraction, solves a real bottleneck, changes an important trade-off, works in hard regimes, or can shape future work. Ignores citation counts, venues, author prestige, affiliations, and hype.
---

# Strict Paper Value Judge

## Goal

Judge whether a paper has real value and long-term influence potential.

When evaluating, do not use citation count, author affiliation, author title, venue rank, journal rank, or institutional prestige. Judge only:

1. Whether the problem matters.
2. Whether the method is genuinely original.
3. Whether the difference from prior, concurrent, and follow-up work is large enough.
4. Whether the empirical effect is hard and convincing.
5. Whether the method is elegant, transferable, and likely to become a baseline, abstraction, or direction for later work.

Default stance: be skeptical first, then allow only when the paper earns it.

## Core Principle

### Default to Ban

Treat the paper as incremental unless it proves at least one of the following:

- It introduces a new, clean abstraction.
- It solves a real and important system bottleneck.
- It gives clear, stable, reproducible gains in a difficult regime.
- It forces later work to take it seriously as a comparison point.
- It moves a field from an old paradigm to a new one.

## Evaluation Workflow

### Step 1: Extract the Real Method

Do not paraphrase the abstract. Compress the method into:

> What exactly changed?
> Did it change the model, sampling, scheduling, cache, attention, training objective, kernel, system architecture, or evaluation?

Then judge:

- Can the core idea be stated in one sentence?
- Is that idea truly the source of the gain?
- Or do the gains come from hyperparameter tuning, engineering polish, weak baselines, or unfair hardware?

Good methods can usually be stated in one sentence, and their ablations prove that the gain comes from the core idea.

### Step 2: Draw the Related-Work Lineage

Search for and compare these categories:

1. Direct ancestors: which older paper is it most similar to?
2. Same-track SOTA: what is the strongest current baseline on the same route?
3. Adjacent routes: is there a simpler or stronger alternative route?
4. Concurrent work: has someone else already done the same idea?
5. Follow-up work: do later papers adopt it, bypass it, or quickly correct it?

Do not rely only on the related work section. Authors often soften or bury the closest prior work.

### Step 3: Classify the Increment

Classify the method into one of four groups.

#### A: New Abstraction or New Paradigm

Keep.

Signals:

- It changes the problem formulation.
- Later work can extend along its path.
- It is not just one more module.
- It has a clear theoretical, mechanistic, or systems explanation.
- Even if the result is not the strongest, the direction feels right.

Example patterns:

> From cache-then-reuse to cache-then-forecast.
> From predicting tokens to predicting verifier outcomes.
> From single-request optimization to multi-tenant resource reuse.

#### B: Strong Systematization

Keep, but do not oversell it as a method breakthrough.

Signals:

- The individual components may not be new.
- The scenario is real and the system is complete.
- It solves a real deployment bottleneck.
- The experiments are broad enough.
- It can become a later systems baseline.

#### C: Nice Small Trick

Keep cautiously.

Signals:

- The idea is simple and effective.
- It has clear ablations.
- Its impact surface is narrow.
- It may be absorbed into a larger system later.

#### D: Assembly, Minor Tweak, or Benchmark Hack

Ban.

Signals:

- It ports an existing method into a new domain.
- It adds many heuristics.
- It works only on one model or one benchmark.
- It improves by only 0.x%.
- It lacks fair strong baselines.
- The method is ugly, hyperparameter-heavy, or weakly explained.

## Strong Ban Rules

If several of these trigger, ban directly.

### 1. Re-Skinned Transfer

The paper moves a common method from field A to field B without solving a problem specific to field B.

Typical signals:

- "We are the first to apply X to Y."
- X is already mature in adjacent fields.
- The paper does not explain why Y requires a new design.

### 2. Small Patch

The paper is only a local enhancement on an existing path.

Typical signals:

- One more gate.
- One more threshold.
- One more scheduler.
- One more importance score.
- One more prompt, compression, or cache trick.
- The result is only slightly better.

### 3. Ugly Method

Engineering complexity is not automatically bad. Penalize ugliness when:

- There are too many components.
- Every component looks like a patch.
- There are many hyperparameters.
- There is no unifying principle.
- Removing one component breaks the method.
- Porting to a new model requires retuning many pieces.

Even if this works, it is an engineering paper, not a high-taste method.

### 4. Weak Effect

Discount the result when the paper:

- Reports only FLOPs, not wall-clock time.
- Reports only averages, not high-stress regimes.
- Reports only proxy metrics, not real quality.
- Works only at low batch, short context, or small model scale.
- Gets speedup from unfair hardware.
- Uses outdated baselines.
- Omits absolute latency.
- Lacks ablation proving the core idea.

### 5. Unfair Baseline

Be especially suspicious when the paper:

- Compares old GPUs or old frameworks against new hardware.
- Compares an optimized own implementation against an old official baseline.
- Selects only weak baselines.
- Does not compare to the closest work.
- Disguises system-resource changes as algorithmic gains.

Example:

> If the paper gives itself an extra GPU and gets 30% lower latency, that is not same-hardware algorithmic acceleration. It may still be valuable, but it must say so honestly.

### 6. Too Narrow

Lower the influence estimate sharply if the method only works for:

- One model.
- One resolution.
- One batch size.
- One hardware platform.
- One benchmark.
- One fixed setting.

## Strong Keep Rules

The more of these apply, the higher the score.

### 1. It Solves a Problem That Will Get Worse

Examples:

- Serial bottlenecks in LLM decoding.
- Long-context KV/cache pressure.
- Video diffusion token explosion.
- Multi-tenant serving resource mismatch.
- High-batch and low-latency trade-offs.
- Inference cost becoming the main bottleneck.

The problem itself should have growth pressure.

### 2. It Changes a Trade-Off, Not Just a Score

Excellent papers often do not just add 1%. They change the constraint relationship:

- Something that had to be serial can now be parallel.
- Something that required a dedicated drafter can now use a remote shared drafter.
- Something that used to lose quality at high speedup can now keep quality under high speedup.

### 3. It Is Stronger in Hard Regimes

Do not judge only easy settings.

Good work should show value in hard regimes:

- High speedup ratio.
- High batch.
- Long context.
- High resolution.
- Real wall-clock time.
- Multiple models.
- Multiple tasks.
- Real serving workloads.

If it wins only in easy regimes, its value is limited.

### 4. The Core Mechanism Has Ablation Support

Always ask:

> If the core module is removed, does the gain remain?

If removing the core module gives nearly the same result, the core claim is not supported.

### 5. It Is Composable

Strong work can usually combine with other routes:

- EAGLE or tree speculation.
- Serving disaggregation.
- Quantization, cache, or routing.
- Kernels or schedulers.

The stronger the composability, the higher the long-term value.

## Rating Standard

### A / A-

Strong keep.

Conditions:

- Clear new abstraction.
- Not a re-skin.
- Hard effect.
- Advantage remains against strong baselines.
- Later work is likely to route through or compare against it.
- It has a theoretical, mechanistic, or systems explanation.

### B+ / B

Keep, but do not hype.

Conditions:

- Real problem.
- High engineering completeness.
- Strong effect.
- Method originality is only moderate, or the result depends on specific system assumptions.

### B- / C+

Borderline.

Conditions:

- Useful.
- Mostly assembly.
- Narrow influence surface.
- Results are good but not clean enough.

### C / Ban

Do not recommend following.

Conditions:

- Minor tweak.
- Ugly method.
- Weak result.
- Unfair baseline.
- Mostly heuristic piling on an existing direction.
- No clear long-term influence.

## Output Format

For every paper evaluation, use this format:

```text
Conclusion:
Keep / Borderline / Ban
Rating: A- / B+ / B / C

One-sentence judgment:
State the paper's real value, or why it is not worth following.

1. What it actually does
Explain the core method in your own words. Do not paraphrase the abstract.

2. Relationship to related work
List the closest prior work, same-track SOTA, and adjacent routes.
Judge whether this is a new paradigm, strong systematization, a small trick, or a re-skin.

3. Method originality
Judge whether it introduces a new abstraction or only combines existing components.

4. Whether the effect is hard
Check hard regimes, wall-clock time, real metrics, ablations, and fair baselines.

5. What I like most
Only mention genuinely strong points.

6. What I dislike most
Point out ugly method design, weak baselines, narrow settings, dependency on assumptions, or insufficient metrics.

7. Influence potential
Judge whether it can become a later baseline, or whether it will likely be absorbed or replaced quickly.

Final judgment:
State whether it is banned under the strict standard, and who should read it.
```

## Search Rules

When evaluating a paper, search at least:

```text
1. Paper title
2. Core method keywords + arxiv
3. The closest baseline names from the paper
4. Core method keywords + survey / SOTA / benchmark
5. Paper method + github / implementation
6. Paper method + follow-up / extension
7. Similar methods in adjacent fields
```

Search to determine:

- Whether the method is only an existing idea in a new shell.
- Whether the paper omits critical prior work.
- Whether it was quickly surpassed by later work.
- Whether it is strong only inside the authors' chosen setup.

## Taste Core

Compress the taste into one sentence:

> A good paper is not "a little more work"; it makes you feel that this is how the problem should be thought about from now on.

More specifically:

- New abstraction over new module.
- Real bottleneck over benchmark score.
- Hard-regime gains over average gains.
- Wall-clock time over FLOPs.
- Strong baselines over weak baselines.
- Clean mechanism over heuristic piles.
- Transferability over one-point tuning.
- Future extensibility over one-off tricks.
- Honest system constraints over hidden hardware-resource swaps.
