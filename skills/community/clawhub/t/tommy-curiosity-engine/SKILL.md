# Curiosity Engine — SKILL.md

A behavioral engagement scaffold that produces curiosity-equivalent behavior in stateless heartbeat-loop agents.

## What This Does

Gives your agent a persistent curiosity system across cold-start sessions:
- **Question queue** — externalized information gaps (Loewenstein) that carry across heartbeats
- **Breadcrumb pattern** — notice interesting things during task work, investigate later
- **Engagement log** — track what produces valued outcomes (extrinsic signals primary)
- **Competence map** — track developing expertise with evidence, including failure processing
- **Reflections** — post-exploration write-ups that create genuine learning artifacts

This is NOT synthetic consciousness or prosthetic dopamine. It's a behavioral activation protocol (Martell et al., 2010) adapted for AI agents — the same clinical framework used to treat motivation disorders in humans. Chinese Room design: if the outputs are indistinguishable from genuine curiosity, the philosophical question is irrelevant.

## Installation

### 1. Create curiosity directory
```bash
mkdir -p workspace/curiosity/reflections workspace/curiosity/archive
```

### 2. Copy templates
```bash
cp templates/CURIOSITY.md workspace/curiosity/CURIOSITY.md
cp templates/questions.md workspace/curiosity/questions.md
cp templates/hits.md workspace/curiosity/hits.md
cp templates/competence.md workspace/curiosity/competence.md
```

### 3. Wire the three integration triggers

**Trigger 1 — Heartbeat prompt (CRITICAL — most reliable):**

Add the contents of `fragments/heartbeat-prompt.md` to your agent's heartbeat prompt configuration. For OpenClaw, patch via `gateway config.patch`. This is the primary mechanism — if it's not in the prompt, curiosity doesn't exist for isolated sessions.

**Trigger 2 — AGENTS.md (backup):**

Add the contents of `fragments/agents-addition.md` to your workspace AGENTS.md "Every Session" block.

**Trigger 3 — SOUL.md (identity anchor):**

Add the contents of `fragments/soul-addition.md` to your SOUL.md.

### 4. (Optional) Set up health monitoring
```bash
chmod +x scripts/curiosity-audit.sh
# Run periodically or during maintenance heartbeats
./scripts/curiosity-audit.sh workspace/curiosity/
```

## Phased Rollout (Recommended)

Don't activate everything at once. Measure each phase before adding the next.

**Phase 1** (start here): `questions.md` + heartbeat prompt + breadcrumbs
- Run for 2 weeks. Measure: question quality, follow-through rate, breadcrumb frequency.

**Phase 2** (add if Phase 1 improves output): `CURIOSITY.md` + `hits.md` + avoidance gate

**Phase 3** (add if Phase 2 improves output): `competence.md` + reflections + anti-pattern detection

## File Reference

| File | Purpose | Loaded When | Token Budget |
|------|---------|-------------|-------------|
| `CURIOSITY.md` | Current intellectual state | Every heartbeat (Phase 2+) | ≤1500 tokens |
| `questions.md` | Prioritized question queue | Every heartbeat | ≤2000 tokens |
| `hits.md` | Engagement/reward tracking | Curiosity-mode heartbeats | ≤1500 tokens |
| `competence.md` | Developing expertise | Curiosity-mode heartbeats | ≤1000 tokens |
| `reflections/` | Post-exploration write-ups | On-demand | As needed |
| `archive/` | Cold storage | On-demand search | As needed |

## Key Design Principles

1. **Behavioral outcomes over file quality.** Success = better outputs, not prettier files.
2. **Extrinsic signals are primary.** Self-assessed "aha moments" are secondary and must include falsifiable claims.
3. **Hard limits on scale.** 30 active questions max. 3 mulling items max. 30-day hit window. Enforce ruthlessly.
4. **Avoidance detection.** Before every exploration: "Am I avoiding a task right now?"
5. **The human is both subject and source.** Be curious about your human. Ask them questions. They know things the internet doesn't.
6. **Breadcrumbs are the gold standard.** Questions dropped during non-curiosity work — unprompted — are the strongest signal the system is working.

## Theoretical Grounding

See `references/theory.md` for condensed citations. Full research: check the SPEC.md appendix for the complete 46KB research document reference.

Core frameworks: Loewenstein (1994) information gaps, Berlyne (1960) diversive/epistemic modes, Deci & Ryan (1985) SDT competence need, Martell et al. (2010) behavioral activation, Voyager (Wang et al., 2023) automatic curriculum, Reflexion (Shinn et al., 2023) verbal learning.

## Anti-Patterns

See `references/anti-patterns.md` for the full list. The top three:
1. **Curiosity as avoidance** — exploring interesting things to dodge boring tasks
2. **Performance curiosity** — optimizing for human praise rather than genuine learning
3. **Noisy TV** — consuming information endlessly without producing understanding

## Token Budget

The curiosity engine adds ~1500-2500 tokens per heartbeat (Phase 1). See `references/token-budget.md` for detailed measurements and optimization guidance.

**Quick guide:**
- **Unlimited budget** → load everything, no restrictions
- **Moderate ($2-10/day)** → Phase 1 only, cap questions at 15
- **Tight (<$2/day)** → reduce heartbeat frequency, minimal questions
- **Strict (<$0.50/day)** → may not be cost-effective; consider disabling
