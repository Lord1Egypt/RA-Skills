---
name: skill-design-guide
slug: skill-design-guide-skill
displayName: Skill Design Guide
display_name: "Skill Design Guide"
description: >
  Design better AI skills with proven architecture patterns. Helps you decide
  Workflow vs Agent, pick the right pattern (Prompt Chaining, Routing,
  Parallelization, Orchestrator-Workers, Evaluator-Optimizer), write clean
  SKILL.md files, and catch common mistakes with a governance-aware quality checklist.
  Based on design principles from Anthropic, OpenAI, and LangChain.
version: "1.7.5"
agent_created: true
category: "Architecture / Design Patterns"
license: "MIT"
read_when:
  - Starting a new skill and unsure whether to use Workflow or Agent
  - Don't know which of the 5 workflow patterns to choose
  - Code works but architecture feels messy
  - Need to review a skill before production
  - "design skill architecture, workflow or agent, choose workflow pattern"
  - "review skill design, skill quality checklist, brain hands session"
  - "skill anti-patterns, prompt chaining vs routing, when to use agent"
metadata:
  openclaw:
    tags:
      - skill-design
      - agent-architecture
      - prompt-engineering
      - workflow-patterns
      - best-practices
      - developer-tools
      - ai-agents
      - openclaw
      - llm-engineering
---

# Skill Design Guide

> **30-Second Test**: If you're writing a SKILL.md or your skill "works but feels messy", load this guide.

## 🆚 What This Is (and Isn't)

| Tool | Purpose |
|------|---------|
| **skill-creator** | HOW to structure a SKILL.md file |
| **THIS GUIDE** | WHY behind design decisions — Workflow vs Agent, which pattern |

This guide answers **WHY**, not HOW. See `references/agent-design-research.md` for full industry research background.

## ✅ 3 Usage Modes

| Mode | Trigger | Output |
|------|---------|--------|
| **New Design** | "I want to build a [X] skill" | Architecture blueprint (pattern + structure) |
| **Skill Review** | "Review this skill" / "Check quality" | Report via checklist |
| **Pattern Selection** | "Should I use X or Y?" | Pattern recommendation with rationale |

---

## Hard Rules

> **These cannot be violated. They override all other considerations.**

1. **Simplicity first.** Start with a single SKILL.md. Add complexity only when simpler solutions fail.
2. **Brain ≠ Hands.** LLM decides what to do (SKILL.md). Deterministic code does it (scripts/). Never mix them.
3. **No full preload.** References are loaded on-demand. Never dump everything into context at once.
4. **Every skill must have:** triggers, steps tagged `[Deterministic]`/`[LLM]`, Hard Rules, Failure Handling, Output Format.
5. **Maintain what you publish.** A published skill unchanged for over four weeks gets a genuine micro-improvement pass — never an empty version bump. Each update must contain at least one real change.

---

## Principle Zero: Simplicity First

> **Start simple. Add complexity only when simpler solutions fall short.**

Practical checklist:
- Single SKILL.md before multiple files
- Deterministic code before LLM
- Fixed workflow before dynamic Agent
- Ship MVP, iterate from output quality

---

## Principle One: Brain / Hands / Session

| Layer | Role | File |
|-------|------|------|
| **Brain** | Decision logic, workflow definition | `SKILL.md` |
| **Hands** | Deterministic execution | `scripts/` |
| **Session** | Knowledge base, config, templates | `references/`, `assets/` |

**Your skills already follow this:** `data-ai-daily-brief` (scripts fetch data), `benjie-model` (Session layer for other skills).

---

## Principle Two: Design for Agent Consumption

> **The primary reader of a skill is an agent runtime, not a human browsing a marketplace.**

Verified evidence (SkillHub TRACE evaluation, 2026-08): trigger scores describe skills being **"唤醒" (awakened)** by user phrases and evaluated on **parameter passing** — both agent-runtime behaviors. The entire evaluation pipeline (including security scans) is automated. Agent-initiated install and invocation is the dominant consumption path.

Design consequences:

| Field | Human-search priority (old) | Agent-consumption priority (now) |
|---|---|---|
| `description` | Catchy summary, keyword stuffing | **Precise capability statement**: what it does, what it does not do, inputs/outputs — this is the agent's routing decision |
| `not_for` | Optional | **Core routing field** — the agent's exclusion logic; a false trigger costs context and wrong execution, worse than a missed trigger |
| `read_when` triggers | Keyword hit rate | Semantic completeness; embedding retrieval matches meaning, not exact keywords |
| Hard Rules / Failure Handling / Output Format | Human readability | **Execution contract** — the agent follows these at runtime after loading |
| README | Important | Marginal — agents never read it |
| Language | Chinese SEO for human search | Still useful: agent search queries **inherit the user's language**, so bilingual descriptions widen embedding match in both languages — but write for meaning, not keyword density |

