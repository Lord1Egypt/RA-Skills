# AI / LLM Skill Template

Template for creating skills extracted from AI/LLM learnings. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the model behavior, prompt pattern, inference optimization, or RAG improvement this skill addresses. Include trigger conditions."
---

# Skill Name

Brief introduction: what AI/model problem this skill solves, which models and providers it applies to, and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Model/inference trigger] | [Config change, prompt fix, or model swap] |
| [Related trigger] | [Alternative approach] |

## Background

Why this AI/LLM knowledge matters. What quality degradation, cost overrun, or latency issue it prevents.

## The Problem

### Current Behavior

```
// Model output, error message, or metric showing the issue
```

### Impact

How the problem manifests: quality drop, cost increase, latency spike, hallucination, or modality failure.

## Solution

### Fix

```
// Updated config, prompt, model selection, or pipeline change
```

### Step-by-Step

1. Identify the model/config issue
2. Benchmark current performance (latency, quality, cost)
3. Apply the fix
4. Re-evaluate on benchmark suite
5. Monitor in production for regression

## Model Compatibility Matrix

| Model | Provider | Version | Tested | Result |
|-------|----------|---------|--------|--------|
| [model-name] | [provider] | [version] | [date] | [pass/fail with notes] |

## Benchmark Results

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Quality (eval score) | [score] | [score] | [+/-] |
| Latency (P50/P99) | [ms] | [ms] | [+/-] |
| Cost (per 1K requests) | [$] | [$] | [+/-] |
| Token usage (avg) | [tokens] | [tokens] | [+/-] |

## Configuration

### Model Parameters

```json
{
  "model": "model-name",
  "temperature": 0.1,
  "top_p": 0.95,
  "max_tokens": 4096,
  "stop_sequences": []
}
```

### Prompt Template

```
[System prompt or prompt pattern that implements the fix]
```

## Common Variations

- **Variation A**: Description and how to handle across different model families
- **Variation B**: Description for multimodal vs text-only scenarios

## Provider Compatibility

| Provider | Models Affected | Notes |
|----------|----------------|-------|
| Anthropic | Claude 4 Opus, Claude 4 Sonnet | [compatibility notes] |
| OpenAI | GPT-4o, GPT-4o-mini | [compatibility notes] |
| Google | Gemini 2.5 Pro, Gemini 2.5 Flash | [compatibility notes] |
| Meta | Llama 3.1 70B, Llama 3.1 8B | [compatibility notes] |
| Mistral | Mistral Large, Codestral | [compatibility notes] |

## Gotchas

- Warning or common mistake when applying the fix
- Edge case with specific model versions or providers
- Behavior differences between text and multimodal inputs

## Related

- Link to model provider documentation
- Link to related evaluation benchmark
- Link to related skill

## Source

Extracted from AI/LLM learning entry.
- **Learning ID**: LRN-YYYYMMDD-XXX or MDL-YYYYMMDD-XXX
- **Original Category**: model_selection | prompt_optimization | inference_latency | fine_tune_regression | context_management | modality_gap | hallucination_rate | cost_efficiency
- **Area**: model_config | prompt_engineering | fine_tuning | rag_pipeline | inference | embeddings | multimodal | evaluation | guardrails
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple AI/LLM skills that don't need all sections:

```markdown
---
name: skill-name-here
description: "What model behavior or AI pattern this addresses and when to apply it."
---

# Skill Name

[Problem statement in one sentence]

## Problem

Description of the model behavior, inference issue, or prompt failure.

## Solution

Updated config, prompt change, or model swap that resolves the issue.

## Benchmark Results

| Metric | Before | After |
|--------|--------|-------|
| [key metric] | [value] | [value] |

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `code-gen-model-selection`, `rag-chunk-sizing`, `lost-in-the-middle-fix`
  - Bad: `ModelSelection`, `rag_chunks`, `fix1`

- **Description**: Start with action verb, mention the model or AI component
  - Good: "Optimizes RAG chunk sizes by content type to improve retrieval relevance. Use when retrieval scores drop below 0.8."
  - Bad: "RAG stuff"

- **Files**:
  - `SKILL.md` — Required, main documentation
  - `scripts/` — Optional, automation (benchmark runner, config validator)
  - `references/` — Optional, detailed docs
  - `assets/` — Optional, templates

---

## Extraction Checklist

Before creating a skill from an AI/LLM learning:

- [ ] Fix is verified (benchmarked, tested with eval suite)
- [ ] Solution is broadly applicable (not one-off model quirk)
- [ ] Model compatibility matrix is filled in
- [ ] Benchmark results are documented (before/after)
- [ ] Configuration parameters are specified
- [ ] Provider compatibility is noted
- [ ] Name follows conventions
- [ ] Description is concise but informative

After creating:

- [ ] Update original learning with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to learning metadata
- [ ] Test skill by reading it in a fresh session
- [ ] Verify config changes work across target models
- [ ] Re-run eval suite to confirm no regression
