# Model Requirements

Quorum's critics need models that can reason about complex artifacts, follow structured evaluation rubrics, use tools (file reading, web search, shell commands), and maintain state across multi-step analysis. Not all models can do this reliably.

## Tier System

Quorum uses a two-tier architecture. **Tier 1** handles judgment-heavy roles (supervisor, aggregator, security critic). **Tier 2** handles pattern-matching roles (correctness, completeness, architecture critics). See [CONFIG_REFERENCE.md](../configuration/CONFIG_REFERENCE.md) for which roles map to which tier.

### Tier 1 — Recommended (Judgment Roles)

These models have the reasoning depth and instruction-following precision required for orchestration, synthesis, and high-stakes evaluation.

| Model | Provider | Notes |
|-------|----------|-------|
| Claude Opus 4.6+ | Anthropic | Best overall for Quorum's judgment roles |
| Claude Sonnet 4.6+ | Anthropic | Strong alternative, significantly cheaper |
| GPT-5.2+ | OpenAI | Capable; tool-use patterns differ slightly |
| Gemini 2.0 Ultra+ | Google | Capable; long-context advantage on large artifacts |

### Tier 2 — Capable (Evaluation Roles)

These models handle structured evaluation well but lack the depth for synthesis and conflict resolution.

| Model | Provider | Notes |
|-------|----------|-------|
| Claude Sonnet 4.6+ | Anthropic | Recommended Tier 2 default |
| Claude Haiku 4.5+ | Anthropic | Usable for simple rubrics; degrades on nuanced evaluation |
| GPT-4o | OpenAI | Adequate for pattern-matching critics |
| Gemini 2.0 Flash | Google | Fast, cost-effective for coverage checks |

### Not Recommended

These models consistently fail at one or more critical requirements (tool use, rubric adherence, evidence grounding, state tracking):

- **Claude Haiku** (pre-4.5) — Insufficient reasoning depth; produces false-precision scores and contradictory findings
- **GPT-4** (original) — Tool-use reliability too low for critic pipelines
- **Llama 70B and below** — Open models at this scale lack the instruction-following precision Quorum requires
- **Mixtral, Command R** — Similar limitations to Llama at comparable scales

> **Why not smaller models?** Quorum critics must: (1) follow a structured rubric item-by-item, (2) cite specific evidence for every finding, (3) assign calibrated severity ratings, and (4) avoid hallucinating findings that aren't grounded in the artifact. Models below ~100B parameters reliably fail at #2 and #4.

## Configuration

Set your model tiers in `quorum-config.yaml`:

```yaml
models:
  tier_1: anthropic/claude-sonnet-4-6    # Judgment roles (supervisor, aggregator, security)
  tier_2: anthropic/claude-sonnet-4-6    # Evaluation roles (correctness, completeness, architecture)
```

For per-critic overrides, see [CONFIG_REFERENCE.md](../configuration/CONFIG_REFERENCE.md).

**First-run behavior:** If no config exists, Quorum auto-detects your available model, asks two setup questions (preferred tier 1 and tier 2 models), writes the config, and proceeds immediately. Zero-config users get sensible defaults.

## Cost Estimates

Rough per-run costs at default (standard) depth with 6 critics:

| Configuration | Tier 1 | Tier 2 | Estimated Cost |
|---------------|--------|--------|----------------|
| Budget | Sonnet | Haiku | ~$0.15–0.30 |
| Balanced | Sonnet | Sonnet | ~$0.30–0.60 |
| Premium | Opus | Sonnet | ~$1.00–2.50 |

Costs scale roughly linearly with critic count and artifact size. The `quick` depth profile (2 critics, no fix rounds) is the cheapest option for iteration.

## Platform Compatibility

Quorum is designed for **OpenClaw** and tested primarily on that platform. The architecture is intentionally model-agnostic — the spec and rubric format don't assume a specific provider. Cross-platform compatibility with other agent frameworks is under active research.

If you're running Quorum on a non-OpenClaw platform and want to share results, [open an issue](https://github.com/SharedIntellect/quorum/issues).


---

> ⚖️ **LICENSE** — Not part of the operational specification above.
> This file is part of [Quorum](https://github.com/SharedIntellect/quorum).
> Copyright 2026 SharedIntellect. MIT License.
> See [LICENSE](https://github.com/SharedIntellect/quorum/blob/main/LICENSE) for full terms.
