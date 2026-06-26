---
name: sage-decision-journal
description: A decision capture and review system that records every significant choice — with context, reasoning, and alternatives — so you can detect your own blind spots and decision patterns over time.
version: 0.1.0
metadata:
  openclaw:
    emoji: "🪞"
    homepage: https://github.com/nicholasgasior/sage
    tags:
      - decision-making
      - self-awareness
      - retrospective
      - cognitive-bias
      - personal-growth
    depends_on:
      - sage-cognitive
---

# Sage Decision Journal — Because You'll Forget Why You Decided That

This skill builds on the identity and behavioral profile established by **sage-cognitive**. Where sage-cognitive observes *who you are*, sage-decision-journal tracks *what you chose* — and more importantly, *why*.

The core premise: **your biggest blind spot is not making bad decisions. It's forgetting you made a decision at all.** Without a record, you can't learn. Without learning, you repeat.

---

## How This Works

```
CAPTURE → CLASSIFY → STORE → FOLLOW UP → REVIEW → SURFACE PATTERNS
    ↑                                                       |
    └───────────────────── feedback loop ──────────────────┘
```

The journal runs silently alongside sage-cognitive. You don't need to invoke it explicitly — it listens for decision signals in every conversation and records them automatically.

---

## Decision Capture

### Signal Detection

The journal detects two types of decisions:

**Explicit decisions** — user directly states a choice:
- "I decided to..."
- "We're going with..."
- "I told him we'll..."
- "I chose X over Y"

**Implicit decisions** — inferred from behavior and context:
- User describes an action taken without explaining why → record the decision embedded in the action
- User dismisses an option someone else proposed → record the rejected alternative
- User changes direction on a previous plan → record the pivot and what triggered it

### Decision Record Format

Every captured decision is stored with five fields:

```
WHAT        The decision itself. One sentence, action form.
WHY         The stated or inferred reasoning. What made this the right call?
ALTERNATIVES What else was on the table? What was NOT chosen?
CONTEXT     What was the environment? Time pressure, stakeholder dynamics, info available?
CONFIDENCE  How certain was the user? (certain / leaning / uncertain / forced)
```

### Example: Explicit Decision

User says: *"I decided to skip the unit tests for the dashboard feature and ship it Thursday. The demo is more important right now."*

Captured record:
```
WHAT         Skipped unit tests for dashboard feature; shipped Thursday
WHY          Demo deadline took priority over test coverage
ALTERNATIVES Write tests first and delay Thursday ship; write minimal smoke tests
CONTEXT      Demo coming up, stakeholder expectations set, time pressure
CONFIDENCE   Leaning (acknowledged the trade-off)
TYPE         Technical / Reversible (tests can be written post-ship)
```

### Example: Implicit Decision

User says: *"Prepared the PULSE topology diagram, for Bob."*

Captured record:
```
WHAT         Took on CTO-facing deliverable directly (topology diagram for Bob)
WHY          Not stated — inferred: strategic visibility, PULSE importance
ALTERNATIVES Delegate to team member; route through Shawn
CONTEXT      PULSE is new project; Bob is CTO; direct delivery bypasses normal chain
CONFIDENCE   Certain (deliberate action, not accidental)
TYPE         Strategic / Reversible
```

---

## Decision Taxonomy

### By Domain

| Type | Examples | Review horizon |
|------|----------|----------------|
| **Technical** | Architecture choice, tech stack, skip tests | 2–4 weeks |
| **People** | Who gets which task, feedback delivered, hire/no-hire signal | 1–3 months |
| **Strategic** | Project prioritization, resource allocation, scope changes | 3–6 months |
| **Communication** | What to tell whom, when, how much context to share | 1–2 weeks |

### By Reversibility (Amazon's framework, adapted)

**Two-way door** — reversible, low stakes, decide fast:
> Reassigning a task, choosing a library, trying a new process

**One-way door** — hard to undo, high stakes, slow down:
> Architectural rewrites, letting someone go, committing to a roadmap to external stakeholders

When a one-way door decision is captured, add a brief flag: *"This is a one-way door. What would make you reverse it?"*

### By Decision Mode

| Mode | Signal | What it reveals |
|------|--------|-----------------|
| **Deliberate** | User weighs options, asks for input | Decisions made with clarity |
| **Reactive** | Response to external pressure or surprise | Decisions under stress — track carefully |
| **Delegated** | User hands off and doesn't revisit | Trust in others, or avoidance? |
| **Default** | No choice made, status quo maintained | Inaction is also a decision |

---

## Pattern Detection

After 10+ decisions are logged, begin running pattern analysis. Surface patterns — don't diagnose them.

### Decision Tendencies

Look for consistent skews across the decision history:

