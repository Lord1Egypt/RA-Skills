---
name: skillprobe
description: >
  A/B evaluates any AI agent skill's real impact through three-role isolation
  (orchestrator + two sub-agents). Generates skill profiles, synthetic test
  tasks, runs baseline vs with-skill comparison, performs attribution analysis,
  and produces structured reports. Use when deciding whether to install a skill,
  comparing skill versions, investigating performance changes after adding a
  skill, optimizing an existing skill, or building a skill quality leaderboard.
homepage: https://clawhub.ai/LuarAssassin/skillprobe
metadata:
  clawdbot:
    emoji: "🔬"
    files: ["scripts/*"]
---

# SkillProbe

A/B evaluate whether a skill actually helps, or just adds complexity.

Runs inside the current agent runtime (Cursor, OpenClaw, ClaudeCode). No extra API key required.

## 7-Step Workflow

Copy this checklist and track progress:

```
Evaluation Progress:
- [ ] Step 1: Profile the skill (read SKILL.md, extract domain/triggers/boundaries)
- [ ] Step 2: Design eval plan (task categories, count, difficulty mix)
- [ ] Step 3: Generate test tasks (normal + boundary + adversarial)
- [ ] Step 4: Dispatch baseline to Sub-Agent A (no skill content!)
- [ ] Step 5: Dispatch with-skill to Sub-Agent B (include full skill)
- [ ] Step 6: Score both runs (rule + result + optional LLM judge)
- [ ] Step 7: Attribute differences and generate report
```

**Steps 1-3 and 6-7**: You (orchestrator) do these.
**Steps 4-5**: Dispatch to isolated sub-agents. NEVER execute tasks yourself.

### Steps 1-3: Prepare (Orchestrator)

1. **Profile**: Read the target skill's SKILL.md. Extract problem domain, trigger conditions, capabilities, boundaries.
2. **Design plan**: Choose task categories (QA, retrieval, coding, analysis, etc.), count, difficulty distribution (easy 30% / medium 40% / hard 20% / edge 10%).
3. **Generate tasks**: Create diverse, self-contained test prompts. Do NOT mention the skill name or A/B experiment in task prompts.

### Steps 4-5: Dispatch (Three-Role Isolation)

Create two **separate** sub-agent sessions. See [DISPATCH_PROTOCOL.md](DISPATCH_PROTOCOL.md) for exact prompt templates and constraints.

Key rules:
- Sub-Agent A (baseline): receives ONLY task prompts, zero skill content
- Sub-Agent B (with-skill): receives task prompts + full skill content
- Different `session_id` for each sub-agent
- Orchestrator never answers any test task

### Steps 6-7: Score and Report (Orchestrator)

Collect outputs from both sub-agents. Score across 6 dimensions (100-point scale). See [SCORING_REFERENCE.md](SCORING_REFERENCE.md) for scoring layers, dimension weights, thresholds, and output format.

## Principles

1. **Three-role isolation**: Orchestrator designs and scores. Sub-agents execute. Never mix.
2. **Real execution only**: No hypothetical or simulated outputs.
3. **Evidence-backed scoring**: Rules and results first; LLM judge optional.
4. **Attribution over numbers**: Explain WHY, not just how much.
5. **Finish before claiming uncertainty**: `Inconclusive` only after real attempted execution.

## Standalone CLI (Optional)

For local runs outside an agent:

```bash
skillprobe evaluate <skill-path> --tasks 30 --repeats 2 --db outputs/evaluations.db
```

Add `--llm-judge [--judge-model <model>]` for pairwise judge scoring. The CLI uses whatever LLM provider the local runtime is configured with.

## Reference Files

- **[DISPATCH_PROTOCOL.md](DISPATCH_PROTOCOL.md)**: Three-role architecture, sub-agent prompt templates, dispatch constraints, evidence requirements
- **[SCORING_REFERENCE.md](SCORING_REFERENCE.md)**: Scoring layers, 6-dimension weights, derived metrics, recommendation thresholds, report format

## Security & Privacy

Skill content and task prompts are sent to the configured LLM provider only. All evaluation data stored locally. No telemetry.
