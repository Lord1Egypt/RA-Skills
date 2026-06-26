---
name: self-improving-ai
description: "Captures learnings about GenAI/LLM configuration, model selection, inference optimization, fine-tuning, RAG pipelines, prompt engineering, multimodal processing, and cost management. Use when: (1) Model response quality degrades after a provider update or version change, (2) Inference latency exceeds acceptable thresholds, (3) Fine-tuned model regresses on evaluation benchmarks, (4) RAG retrieval returns irrelevant or stale chunks, (5) Token costs exceed budget projections, (6) Hallucination rate increases on factual queries, (7) Context window overflows cause critical information truncation, (8) Multimodal pipeline fails on specific input types (image, audio, video, PDF), (9) A better model or configuration is discovered for a task, (10) Guardrails block valid output or miss harmful content."
---

# Self-Improving AI Skill

Log AI/LLM-specific learnings, model issues, and feature requests to markdown files for continuous improvement. Captures model selection insights, prompt optimization patterns, inference tuning, fine-tuning regressions, RAG pipeline improvements, embedding management, multimodal processing failures, evaluation findings, and guardrail adjustments. Important learnings get promoted to model selection matrices, prompt libraries, fine-tuning runbooks, RAG architecture docs, inference optimization checklists, evaluation benchmarks, or guardrail policies.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# AI / LLM Learnings\n\nModel selection insights, prompt optimization patterns, inference tuning, fine-tuning lessons, RAG pipeline improvements, embedding management, multimodal processing, evaluation findings, and guardrail adjustments.\n\n**Categories**: model_selection | prompt_optimization | inference_latency | fine_tune_regression | context_management | modality_gap | hallucination_rate | cost_efficiency\n**Areas**: model_config | prompt_engineering | fine_tuning | rag_pipeline | inference | embeddings | multimodal | evaluation | guardrails\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/MODEL_ISSUES.md ] || printf "# Model Issues Log\n\nInference failures, model regressions, RAG retrieval problems, embedding drift, multimodal pipeline errors, and guardrail misfires.\n\n---\n" > .learnings/MODEL_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nCapabilities needed for model selection, inference optimization, fine-tuning, RAG pipelines, multimodal processing, and evaluation.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log API keys, model access tokens, customer data, or PII. Prefer redacted excerpts over raw model outputs. Mask user inputs and sensitive content in all entries.

If you want automatic reminders, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Model quality drops after provider update | Log to `.learnings/MODEL_ISSUES.md` with model version details |
| Latency spike on inference | Log to `.learnings/MODEL_ISSUES.md` with latency measurement |
| Fine-tuned model regresses on eval | Log to `.learnings/LEARNINGS.md` with `fine_tune_regression` |
| RAG returns wrong or stale chunks | Log to `.learnings/MODEL_ISSUES.md` with retrieval details |
| Token cost over budget | Log to `.learnings/LEARNINGS.md` with `cost_efficiency` |
| Hallucination detected | Log to `.learnings/LEARNINGS.md` with `hallucination_rate` |
| Context window overflow | Log to `.learnings/LEARNINGS.md` with `context_management` |
| Better model discovered for task | Log to `.learnings/LEARNINGS.md` with `model_selection` |
| Prompt tweak improves output significantly | Log to `.learnings/LEARNINGS.md` with `prompt_optimization` |
| Multimodal input fails (image/audio/video) | Log to `.learnings/MODEL_ISSUES.md` with modality details |
| Embedding quality degrades | Log to `.learnings/MODEL_ISSUES.md` with similarity metrics |
| Guardrail false positive | Log to `.learnings/LEARNINGS.md` with guardrails note |
| New AI capability needed | Log to `.learnings/FEATURE_REQUESTS.md` |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-ai
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-ai.git ~/.openclaw/skills/self-improving-ai
```

### Workspace Structure

OpenClaw injects these files into every session:

```
~/.openclaw/workspace/
├── AGENTS.md          # Multi-agent workflows, model routing
├── SOUL.md            # Model behavior guidelines, personality
├── TOOLS.md           # Model/tool configuration, parameters
├── MEMORY.md          # Long-term memory (main session only)
├── memory/            # Daily memory files
│   └── YYYY-MM-DD.md
└── .learnings/        # This skill's log files
    ├── LEARNINGS.md
    ├── MODEL_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — model selection, prompt optimization, cost efficiency, hallucination patterns