Practical rules:

1. Write `not_for` as carefully as `read_when` — every excluded scenario prevents a misrouted task.
2. Don't stuff trigger keywords; one precise capability sentence (plus a bilingual summary) outperforms a keyword list under embedding retrieval.
3. Invest in the body's executable sections (Hard Rules, Failure Handling, Output Format) — that is where agent execution quality is decided.

### GEO Checklist (from live publish rounds, 2026-08/09)

Field-tested generative-engine optimization rules for skill descriptions. Apply these before any publish; they complement, not replace, the table above.

1. **First sentence = What + Use when.** The opening sentence is the model's primary routing surface — lead with the capability and the trigger condition ("Use when any X fails…"), not with background.
2. **Bilingual triggers live inside `description` itself.** Some platform search indexes (SkillHub) index only `description`, not `description_zh` — Chinese keywords must appear in the description text, not only in the dedicated Chinese field.
3. **Triggers must match the user's actual phrasing**: error message text (`no_token`, "样式丢失"), colloquial phrasing ("修改丢失", "被截断"), and platform nouns — not just your own vocabulary.
4. **Description–content consistency**: every capability the description promises must exist as a section in the body. A stale promise poisons routing — the agent loads the skill, finds nothing, and trust in the description degrades. (Empirical: a description advertised a tool quick-reference the body never had.)
5. **Slug discipline**: a slug change is a platform identity rebuild (links, installs, stats break; old slug becomes orphaned). Never rename casually. Before publishing a NEW slug, probe availability via API and validate the probe method itself against known-existing slugs — a naive probe can silently miss or mislead.
6. **Boundary declarations reduce misrouting**: keep `not_for` in sync with the description — when the description gains a new trigger phrase, check whether any not_for exclusion now conflicts with it.

---

## Step 1: Workflow or Agent?

One question: **Are the task steps predetermined?**

| Type | When |
|------|------|
| **Workflow** | Steps are clear and predictable → choose this (faster, cheaper, debuggable) |
| **Agent** | Steps uncertain, need dynamic planning → choose this (flexible but costly) |

**Most things are workflows.** Don't pick Agent because it sounds advanced.

---

## Step 2: Pick a Pattern

Five workflow patterns. Full details in `references/pattern-details.md`.

| Pattern | Best For |
|---------|----------|
| **Prompt Chaining** | Sequential steps with checkpoints |
| **Routing** | Clear input types → different paths |
| **Parallelization** | Independent subtasks |
| **Orchestrator-Workers** | Unpredictable subtasks (sparingly!) |
| **Evaluator-Optimizer** | Generate→Evaluate→Repeat until pass |

---

## Step 3: Skill Structure

### Required

| Component | Content |
|-----------|---------|
| **SKILL.md** | YAML frontmatter (`name`, `description`, `read_when`) + workflow + Hard Rules + Failure Handling + Output Format |

### Optional

| Component | When |
|-----------|------|
| `references/` | Domain knowledge (loaded on demand) |
| `scripts/` | Deterministic steps |
| `assets/` | Templates, configs |
| `hooks/` | Host-session hooks — opt-in gated, fail-open (see Behavior Surface) |
| `evals/` | Runnable output-quality checks for the skill itself |

### SKILL.md Template

```yaml
---
name: my-skill
description: One sentence. Trigger keywords: a, b, c.
version: 1.0.0
read_when:
  - "trigger phrase 1"
  - "trigger phrase 2"
---

# Skill Name

Overview paragraph.

## Workflow

### Step 1: [Deterministic] Confirm Input
- Validate input exists
- If missing, stop and report

### Step 2: [Deterministic] Load Materials
- Read `references/xxx.md` (only needed files)

### Step 3: [LLM] Core Execution
- Generate output following these rules:
  - Rule 1
  - Rule 2

### Step 4: [LLM] Self-Check
- Verify output meets criteria → fix → re-output

### Step 5: [Deterministic] Save Output

## Hard Rules

> These cannot be violated.

1. Rule 1
2. Rule 2

## Failure Handling

| Scenario | Action |
|----------|--------|
| Source file not found | Stop, report missing file |
| Output 50% over limit | Compress and rewrite |

## Output Format

[Define exact format and fields]
```

---

## Step 4: Quality Checklist

After completing a skill, run the full governance-aware checklist. Load `references/quality-checklist.md` for details.

Structure ✓ | Principles ✓ | Tools ✓ | Guardrails ✓ | Behavior surface ✓ | Observability ✓

