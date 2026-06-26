---
name: smart-model-router
version: 1.2.0
description: "Stop sending 'format this JSON' to Opus. Stop sending 'redesign the auth system' to Haiku. Smart Model Router picks the right brain for every task — decision tree, cost tiers, and an optional cheap-model classifier for the ambiguous ones."
metadata:
  openclaw:
    emoji: "🧭"
    notes:
      security: "No network calls. Decision tree logic only — reads task description, outputs model recommendation."
---

# Model Router

Automatically select the right LLM for any task. Stop overpaying for simple tasks. Stop under-powering complex ones.

## Quick Decision: Can You Route Without a Classifier?

Most tasks fit obvious categories. Check the **Fast Route Table** first. Only use the classifier for ambiguous cases.

### Fast Route Table

| Signal in task | Route to | Why |
|---|---|---|
| "what time" / "what date" / simple lookup | **flash** | Zero reasoning needed |
| Format conversion, CSV→JSON, extract fields | **flash** | Mechanical transformation |
| Summarize text, list bullet points | **fast** | Pattern matching, not reasoning |
| Translate text | **fast** | Well-trained capability across all models |
| Write code, implement feature, refactor | **mid** | Needs structured thinking |
| Review code, find bugs, security audit | **mid** | Analysis without deep creativity |
| Draft email, write content | **mid** | Needs tone + context awareness |
| Research + synthesize from multiple sources | **mid** | Needs breadth, not max depth |
| Debug complex system, multi-file investigation | **strong** | Needs deep reasoning chains |
| Reflect on failures, self-improvement | **strong** | Requires genuine metacognition |
| Creative writing with nuance | **strong** | Judgment + style + originality |
| Math proofs, formal logic, complex reasoning | **reasoning** | Chain-of-thought specialist |
| Architectural decisions, tradeoff analysis | **strong** | Needs weighing multiple factors |

### Tier → Model Mapping

Configure these based on your available providers:

| Tier | Default Model | Alternatives | Cost (per 100-token query) |
|---|---|---|---|
| **flash** | `gemini-flash` | `haiku` | ~$0.00007 |
| **fast** | `haiku` | `gemini-flash`, `gpt-4o-mini` | ~$0.0003 |
| **mid** | `sonnet` | `gpt-5.2`, `gemini` | ~$0.001 |
| **strong** | `opus` | `gpt-5.2-pro`, `gemini` | ~$0.003 |
| **reasoning** | `openai/o3` | `opus` (with thinking) | ~$0.002 |

## The "Good Enough" Principle

**Not every task needs the smartest model. Most tasks need a fast, cheap, correct one.**

### Definitely Does NOT Need Big Brains (flash/fast tier)

These tasks have a single correct answer or a mechanical transformation. No model does them "better" — they all get it right. Use the cheapest:

- Date/time queries, timezone conversions
- Regex generation, string formatting
- JSON/CSV/XML transformations
- Template filling (mail merge, form letters)
- Data extraction from structured text
- Simple Q&A with context provided
- Spell checking, grammar fixes
- File listing, directory scanning summaries
- Status checks, health report formatting
- Translating short text

### Needs Real Intelligence (mid tier)

These tasks benefit from a good model but don't need the frontier. The gap between mid and strong is <5% quality for 5x the cost:

- Code generation (functions, classes, modules)
- Code review and bug finding
- Content writing (blog posts, documentation)
- Email drafting with tone awareness
- Data analysis with narrative
- API integration code
- Test generation
- Summarizing long documents
- Morning briefings, daily reports

### Actually Needs Top Tier (strong)

Only route here when the task genuinely requires deep reasoning or creativity that cheaper models measurably fail at:

- Multi-step debugging across files
- Architectural refactoring decisions
- Self-reflection and failure analysis (wind-down)
- Nuanced judgment calls (should we do X or Y?)
- Creative writing with specific voice/style
- Complex negotiation drafting
- Synthesizing contradictory information
- Tasks where being wrong has high cost

## Classifier Prompt (For Ambiguous Cases)

When the Fast Route Table doesn't clearly match, use a cheap model to classify. Send this to `gemini-flash` or `haiku`:

```
Classify this task into exactly one tier. Reply with ONLY the tier name.

Tiers:
- flash: mechanical lookup, formatting, simple extraction
- fast: summarization, translation, template work
- mid: code generation, content writing, analysis, drafting
- strong: complex debugging, self-reflection, creative writing, architectural decisions
- reasoning: math proofs, formal logic, multi-step deduction

Task: {TASK_DESCRIPTION}

Tier:
```

Cost: ~20 tokens (~$0.000001). Negligible.

### Generosity Rule (When in Doubt, Go Up)

If the classifier returns a tier but you're unsure:
- **Non-critical task** → trust the classifier
- **User-facing output** → go one tier up
- **Irreversible action** → always use strong
- **Ambiguous between two tiers** → pick the higher one

This is the "generous in doubt" principle: overspending 1¢ on a better model costs less than a bad result that needs re-doing.

## Integration with OpenClaw

### Sub-agent spawning

```javascript
// Before (manual):
sessions_spawn({ task: "Review this PR", model: "sonnet" })

// After (auto-routed):
// 1. Check Fast Route Table → "Review code" → mid → sonnet
sessions_spawn({ task: "Review this PR", model: "sonnet" })

// For ambiguous tasks:
// 1. Fast Route doesn't match clearly
// 2. Send classifier prompt to gemini-flash
// 3. Get tier → map to model
// 4. Spawn with that model
```