- `MODEL_ISSUES.md` — inference failures, model regressions, RAG problems, multimodal errors
- `FEATURE_REQUESTS.md` — AI tooling, evaluation frameworks, model management capabilities

### Promotion Targets

When AI learnings prove broadly applicable, promote them:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Model behavior patterns | `SOUL.md` | "Claude 4 tends to over-qualify, use direct prompting" |
| Model selection & routing | `AGENTS.md` | "Use fast model for triage, capable model for code gen" |
| Model/tool configuration | `TOOLS.md` | "Set temperature 0.1 for code, 0.7 for creative" |
| Model selection insights | Model selection matrix | "Sonnet for code gen, Opus for complex reasoning" |
| Prompt patterns that work | Prompt library | "Chain-of-thought improves code quality by 35%" |
| Fine-tuning lessons | Fine-tuning runbook | "Always include replay data to prevent forgetting" |
| RAG improvements | RAG architecture doc | "Chunk by content type, not fixed token size" |
| Inference optimizations | Performance tuning guide | "Cache system prompts, batch similar requests" |
| Evaluation findings | Benchmark suite docs | "HumanEval + internal eval for code gen models" |
| Guardrail tuning | Guardrail policy doc | "Lower toxicity threshold for customer-facing" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-ai
openclaw hooks enable self-improving-ai
```

See `references/openclaw-integration.md` for complete details.

---

## Generic Setup (Other Agents)

For Claude Code, Codex, Copilot, or other agents, create `.learnings/` in the project or workspace root:

```bash
mkdir -p .learnings
```

Create the files inline using the headers shown above.

### Add reference to agent files

Add to `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`:

#### Self-Improving AI Workflow

When AI/model issues or patterns are discovered:
1. Log to `.learnings/MODEL_ISSUES.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings to:
   - Model selection matrix — which model for which task
   - Prompt library — proven prompt patterns and templates
   - Fine-tuning runbook — training procedures and eval gates
   - RAG architecture doc — chunking, retrieval, and reranking strategies
   - Benchmark suite — evaluation methodology and baselines

## Logging Format

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: model_config | prompt_engineering | fine_tuning | rag_pipeline | inference | embeddings | multimodal | evaluation | guardrails

### Summary
One-line description of the AI/model insight

### Details
Full context: what model behavior was observed, why it matters for quality/cost/latency,
what the correct configuration or approach should be. Include metrics and benchmarks.

### Impact
- **Quality**: eval score change (e.g., HumanEval pass@1 improvement)
- **Cost**: per-request or daily cost delta
- **Latency**: P50/P99 change

### Suggested Action
Specific model swap, config change, prompt update, or pipeline improvement to adopt