---

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|------|
| **Over-engineering** | Start with single SKILL.md |
| **Full preload** | Load references on-demand only |
| **God Skill** | Split duties — one skill, one thing |
| **All-LLM** | Scripts for deterministic steps |
| **No guardrails** | Add Hard Rules + Failure Handling |
| **Vague output** | Define exact format and fields |
| **Publishing dirty** | Before publishing, run `skill-publish` to audit and clean |
| **Undeclared side effects** | Declare every network/credential behavior in the frontmatter (see Behavior Surface) |

---

## Behavior Surface: Minimal, Opt-in, Declared

Rules for anything a skill ships beyond prose — hooks, scripts, platform adapters. Distilled from live scanner findings and a 48k-star community skill (2026-09).

| Rule | What it means |
|------|---------------|
| **Opt-in only** | Anything that runs automatically (hooks, session-start injection) is gated behind a user-created flag file; flag absent → do nothing |
| **Fail open at the host boundary only for non-safety paths** | A hook or helper that misbehaves must never crash the host session: catch unexpected errors and exit 0. But a safety-relevant check (credential exposure, destructive action, disallowed network call) must fail **closed** — refuse the action and surface a warning, never silently continue. |
| **Resolve paths from the script's own location** | Never trust environment variables to locate bundled files — derive them from the script path |
| **Single source of truth** | One canonical rules file; platform adapters only inject it, never copy it — copies drift and contradict |
| **Declarations match behavior** | Every network endpoint, credential source, and file read the scripts perform must appear in the frontmatter (`permissions` + capability tokens). Scanners flag undeclared behavior (LP1), and absolute claims like "never reads files" must be scoped when another component does read one |
| **Ship an override section** | State when the skill's own rules yield — safety > task > harness > style. Rules without an escape hatch get discarded wholesale |

Keep the surface minimal: the best helper does nothing until explicitly invoked, and nothing harmful when it fails.

---

## After Design: Publishing

When the skill is ready to share on ClawHub/GitHub, use **`skill-publish`** to audit and publish. It handles: personal data scanning, frontmatter validation, content cleanup, bilingual enforcement, file separation (local vs published), and dual-platform push.

---

## Failure Handling (for this guide itself)

| Scenario | Action |
|----------|--------|
| User asks for code, not design | Redirect to `skill-creator` |
| Pattern comparison ambiguous | Load `references/pattern-details.md` |
| Review request without skill details | Ask: "Show me your SKILL.md or describe what the skill does" |
| User wants to publish a completed skill | Redirect to `skill-publish` |

---

## References (on-demand)

| Need | Load |
|------|------|
| 25-point checklist | `references/quality-checklist.md` |
| Pattern deep dive | `references/pattern-details.md` |
| Platform-specific config | `references/platform-compatibility.md` |
| Industry research background | `references/agent-design-research.md` |
| Anthropic tool design | `references/anthropic-tool-design.md` |
| Publishing to ClawHub/GitHub | Use `skill-publish` (separate skill) |

---

*v1.7.3 | Based on Anthropic/OpenAI/LangChain design principles | 2026-09-20*

**Changelog:**
- v1.7.2: Added Hard Rule 7 (maintain published skills: real micro-improvements, no empty bumps)
- v1.7.1: Added "Behavior Surface" section (opt-in gating, fail-open hooks, path self-resolution, single source of truth, declaration-behavior match, override section) + `hooks/` and `evals/` as optional components + undeclared-side-effects anti-pattern. Distilled from the i-have-adhd skill audit and the LP1 scanner findings. (Changelog entries for v1.5.0-v1.7.0 were not kept; the frontmatter version remained authoritative.)
- v1.4.6: Published merged content to the correct slug `skill-design-guide-skill` — restores 9 `metadata.openclaw.tags` (discoverability) + 1.4.4 governance-aware checklist / Governance & Continuity checks. (The bare `skill-design-guide` slug on ClawHub is occupied by an unrelated third-party account — owner `tttt-bjgs`, old Chinese draft published 2026-03, verified via inspect owner field 2026-09-20. It is not ours: never delete or publish to it. This is why the canonical slug carries the `-skill` suffix. An earlier version of this line wrongly assumed it was our own stray duplicate.)
- v1.4.5: Restored `metadata.openclaw.tags` (9 discoverability tags) dropped in the 1.4.4 sync; no content change beyond 1.4.4 governance additions
- v1.4.4: Added governance checks for single source of truth, private-data separation, secret scanning, retry/re-run, external-action gates, and persistent task continuity
- v1.4.3: Restored display name "Skill Design Guide"
- v1.4.2: Consolidated `reference/` + `references/` into a single `references/` dir; fixed all reference paths
- v1.4.1: Fixed display name
- v1.4.0: Refactored for progressive disclosure — split checklist/patterns/platform into `references/`; added Hard Rules + Failure Handling; reduced SKILL.md from 13K to ~5K chars
- v1.3.0: Added usage scenarios, Chinese version (SKILL_zh.md)
- v1.2.0: Platform-agnostic rewrite, added Credits