### Cron job model assignment

Use the table when creating or reviewing crons:

```
heartbeat:        flash  → qwen3 (local, free)
cleaning-lady:    fast   → sonnet
morning-briefing: mid    → sonnet
code review:      mid    → sonnet
wind-down:        strong → opus
self-evolution:   strong → opus
```

### Agent-level rule (add to AGENTS.md)

```markdown
## Model Routing

When spawning sub-agents, auto-select model by task type:
- Mechanical/extraction/formatting → gemini-flash
- Summarization/translation → haiku
- Coding/drafting/analysis → sonnet
- Deep reasoning/self-reflection → opus
- Math/logic/chain-of-thought → o3
When in doubt, go one tier up. Overpaying 1¢ beats re-doing work.
```

## Provider Strengths (2026 Benchmarks)

For detailed model comparisons, see `references/model-strengths.md`.

Quick reference for tier selection when multiple models are available at the same tier:

| Strength | Best provider | Why |
|---|---|---|
| Coding (Terminal-Bench) | Claude (Opus/Sonnet) | 65.4 score, leads benchmarks |
| Large context (>200K) | Gemini | 1M window, native long-doc |
| Multimodal (images/video) | Gemini | Full video processing |
| Structured feedback | GPT | Calibrated, consistent format |
| Chain-of-thought reasoning | o3 | Purpose-built for deduction |
| Speed + cost efficiency | Gemini Flash | Fastest, cheapest tier |
| Creative/nuanced writing | Opus | Best subjective quality |

## Cron & Sub-Agent Routing

The router applies to ALL model selections, including:
- Sub-agents spawned by cron jobs (not just interactive)
- Sub-agents spawned by other sub-agents (recursive routing)
- Cron job model assignment at creation time
- The classifier model itself (always flash)

### Cron Model Assignment
```
heartbeat:        flash/local  → qwen3 (free)
cleaning-lady:    fast         → haiku or sonnet
morning-briefing: mid          → sonnet
code review:      mid          → sonnet (or gpt for cross-model review)
wind-down:        strong       → opus (needs metacognition)
self-evolution:   strong       → opus
research reports: mid          → gemini (large context)
```

### Sub-Agent Spawning Rule
When a cron job spawns sub-agents, EACH sub-agent gets its own tier:
```
Cron: morning-briefing (sonnet)
  └── Sub-agent: check emails → fast (haiku)
  └── Sub-agent: calendar summary → flash (gemini-flash)
  └── Sub-agent: draft briefing text → mid (sonnet)
```

## Big Task Orchestration

For complex multi-step tasks, see `references/task-orchestration.md`:
- Hierarchical supervisor → workers pattern
- Pipeline pattern (gather → analyze → synthesize)
- Parallel fan-out with merge
- Context isolation to prevent collapse
- Claude Code architecture lessons (reverse-engineered)

## Chain-of-Thought Optimization

Match CoT technique to tier for maximum ROI. See `references/chain-of-thought.md`:
- flash/fast: no CoT (tasks too simple)
- mid: structured CoT for complex sub-tasks
- strong: full CoT, Tree of Thought
- reasoning (o3): native CoT (don't prompt for it)

## What to Keep in Bootstrap vs Auxiliary Files

**In AGENTS.md (every prompt):** Only the routing rule (7 lines):
```
When spawning sub-agents, auto-select model by task type:
- Mechanical/extraction/formatting → gemini-flash
- Summarization/translation → haiku
- Coding/drafting/analysis → sonnet
- Deep reasoning/self-reflection → opus
- Math/logic/chain-of-thought → o3
- Reviews/second opinions → gpt
When in doubt, go one tier up.
```

**In this skill (loaded on demand):** The full routing table, classifier prompt, tier definitions, provider strengths.

**In reference files (loaded only when needed):**
- `references/model-strengths.md` — detailed benchmarks and per-provider analysis
- `references/task-orchestration.md` — big task decomposition, Claude Code architecture
- `references/chain-of-thought.md` — CoT techniques matched to tiers

This follows the progressive disclosure principle: 7 lines always loaded, full skill on demand (~5KB), deep references only when the task requires them.

## Anti-Patterns

- ❌ Using Opus for "what time is it" (flash task, 40x overspend)
- ❌ Using Flash for debugging a race condition (will miss it)
- ❌ Always defaulting to one model (defeats the purpose)
- ❌ Routing user-facing content to the cheapest model (quality matters)
- ❌ Classifying every task (most fit the Fast Route Table obviously)
- ❌ Putting the full routing table in bootstrap files (wastes tokens every prompt)
- ❌ Not routing cron sub-agents (they spend tokens too)
- ❌ Self-reviewing output (use a different model for review)

## Pairs Well With

- [model-prompt-adapter](https://clawhub.com/globalcaos/model-prompt-adapter) — once Router picks the model, Adapter fixes its quirks
- [subagent-overseer](https://clawhub.com/globalcaos/subagent-overseer) — monitor the sub-agents you're routing models for
- [agent-superpowers](https://clawhub.com/globalcaos/agent-superpowers) — the full engineering pipeline these routed agents should follow

👉 **https://github.com/globalcaos/tinkerclaw**

_Clone it. Fork it. Break it. Make it yours._
