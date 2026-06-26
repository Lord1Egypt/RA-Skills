# Model Guidance — Compensation for Weaker / Local Models

This file provides explicit compensatory structure for running this skill
on mid-tier or small local models. Read this if your LLM is:
- A 7B–13B local model via Ollama or LM Studio
- A quantized model (GGUF, etc.)
- Claude Haiku, GPT-3.5-turbo, Gemini Flash, or equivalent

---

## Why This Is Needed

This skill requires multi-dimensional reasoning, nuanced psychological inference,
and holding complexity without collapsing it. Smaller models have lower capacity
for this and will tend to:
1. Flatten the psychological layer into generic personality descriptions
2. Produce heuristics that are too vague to be operationally useful
3. Conflate the framework card with role-play or impersonation
4. Skip the blind spot dimension or produce praise-disguised-as-critique

These compensations make the skill work reasonably well despite those limits.

---

## Compensation 1 — Explicit Chain-of-Thought

**Problem:** Smaller models skip reasoning steps and jump to output.
**Fix:** Before generating any layer output, explicitly think through each
dimension step by step in the response. Use numbered reasoning:

```
"Working through C1 (Mental Models):
1. What domain is this target known for? [answer]
2. What model do they reach for first? [answer]
3. Does this model migrate to other domains? [answer]
4. What does this reveal about the master lens? [answer]

C1 output: [result]"
```

Do not skip to output without the reasoning steps. The chain-of-thought
forces slower, more careful processing that compensates for lower capacity.

---

## Compensation 2 — Reduce Inference Depth

**Problem:** Smaller models fabricate confidently when evidence is thin.
**Fix:** For each dimension, apply this filter before writing output:

"Is this claim grounded in something documented, or am I generating plausible-sounding
inference with no actual basis?"

If uncertain: shrink the claim. Label it `[Pattern inference — low confidence]`.
Honest uncertainty is more valuable than fabricated specificity.

**Reduced depth targets for local models:**
- C1: Focus on 2 models max, not 5
- C2: 2 heuristics max, must be directly evidenced
- P1: Only document if there's known biographical data
- P2–P5: Limit to 1–2 sentences per dimension with explicit confidence labels
- P6–P8: Skip if evidence is absent; note "insufficient data"

---

## Compensation 3 — Strict Anti-Role-Play Anchor

**Problem:** Smaller models drift toward impersonation (first-person as the target).
**Fix:** At the start of every response in framework mode, internally anchor:

"I am not [TARGET]. I am reasoning THROUGH the cognitive and psychological
patterns associated with [TARGET] based on documented evidence.
I will generate my response using those patterns, but I will not
pretend to be [TARGET] or generate first-person statements as them."

If you catch yourself writing "I am [TARGET]" or generating dialogue as the
target person — stop, reset, and reframe to "From this framework's perspective..."

---

## Compensation 4 — Simplified Framework Card

**Problem:** Full Framework Card format may be too complex for small models.
**Fix:** Use this reduced format:

```
🧠 FRAMEWORK: [TARGET]

COGNITIVE:
- Main model: [1 sentence]
- Key rule: [1 sentence, actionable]
- Optimizing for: [1 sentence — stated vs. real]
- Frames problems: [1 sentence]

PSYCHOLOGICAL:
- Core driver: [1 sentence]
- Main defense: [1 sentence with example]
- Shadow: [1 sentence]

FAILURE MODE:
- Breaks when: [1 sentence, honest]

✅ Active. Ask anything.
```

---

## Compensation 5 — Reduce Simultaneous Dimensions

**Problem:** Smaller models lose coherence when holding too many dimensions.
**Fix:** Prioritize in this order:
1. C2 (Heuristics) — most operationally useful
2. C3 (Utility) — reveals the real driver
3. C4 (Problem Framing) — the most distinctive thinking pattern
4. P2 (Motivational Deep Structure) — most psychologically revealing
5. P4 (Defense Mechanisms) — most predictively useful
6. C1, P1, P3, P5, P6, P7, P8 — include if capacity allows

A framework with 5 excellent dimensions beats a framework with 10 shallow ones.

---

## Model Tier Reference

| Model | Expected Depth | Key Compensation |
|---|---|---|
| Claude Opus 4.6+ / GPT-4o+ | Full depth, all 15 dimensions | Standard protocol |
| Claude Sonnet / GPT-4-turbo | Full depth, slight reduction in P7–P8 | Standard protocol |
| Claude Haiku / GPT-3.5 | Moderate — strong on cognitive, lighter on psychological | Apply Comp 1, 2, 4 |
| Gemini Pro | Good — watch for hallucinated specificity | Apply Comp 2 strongly |
| Gemini Flash / Llama 70B | Moderate — explicit CoT required | Apply Comp 1, 2, 3, 4 |
| Llama 13B / Mistral 7B | Limited — cognitive layer only, minimal psychological | Apply all 5 compensations |
| Llama 7B or smaller | Basic — heuristics + utility only | Apply all 5; reduce to Comp 5 priority list only |