### Metadata
- Source: benchmark_evaluation | a_b_test | production_monitoring | incident | user_report
- Model: model name and version (e.g., claude-4-sonnet, gpt-4o, llama-3.1-70b)
- Provider: anthropic | openai | google | meta | mistral | local | custom
- Modality: text | image | audio | video | multimodal
- Temperature/Top-P/Top-K: generation parameters used
- Token Usage: input/output tokens (e.g., 2400 input / 1800 output)
- Latency: response time in ms (e.g., P50 1200ms, P99 3400ms)
- Cost: estimated cost per request (e.g., $0.027/task)
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: model_selection.code_generation (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

**Categories for learnings:**

| Category | Use When |
|----------|----------|
| `model_selection` | A different model performs better for a task (quality, cost, or latency) |
| `prompt_optimization` | A prompt change significantly improves output quality or efficiency |
| `inference_latency` | Latency exceeds thresholds or optimization opportunity found |
| `fine_tune_regression` | Fine-tuned model scores below baseline on eval benchmarks |
| `context_management` | Context window overflow, lost-in-the-middle, or prompt structure issue |
| `modality_gap` | Model fails on specific input type (image, audio, video, PDF) |
| `hallucination_rate` | Model produces factually incorrect output on known-fact queries |
| `cost_efficiency` | Token cost exceeds budget or cost optimization opportunity found |

### Model Issue Entry [MDL-YYYYMMDD-XXX]

Append to `.learnings/MODEL_ISSUES.md`:

```markdown
## [MDL-YYYYMMDD-XXX] issue_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: model_config | prompt_engineering | fine_tuning | rag_pipeline | inference | embeddings | multimodal | evaluation | guardrails

### Summary
Brief description of the model/inference issue

### Details
What happened: model regression, inference failure, RAG retrieval miss, embedding drift,
multimodal pipeline error, or guardrail misfire. Include specific inputs and outputs (redacted).

### Root Cause
What in the model, config, or pipeline caused this issue.

### Fix
Steps taken or recommended to resolve: model swap, config change, preprocessing, reindex, etc.

### Metadata
- Model: model name and version
- Provider: anthropic | openai | google | meta | mistral | local | custom
- Modality: text | image | audio | video | multimodal
- Temperature/Top-P/Top-K: generation parameters used
- Token Usage: input/output tokens
- Latency: response time in ms
- Cost: estimated cost per request
- Environment: production | staging | development
- Related Issues: MDL-20250110-001 (if recurring)

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: model_config | prompt_engineering | fine_tuning | rag_pipeline | inference | embeddings | multimodal | evaluation | guardrails

### Requested Capability
What AI tool, framework, or capability is needed

### User Context
Why it's needed, what manual process it replaces, estimated time saved

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built: eval framework, model router, A/B test harness, monitoring dashboard

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_tool_or_capability

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `MDL` (model issue), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250415-001`, `MDL-20250415-A3F`, `FEAT-20250415-002`

## Resolving Entries

When an issue is resolved, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Fix Applied**: model swap / config change / prompt update / pipeline fix
- **Notes**: Updated model selection matrix / added to prompt library / retrained model
```

Other status values:
- `in_progress` — Actively being investigated or benchmarked
- `wont_fix` — Accepted trade-off (add reason and cost/quality analysis in Resolution notes)
- `promoted` — Elevated to model selection matrix, prompt library, fine-tuning runbook, or RAG architecture doc
- `promoted_to_skill` — Extracted as a reusable skill

## Promoting to Project Memory

When a learning is broadly applicable (not a one-off model quirk), promote it to permanent project knowledge.

### When to Promote

- Model selection insight confirmed across 3+ task types
- Prompt pattern improves quality consistently across models
- Fine-tuning lesson applies beyond one specific training run
- RAG improvement verified on multiple document types

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| Model selection matrix | Which model for which task, with benchmarks |
| Prompt library | Proven prompt patterns, system prompt templates |
| Fine-tuning runbook | Training procedures, data mixing ratios, eval gates |
| RAG architecture doc | Chunking strategy, embedding models, retrieval ranking |
| Performance tuning guide | Inference caching, batching, quantization, provider routing |
| Benchmark suite docs | Eval methodology, baseline scores, regression thresholds |
| Guardrail policy doc | Content filtering rules, PII detection, output validation |
| `AGENTS.md` | Model routing, multi-agent workflows |

### How to Promote

1. **Distill** the learning into an actionable guideline or configuration
2. **Add** to appropriate target (matrix entry, prompt template, runbook step)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: model selection matrix` (or `prompt library`, `fine-tuning runbook`, etc.)

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: MDL-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring AI issues often indicate:
   - Same model failing on same input type (→ model swap or preprocessing)
   - Same prompt pattern needed across tasks (→ add to system prompt template)
   - Same cost overrun on specific use case (→ model downgrade or caching)
   - Same hallucination on same topic (→ RAG grounding or guardrail)

## Simplify & Harden Feed

Ingest recurring AI patterns from `simplify-and-harden` into model configs or prompt libraries.

1. For each candidate, use `pattern_key` as the dedupe key.
2. Search `.learnings/LEARNINGS.md` for existing entry: `grep -n "Pattern-Key: <key>" .learnings/LEARNINGS.md`
3. If found: increment `Recurrence-Count`, update `Last-Seen`, add `See Also` links.
4. If not found: create new `LRN-...` entry with `Source: simplify-and-harden`.

**Promotion threshold**: `Recurrence-Count >= 3`, seen in 2+ task types, within 30-day window.
Targets: model selection matrix, prompt library, fine-tuning runbook, `AGENTS.md` / `TOOLS.md`.

## Periodic Review

Review `.learnings/` at natural breakpoints:

### When to Review
- When model provider announces updates or deprecations
- After switching or upgrading models
- Monthly cost review (compare actual vs budget)
- Quarterly eval benchmark re-run
- When new modality support is added
- After fine-tuning iterations

### Quick Status Check
```bash
grep -h "Status\*\*: pending" .learnings/*.md | wc -l
grep -B5 "Priority\*\*: critical\|Priority\*\*: high" .learnings/MODEL_ISSUES.md | grep "^## \["
grep -B2 "hallucination_rate\|fine_tune_regression" .learnings/LEARNINGS.md | grep "^## \["
```

### Review Actions
- Resolve fixed model issues with config change notes
- Promote recurring patterns to model selection matrix or prompt library
- Update cost projections based on actual usage
- Re-run eval benchmarks after model updates

## Detection Triggers

Automatically log when you encounter:

**Model Response Quality** (→ model issue or learning):
- Model response includes "I don't have access to" or "As an AI" when it shouldn't
- Model output contradicts known facts (hallucination)
- Response quality noticeably worse than previous interactions with same model

**Inference Performance** (→ model issue with latency/cost context):
- Response latency >5s for simple queries
- Token count approaching context limit (>80% utilization)
- Cost per session exceeding threshold
- Rate limit or quota exceeded
- Model version deprecated warning

**RAG Pipeline** (→ model issue with rag_pipeline area):
- RAG context retrieved but answer ignores it
- Retrieved chunks are irrelevant to the query
- Embedding similarity scores below threshold

**Fine-Tuning** (→ learning with fine_tune_regression):
- Fine-tuned model scoring below baseline on eval
- Training loss not converging or eval loss increasing
- Catastrophic forgetting on non-target tasks

**Multimodal** (→ model issue with multimodal area):
- Image/audio/video input returns "I can't process this"
- OCR quality drops on rotated/skewed/low-contrast scans
- Cross-modal retrieval fails (text query → image result)

**Guardrails** (→ learning with guardrails note):
- Guardrail blocks legitimate request (false positive)
- Harmful content passes through guardrail (false negative)
- Structured output validation rejects valid response

## Priority Guidelines

| Priority | When to Use | AI Examples |
|----------|-------------|-------------|
| `critical` | Model producing harmful/dangerous output, data leaking through model, fine-tuned model catastrophic regression, guardrail completely bypassed | Hallucination in medical/legal advice, PII in model output, 45% drop on coding benchmarks after fine-tune |
| `high` | Significant quality drop, latency >10x baseline, cost overrun >50%, hallucination on critical facts, multimodal pipeline broken | Model fails all rotated PDF scans, 3x latency after provider update, daily cost doubled |
| `medium` | Model selection could be better, prompt optimization opportunity, minor eval regression, cost optimization, embedding refresh needed | Sonnet 23% better than GPT-4o for code gen, chain-of-thought adds 35% quality, embedding dimension reduction saves 60% |
| `low` | Documentation of model behavior, minor prompt tweak, config cleanup | Model prefers bullet lists over paragraphs, temperature 0.1 vs 0.0 negligible difference |

## Area Tags

Use to filter learnings by AI domain:

| Area | Scope |
|------|-------|
| `model_config` | Model selection, version pinning, parameter tuning (temperature, top-p, top-k, max tokens, stop sequences), provider configuration, fallback chains |
| `prompt_engineering` | System prompts, few-shot examples, chain-of-thought, prompt templates, prompt compression, prompt caching |
| `fine_tuning` | Training data curation, hyperparameters, eval sets, RLHF/DPO, LoRA/QLoRA, catastrophic forgetting, checkpoint management |
| `rag_pipeline` | Chunking strategy, embedding models, vector stores, retrieval ranking, reranking, hybrid search, context assembly |
| `inference` | Latency optimization, batching, streaming, caching, quantization, speculative decoding, KV cache, provider routing |
| `embeddings` | Model selection, dimension reduction, index management, drift detection, similarity thresholds, multi-language |
| `multimodal` | Vision (image/PDF), audio (speech/music), video, cross-modal retrieval, modality-specific prompting, output format handling |
| `evaluation` | Benchmarks, human eval, automated eval (LLM-as-judge), A/B testing, regression testing, domain-specific metrics |
| `guardrails` | Content filtering, PII detection, toxicity, factuality checks, output validation, structured output enforcement, jailbreak prevention |

## Model Lifecycle Management

Track model deprecation schedules and plan migrations proactively.

### Deprecation Tracking

Maintain awareness of provider deprecation timelines. OpenAI models typically deprecated 6-12 months after successor release. Anthropic version-pinned models maintained per published schedule. Gemini versions follow quarterly cadence. Open-weight models (Llama, Mistral) don't deprecate but lose community support.

### Migration Planning

When a model version is deprecated: (1) log to `MODEL_ISSUES.md` with deprecation date and replacement, (2) run eval suite against replacement before cutover, (3) update all config files and fallback chains, (4) monitor quality for 7 days post-migration, (5) update model selection matrix.

Pin exact versions in production. Keep eval results versioned alongside model configs. Document behavioral differences between generations. Maintain fallback chains: primary → secondary → tertiary.

## Best Practices

1. **Pin model versions** — never use "latest" in production
2. **Benchmark before switching models** — gut feeling is not evaluation
3. **Measure cost per task, not just per token** — task-level cost captures retries and multi-turn
4. **Cache aggressively** — same prompt + same input = same output
5. **Use structured output (JSON mode)** when downstream parsing is needed
6. **Separate system prompt from user context** for cleaner caching
7. **Test multimodal inputs with edge cases** — blurry images, noisy audio, long video
8. **Keep eval sets versioned alongside fine-tuned models**
9. **Log temperature/parameters with every issue** — reproducibility matters
10. **Set up fallback chains** — provider outages happen
11. **Monitor embedding drift** after source data changes
12. **Review guardrail logs monthly** for false positive trends

## Gitignore Options

**Keep learnings local** (per-developer):
```gitignore
.learnings/
```

**Track learnings in repo** (team-wide):
Don't add to .gitignore — learnings become shared knowledge.

**Hybrid** (track templates, ignore entries):
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## Hook Integration

Enable automatic reminders through agent hooks. This is **opt-in**.

### Quick Setup (Claude Code / Codex)

Create `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-ai/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects an AI-focused learning evaluation reminder after each prompt (~50-100 tokens overhead).

### Advanced Setup (With Error Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-ai/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-ai/scripts/error-detector.sh"
      }]
    }]
  }
}
```

Enable `PostToolUse` only if you want the hook to inspect command output for model API errors, rate limits, context overflows, and inference failures.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate AI/model learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on model API errors, rate limits, inference failures |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When an AI learning is valuable enough to become a reusable skill, extract it.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Same model issue or pattern in 2+ projects or task types |
| **Verified** | Status is `resolved` with confirmed benchmark improvement |
| **Non-obvious** | Required investigation, benchmarking, or A/B testing |
| **Broadly applicable** | Not specific to one model version; useful across providers |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-ai/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-ai/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with AI-specific content, model compatibility matrix, and benchmark results
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Read skill in fresh session to ensure it's self-contained

### Extraction Detection Triggers

**In conversation**: "This model keeps failing on this", "Save this prompt pattern as a skill", "We always need this RAG config".

**In entries**: Multiple `See Also` links, high priority + resolved, same `Pattern-Key` across projects, verified benchmark improvement.

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hooks (UserPromptSubmit, PostToolUse) | Automatic via error-detector.sh |
| Codex CLI | Hooks (same pattern) | Automatic via hook scripts |
| GitHub Copilot | Manual (`.github/copilot-instructions.md`) | Manual review |
| OpenClaw | Workspace injection + inter-agent messaging | Via session tools |

### Model Routing for Multi-Agent Setups

Different agents benefit from different models:
- **Triage agent**: fast model (e.g., Claude Haiku, GPT-4o-mini) for classification and routing
- **Coding agent**: capable model (e.g., Claude Sonnet, GPT-4o) for code generation and review
- **Document processing agent**: multimodal model (e.g., Claude Opus, Gemini Pro) for image/PDF/video
- **Evaluation agent**: strong reasoning model for LLM-as-judge tasks

Log model routing decisions as `model_selection` learnings. Promote proven routing patterns to `AGENTS.md`.

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/ai/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: ai
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (ai)
Only trigger this skill automatically for AI/LLM signals such as:
- `rate limit|context window|token|hallucination|model deprecation`
- `rag|embedding|fine-tune|inference latency|guardrail`
- explicit AI/model intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/ai/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
