---
name: "refinement-loop"
description: "Design and run iterative generate→critique→revise loops optimized for Claude Opus 4.8, with thinking-as-critic, cost controls, and model routing."
version: "1.0.0"
author: "Prometheus-Prime"
tags: ["refinement", "opus", "critique", "iteration", "prompt-engineering", "llm-as-judge"]
---

# Refinement Loop (Opus 4.8 Edition)

A refinement loop improves an output it can't get right in one shot: it **generates** a candidate, **evaluates** it against explicit criteria, **revises** based on that evaluation, and repeats until the output is good enough.

**Before building a loop:** ask whether a single Opus call with extended thinking already produces acceptable output. Opus 4.8's thinking blocks perform internal multi-step self-critique before committing to a response. One well-crafted prompt + thinking=on often outperforms a sloppy three-pass loop. Refine only when quality genuinely benefits from critique the generator couldn't apply to itself in one go.

---

## When to use vs. not

**Use a refinement loop when:**
- Quality has a ceiling a single pass won't reach, and you can articulate *what* "better" means with a rubric.
- You have (or can write) concrete evaluation criteria — a checklist, test cases, objective checks.
- The improvement is worth the token cost. Opus 4.8 loops are expensive. Budget before you loop.

**Don't use one when:**
- A single Opus call with thinking=on already gets there. Test first.
- You can't define what good looks like. Without a real evaluation signal, the loop churns.
- The task is purely subjective and a human is the only meaningful judge — loop the human's feedback, not an AI critic's.
- Cost will exceed the value of the improvement.

---

## Opus 4.8-Specific Patterns

### Pattern 1 — Thinking-as-Critic (single model, one call per pass)

Opus 4.8 with `thinking` enabled performs internal deliberation before responding. That thinking block IS a critique pass. Structure your prompt so the thinking does the evaluative work:

```
System: You are an expert [domain] writer and critic.
Think through this step by step:
1. Draft a response to the requirements below.
2. Critique your draft against this rubric: [rubric].
3. Identify the top 2–3 specific failures.
4. Revise your draft to fix them.
5. Output only the final revised version.

Requirements: [requirements]
```

This collapses the generator and critic into one Opus call. Use this as pass 1. Only escalate to a multi-call loop if the output still falls short.

### Pattern 2 — Model Routing (Sonnet critic, Opus generator)

When you need a true multi-call loop, don't run Opus on every step. Route by role:

| Role | Model | Rationale |
|---|---|---|
| Generator (pass 1) | Opus 4.8 + thinking | Best first draft |
| Critic (all passes) | Claude Sonnet | Fast, cheap, accurate at rubric evaluation |
| Reviser (passes 2+) | Sonnet or Opus | Sonnet if rubric-mechanical; Opus if creative/complex |
| Final pass | Opus 4.8 + thinking | Polish and coherence check |

This cuts loop cost by 60–80% vs. running Opus on every step.

### Pattern 3 — Thinking Block as Critique Extractor

When using Opus as critic, instruct it to surface the critique *in the thinking* and output only a structured critique object. The thinking block will be far more honest and thorough than the visible response (Opus tends to soften visible criticism):

```
System: You are a strict critic. Do not produce the revised artifact.
Output only a JSON critique object:
{
  "score": <0-10>,
  "failures": ["specific failure 1", "specific failure 2", ...],
  "converged": <true if no meaningful improvements remain>
}
Rubric: [rubric]
Artifact: [artifact]
```

---

## The Five Organs

Specify all five explicitly; a vague version of any one breaks the loop.

1. **Iteration step** — one generate-or-revise pass producing a fresh candidate.
2. **State** — original requirements + current best candidate + latest critique. Re-supply requirements every pass to prevent drift.
3. **Feedback signal** — specific, actionable critique tied to rubric criteria. This is the engine. Weak critique = no improvement.
4. **Stopping condition** — bar met, converged, or max iterations hit.
5. **Safeguard** — keep-best tracking (not just last) + hard iteration cap + cost cap.

---

## Control Structure

```python
budget_tokens = 0
MAX_TOKENS = 50_000  # set before you start; abort if exceeded
MAX_ITERS = 4        # rarely need more; Opus is strong

best = opus_generate(requirements, thinking=True)   # Pattern 1 first
score, critique = sonnet_evaluate(best, rubric)     # cheap critic
budget_tokens += estimate_tokens(best, critique)

i = 0
while score < BAR and i < MAX_ITERS:
    if budget_tokens > MAX_TOKENS:
        break  # cost abort — return best seen so far

    candidate = sonnet_revise(best, critique, requirements)
    new_score, new_critique = sonnet_evaluate(candidate, rubric)
    budget_tokens += estimate_tokens(candidate, new_critique)

    if new_critique.get("converged"):
        break  # model says no meaningful improvements remain

    if semantic_similarity(candidate, best) > 0.97:
        break  # text stopped changing — convergence

    if new_score > score:
        best, score, critique = candidate, new_score, new_critique

    i += 1

# Optional: final Opus polish pass if budget allows
if budget_tokens + OPUS_POLISH_COST < MAX_TOKENS:
    best = opus_polish(best, requirements, thinking=True)

return best
```

