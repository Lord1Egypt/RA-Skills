# Agent Playbook — Decision Guide for AI Agents

> This file is the **agent-specific** decision layer. It extracts the "how should an agent think about this?" guidance from SKILL.md into one place.
> Humans can read it too — it doubles as a transparency document showing how the agent makes decisions.

---

## Routing decision tree

When the user sends a message, follow this order:

```
1. Is it a structured data input (CSV/JSON/SQL/MD-table)?
   YES → Format Auto-Detect fast path (Mode 2, skip Perception)
   NO ↓

2. Does it match a Review trigger (审查/audit/polish/a11y)?
   YES → Review Mode (independent of production modes)
   NO ↓

3. Does it match Mode 1 triggers (PPT/slides/deck/演讲)?
   YES → Mode 1 (Presentation)
   NO ↓

4. Does it match Mode 2 triggers (APP/界面/原型/landing)?
   YES → Mode 2 (Prototype)
   NO ↓

5. Does it match Mode 3 triggers (动效/动画/motion)?
   YES → Mode 3 (Animation)
   NO ↓

6. Ambiguous → Ask once with focused options (see below)
```

**Key principle:** Ask once, not repeatedly. A 30-second question saves an hour of rework.

---

## When to ask vs infer

### Ask when:
- The request is genuinely ambiguous between two modes ("帮我做个展示" could be deck or prototype)
- Critical information is missing AND cannot be safely inferred (audience, brand, content scope)
- The user's request could map to 3+ distinct visual directions

### Infer when:
- The request has a clear dominant signal ("做一份 PPT" → Mode 1, no question needed)
- The user has provided partial constraints that narrow the space ("像 Linear 的 dashboard" → Mode 2 + Linear tokens)
- The cost of asking exceeds the cost of a wrong guess (trivial tweaks, follow-up edits)

### The "Design Read" pattern

When you infer, **state your inference** before generating:

```
Reading this as: [product landing] for [technical buyers],
with a [conversion-first] visual language,
leaning toward [swiss-grid theme + Stripe tokens].
```

This lets the user correct a wrong assumption before any heavy generation happens.

---

## Fallback decision matrix

| Situation | Primary action | Fallback | When to escalate |
|---|---|---|---|
| WebFetch fails for URL-to-brand | Try catalog lookup | Ask user for 3-5 brand tokens manually | User can't provide tokens |
| Theme CSS not found | Use `corporate-clean` | — | — |
| Template directory not found | Build from single-page layouts | — | — |
| runtime.js fails to load | Deck still works as static slides | — | — |
| PDF export fails | Offer manual "Print to PDF" | — | — |
| Brand DESIGN.md has no palette | Derive from brand name dominant color | Ask user for primary color | — |
| Generation produces syntax errors | Auto-retry with fix | Swap simplified component | 3 failures → escalate to user |
| User asks for non-design task | Explain scope, redirect | — | — |

**Escalation rule:** After 3 consecutive failures on the same issue, stop. The problem is likely conceptual (wrong approach), not a typo. Ask the user.

---

## Context management for long sessions

When context window is tight, drop in this order:

1. **Keep** — current task goal, active design system tokens, user's latest request
2. **Keep** — technical constraints (React version hashes, component APIs)
3. **Compress** — earlier exploration steps after a phase completes
4. **Drop** — rejected design variations, superseded planning notes, duplicated information

**State separation:** Treat yourself as stateless. All persistent state lives in files (HTML, JSON, localStorage), not in conversation memory. When resuming work, re-read the files.

---

## Error recovery hierarchy

1. **Auto-retry on syntax errors** — console output points at the line; fix and re-render immediately
2. **Graceful degradation** — if a component refuses to render, swap in a simplified fallback
3. **State checkpoint** — before destructive edits, copy the file
4. **Escalate after 3 failures** — conceptual issue, not a typo

---

## Token budget discipline

| Mode | Budget | Split strategy if exceeded |
|---|---|---|
| Mode 1 (deck) | 4K-8K tokens | Generate CSS separately from HTML body |
| Mode 2 (prototype) | 6K-12K tokens | Split JSX modules, generate incrementally |
| Mode 3 (animation) | 4K-10K tokens | Generate keyframe definitions separately |
| URL-to-brand | 500-1K tokens | Only extract essential tokens |
| Iteration | 500-2K tokens | Output only changed sections |

---

## Anti-patterns for agents

- ❌ Generating a complete deliverable without showing CP1-CP4 checkpoints
- ❌ Asking more than 3 rounds of questions (user fatigue)
- ❌ Retrying the same approach 3+ times without diagnosing root cause
- ❌ Using literal hex colors instead of design tokens
- ❌ Writing a fresh `.slide` layout from scratch instead of copying from `templates/single-page/`
- ❌ Using React + Babel inside a deck (decks are static)
- ❌ Presenting broken work — fix before `done`

---

## Communication style

- **Lead with the answer or action**, not the reasoning. The user sees the result first.
- **State inferences explicitly** so the user can correct early.
- **Don't announce snips or context management** — they just happen.
- **Use the user's language** — if they write in Chinese, respond in Chinese.
- **Reference patterns by name** when applying them: "Using the **Pitch flow** pattern (P1)."

---

## Relationship to SKILL.md

| SKILL.md section | Agent playbook section |
|---|---|
| Intent Router | Routing decision tree |
| When the request is ambiguous | When to ask vs infer |
| Runtime Fallback Strategies | Fallback decision matrix |
| Token Budget Guidelines | Token budget discipline |
| Context Management (mode-2-prototype.md) | Context management for long sessions |
| Design for Failure (mode-2-prototype.md) | Error recovery hierarchy |
| Anti-Patterns (mode-2-prototype.md) | Anti-patterns for agents |

The agent playbook is a **condensed decision reference** — SKILL.md remains the authoritative source for full context, rules, and examples.
