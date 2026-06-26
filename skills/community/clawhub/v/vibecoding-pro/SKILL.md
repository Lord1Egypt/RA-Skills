---
name: vibe-coding-pro
slug: vibe-coding-pro
version: "1.0.0"
description: >
  Transform your AI coding workflow from "write and hope" to "iterate with precision."
  VibeCoding Pro implements the Generator-Evaluator dual-agent pattern (inspired by Anthropic's
  engineering research and GAN design theory) — separating the creative agent that produces
  code from an independent QA agent that validates it through real browser interaction.
  Eliminates AI self-evaluation bias structurally, not through better prompts.
  Use when: building React/UI components that need real quality assurance, running multi-round
  AI-assisted development sprints, or upgrading from "vibe coding" (prompt → code → done) to
  genuine engineering-grade AI development workflows.
---

# VibeCoding Pro

> **The AI coding upgrade that actually ships working software.**

VibeCoding is fun. VibeCoding Pro is *reliable*.

---

## What VibeCoding Gets Wrong

Most AI coding workflows look like this:

```
You → "build a login form" → AI generates → "looks good!" → ship it
                                            ↑
                                   This is the problem.
```

**Why it's broken:** The same AI that generated the code judges whether it works. It suffers from *cognitive commitment bias* — it can't objectively evaluate what it just built because it already committed to the approach. Bugs survive. Edge cases break. UX issues ship.

**The evidence:** Anthropic's 2026 engineering research ran an experiment. Solo Claude agents produced 2D game makers where the core game loop was fundamentally broken — entities rendered but ignored all player input. The agent called its own output "working." Only when a separate Evaluator agent physically clicked through the game did it discover the wiring between entity definitions and game runtime was severed.

---

## What VibeCoding Pro Gets Right

```
User Goal / Spec
      ↓
 ┌─────────────┐
 │  Generator  │ ← "Build X according to spec"
 │  (vibe)     │
 └──────┬──────┘
        │ artifact
        ↓
 ┌────────────────────────────────────┐
 │           Evaluator                │
 │  • Reads SPEC (NOT generator output)│
 │  • Opens URL in real browser        │
 │  • Clicks, fills, navigates         │
 │  • Scores on rubric (0-100)          │
 │  • Returns structured JSON feedback  │
 └────────────────┬───────────────────┘
                  │ score + feedback
                  ↓
         ┌────────────────┐
         │ score ≥ threshold? │
         │ YES → Done     │
         │ NO → Generator  │
         └────────┬────────┘
                  └── Loop (5-15 rounds)
```

**The structural fix:** Evaluator never reads the generator's code, reasoning, or commit messages. It only reads the SPEC and operates the deployed artifact. This eliminates anchoring bias architecturally — not through clever prompting.

---

## When to Use VibeCoding Pro

| Scenario | Apply? | Why |
|----------|--------|-----|
| React / H5 / Web UI with real interactions | ✅ Yes | Playwright can actually click through it |
| Multi-step form flows (wizard, checkout, onboarding) | ✅ Yes | Evaluator can exercise each step |
| API + frontend integration | ✅ Yes | Evaluator calls endpoints and checks DB state |
| Single utility function | ⚠️ Optional | Might be overkill |
| Pure backend logic (no UI) | ⚠️ Use API Evaluator template | Evaluator calls endpoints directly |
| Design-sensitive work (brand identity, layout) | ✅ Yes | Human-in-the-loop variant works best |

---

## Quick Start

### Step 1: Write a Spec Contract

The SPEC is the most important artifact. It's the Evaluator's only reference.

```markdown
# Spec: [Feature Name] v1.0

## Goal
[One sentence: what exists when this is done?]

## Functional Requirements
- FR-001: [Specific, testable, observable]
- FR-002: [...]

## Interaction Specifications
- UI-001: [User clicks X → Y happens]
- UI-002: [Form accepts type Y, rejects type N]

## Acceptance Criteria
- AC-001: [Measurable outcome]
- AC-002: [...]

## Out of Scope
- [Explicitly NOT required]

## Test Scenarios
**Scenario 1:** Happy path — normal user completes primary action
**Scenario 2:** Edge case — empty data, error state
**Scenario 3:** Boundary — max input length, concurrent actions
```

### Step 2: Run the Loop