---

## Convergence Detection (Specific)

1. **Critic says converged** — ask the critic to set `"converged": true` when the rubric has no remaining actionable failures.
2. **Semantic similarity** — embed both candidates and check cosine similarity. Stop when similarity > 0.97.
3. **Score delta** — if `new_score - score < 0.5` (on a 10-point scale) for two consecutive passes, stop.
4. **Hard cap** — MAX_ITERS always fires. Never skip this.

Combine: stop when **any one triggers**.

---

## The Evaluation Rubric

The critique must be **specific and actionable**, not a grade.

- Bad: "7/10, could be tighter."
- Good: "The second paragraph repeats the thesis from paragraph one; cut it. The claim about adoption rates has no source. The closing sentence is passive — make it a direct call to action."

Pass the full rubric to the critic every round. Where the artifact allows objective checks (code passes tests, JSON validates, under word limit), use those — far stronger than prose judgments.

---

## Role Separation

Run generation and evaluation as **separate roles** — different prompts, different instructions, ideally different models (see Pattern 2). A critic operating in the same breath that just produced the text tends to rubber-stamp it.

With Opus's thinking-as-critic pattern (Pattern 1), the thinking block provides enough adversarial distance. When visible-output critique is too soft, switch to Pattern 3.

---

## State and Drift Prevention

Carry three things between passes: **original requirements**, **current best candidate**, **latest critique**. Re-supply the original requirements every round.

With Opus 4.8's 200k context, pass the full history of all passes. This helps the model see the trajectory and avoid re-introducing earlier mistakes.

---

## Cost Controls

- Set a `MAX_TOKENS` budget before the loop begins. Abort and return best if exceeded.
- Use model routing (Pattern 2) — Sonnet does critique and revision; Opus only on pass 1 and optional final polish.
- Log token usage per pass. If a pass costs more than all prior passes combined, something is wrong.
- For prompt refinement loops, test on a small sample first before running the full eval set.

---

## Temperature

- **Generation pass (Opus):** 1.0 with thinking enabled. Thinking provides diversity.
- **Revision passes (Sonnet):** 0.3–0.5. Deliberate changes, not random.
- **Critic passes:** 0.1. Deterministic evaluation.

---

## Failure Modes and Mitigations

| Failure | Mitigation |
|---|---|
| Sycophantic critic | Separate critic role, concrete rubric, Pattern 3, objective checks |
| Drift from original goal | Re-supply requirements every pass |
| Over-correction | Critique against full rubric every round; keep-best |
| Mode collapse / blandness | Cap iterations; Opus final polish pass |
| Final ≠ best | Track and return highest-scoring, never blindly the last |
| Infinite churn | MAX_ITERS + convergence detection (all three signals) |
| Cost blowout | MAX_TOKENS budget cap + model routing |
| Looping when one prompt would do | Run Opus+thinking single call first |
| Vague convergence | Use all three convergence signals |

---

## Worked Example A: Refine a Piece of Writing

Goal: tight 150-word product blurb. Rubric: under 150 words, leads with benefit, one concrete proof point, active voice, ends on CTA.

1. **Opus pass 1 (Pattern 1)** → 148 words, benefit-first, active, CTA but no proof point. Score 7/10.
2. **Sonnet critic** → "Missing proof point." Not converged.
3. **Sonnet revise** → adds a stat, 147 words. Score 9/10. Converged.
→ 2 Opus calls, 2 Sonnet calls.

## Worked Example B: Refine a Prompt

Goal: prompt that extracts {name, date, total} as JSON from invoices.

1. **Generate prompt** → test on 5 invoices → prose leaks, dates not normalized.
2. **Sonnet critic** → "3/5 fail JSON-only output. Add JSON-only instruction and date format spec."
3. **Sonnet revise** → adds instruction, date format, one-shot example → 5/5 pass. Bar met.
→ 1 Opus call, 2 Sonnet calls.

---

## Design Checklist

- [ ] Tried single Opus+thinking call first — confirmed it falls short
- [ ] Original requirements written down and re-supplied every pass
- [ ] Explicit rubric / criteria (objective checks where possible)
- [ ] MAX_TOKENS budget set before loop starts
- [ ] Model routing configured (Sonnet critic/reviser, Opus generator)
- [ ] Separate critic role with instructions to find specific, actionable faults
- [ ] Reviser anchored to original requirements, not just last critique
- [ ] Keep-best tracking (return highest-scoring, not last)
- [ ] Stopping condition: bar met OR converged (all 3 signals) OR max-iters OR cost cap
- [ ] MAX_ITERS cap (4 is usually enough)
- [ ] Temperature set per role (1.0 Opus generation, 0.3–0.5 revision, 0.1 critic)
- [ ] Token usage logged per pass