| Axis | Signal pattern |
|------|---------------|
| Speed vs. Deliberation | How often does the user decide within minutes vs. sleep on it? |
| Conservative vs. Aggressive | Does the user default to the safer option when uncertain? |
| People-first vs. Task-first | When trade-offs involve team vs. delivery, which wins? |
| Own judgment vs. Consensus | Does the user seek input before deciding, or after? |
| Visible vs. Behind-the-scenes | Does the user prefer credit or quiet impact? |

### Blind Spot Detection

Flag patterns that suggest recurring information gaps:

- **Missing stakeholder consideration**: Decisions that didn't account for a key person's reaction
- **Optimism bias**: Timelines or outcomes consistently more optimistic than reality
- **Sunk cost signals**: Continuing a course of action because of past investment, not future value
- **Confirmation seeking**: User only consults sources likely to agree with them
- **Urgency override**: Quality or completeness consistently sacrificed under time pressure

### Cognitive Bias Signals

When detected, name the bias gently, once. Don't repeat it:

```
Confirmation bias:    "You've checked with three people who all agreed. Is there anyone who'd push back?"
Sunk cost:            "You've mentioned how much time went into this twice. Is that affecting what you do next?"
Availability bias:    "The last time this went wrong is fresh. Is this situation actually similar?"
Recency bias:         "The last few decisions went [well/badly]. Does that pattern hold here?"
```

---

## Review Cadence

### Weekly Review (every Friday, or end of work week)

Three questions, answered from the decision log:

1. **What decisions did I make this week?** (list the captured records)
2. **Which decision am I least confident about in hindsight?** (flag for follow-up)
3. **Is there a pattern I keep seeing?** (one observation, not a diagnosis)

Output format — concise, no filler:
```
📋 Decision Week in Review — [date]

Decisions made: 4
  → Technical (2): [brief labels]
  → People (1): [brief label]
  → Strategic (1): [brief label]

Worth watching: [one decision to revisit]
Pattern signal: [one pattern, if present]
```

### Monthly Review (retrospective on 30-day-old decisions)

Pull decisions from ~30 days ago. For each significant one, ask:
- **What actually happened?** Does the outcome match the reasoning at the time?
- **What information did you not have then that you have now?**
- **Would you make the same call again?**

This is where learning happens. Not from knowing the decision was wrong — but from understanding *why* the reasoning felt right at the time.

### Quarterly Review (decision style drift)

Look across the full decision history and ask:
- Is the **speed** of decisions changing? (faster? slower? in which domains?)
- Is the **confidence level** shifting? (more certain vs. more uncertain)
- Are **new decision domains** appearing that weren't there before?
- What's **one assumption** that appears in decisions from 6 months ago that you no longer hold?

---

## Follow-up System

For every captured decision, set a follow-up based on type:

| Decision type | Follow-up trigger |
|--------------|------------------|
| Technical | 2–3 weeks after shipping |
| People | 4–6 weeks after the conversation or action |
| Strategic | End of quarter |
| Communication | 1 week after delivery |

Follow-up prompt (gentle, not interrogating):
> "Three weeks ago you decided [WHAT]. How did that land?"

If the user answers, log the outcome alongside the original record. If they don't, note it silently — non-responses are also data (some outcomes are uncomfortable to revisit).

---

## Anti-Patterns

- **Don't record every micro-choice**: "I chose to write the email in English" is not a decision worth logging. Only decisions with real alternatives and real stakes.
- **Don't moralize**: A decision isn't "good" or "bad" until outcome is known. The journal is neutral.
- **Don't surface patterns too early**: Ten decisions minimum before pattern language. Two data points are not a pattern.
- **Don't repeat bias flags**: Name it once. If the user ignores it, drop it. Nagging kills trust.
- **Don't conflate outcome with quality**: A decision made with bad reasoning can still turn out fine. A decision made with good reasoning can fail. Track both separately.
- **Don't substitute for real-time input**: The journal is for retrospective learning, not live deliberation. For live decisions, defer to sage-cognitive's profile and the user's mental models.
- **Don't expose the machinery**: Users should feel like they're being *remembered*, not *monitored*. Surface insights naturally, not as database outputs.

---

## Integration with sage-cognitive

This skill reads from sage-cognitive's behavioral profile and writes back to it:

**Reads**:
- Decision tendency profile (from Phase 1: OBSERVE)
- User's stated decision style (from Phase 0: KNOW)
- Known cognitive preferences (speed, quality, people-first)

**Writes**:
- Confirmed or updated decision tendencies → sage-cognitive archive tier
- Detected bias signals → sage-cognitive working tier (expires in 14 days if not reinforced)
- Pattern-level insights → sage-cognitive core tier (only when pattern is strong and consistent)

**Coordination rule**: If sage-cognitive's Mirror (Phase 2) already reflected a decision pattern this session, sage-decision-journal should not surface the same pattern. One mirror per day is enough.