1. **Generator Agent** receives: SPEC + iteration history + previous Evaluator feedback
2. **Generator** builds artifact and deploys
3. **Evaluator Agent** receives: SPEC + deployed URL (NOT generator code)
4. **Evaluator** opens browser, clicks through test scenarios, screenshots, scores
5. **Evaluator** returns structured JSON with score breakdown
6. If score ≥ threshold → done. If not → loop back to Generator.

---

## Architecture Reference

See `references/architecture.md` for:
- Four architecture variants (Sequential / Parallel / Staged / Human-in-loop)
- GAN theory deep-dive and why it works
- Spec Contract template (copy-paste ready)
- History format and loop control logic
- Anti-patterns and how to fix them

---

## Evaluator Templates

See `references/evaluator-prompts.md` for:

| Template | When to Use | Evaluator Mode |
|----------|-------------|----------------|
| **Web/H5 UI** | React/Vue/H5/Web components | Playwright browser automation |
| **API/Backend** | REST endpoints, microservices | Direct HTTP calls |
| **Content/Docs** | Reports, copy, documentation | Structured text scoring |

Each template includes:
- System prompt (calibrated for evaluator independence)
- User prompt with rubric
- Required JSON output schema
- 4 calibration examples (30/60/85/95 score ranges)

---

## Iteration Loop Scripts

See `scripts/iteration_loop.py` for a complete Python implementation:
- `run_generator()` — adapt to your agent (Claude API, OpenAI, subagent, etc.)
- `run_evaluator()` — adapt to your QA stack (Playwright, HTTP client, etc.)
- Full loop control: plateau detection, approach switching, escalation
- CLI: `python iteration_loop.py --spec spec.md --url http://localhost:3000 --threshold 85 --rounds 15`

See `scripts/calibrate_evaluator.py` for evaluator calibration utility:
- Run on 4 known examples before production
- Auto-detects score drift and suggests rubric adjustments

---

## Scoring Rubric

Default rubric (adjust weights by domain):

| Dimension | Weight | Measures |
|-----------|--------|---------|
| Functional completeness | 30% | Every spec requirement works end-to-end |
| Interaction quality | 25% | Click/form/nav behavior as a real user |
| Edge case handling | 20% | Error states, empty data, boundary inputs |
| Code/design quality | 15% | Consistency, readability, no anti-patterns |
| Originality/craft | 10% | Avoids template defaults and AI slop patterns |

**Threshold guidelines:**

| Use Case | PASS_THRESHOLD | MAX_ROUNDS |
|----------|----------------|------------|
| Internal prototype | 70 | 10 |
| User-facing feature | 85 | 15 |
| Production critical | 95 | 20 + human review |

---

## Why This Works (Research Background)

**Source:** Anthropic Engineering, "Harness Design for Long-Running Application Development" (March 2026)

Key findings:
- Solo Claude agents on 16-feature game maker: core game loop broken, entity runtime wiring severed
- Full harness (Generator + Evaluator): fully working, sprite animation, sound, AI-assisted level design
- Opus 4.6 vs 4.5: improved planning reduced harness complexity needed
- Evaluator value is *situational*: worth the cost when task exceeds what the model reliably does solo

**GAN theory parallel:** The Generator tries to fool the Evaluator. The Evaluator tries to catch failures the Generator misses. The adversarial tension drives quality upward. Unlike ML GANs, this uses natural language feedback — it's fully inspectable and steerable.

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Same agent generates and evaluates | Cognitive anchoring bias | Separate agents with separate prompts |
| Evaluator reads generator's code | Judges intent, not reality | Show only deployed URL |
| Skipping calibration | Score inflation/drift | Run 3-5 known examples first |
| Vague scoring ("7/10 looks fine") | Unactionable feedback | Require structured JSON per rubric |
| Too few rounds | Generator never converges | Minimum 10 rounds for complex UI |
| Never switching approach | Gets stuck in local minimum | Switch strategy after 3 plateauing rounds |
| Using for trivial tasks | Overhead > value | Reserve for multi-feature/full-page work |

---

## OpenClaw Integration

In OpenClaw, use the `coder` + `tester` subagents:

```
Generator → sessions_spawn(agentId="coder", ...)
Evaluator → sessions_spawn(agentId="tester", ...) + browser tool
```

The `tester` subagent should use the Playwright MCP tool:
- `browser_navigate` → open URL
- `browser_click` → interact
- `browser_fill` → form input
- `browser_screenshot` → capture evidence

---

*Built on Anthropic's 2026 engineering research. Inspired by GAN theory and adversarial validation patterns.*
