---
name: tastes
version: 0.1.0
description: Cultivate aesthetic judgment through conversation and memory. Build and maintain TASTES.md — the missing layer between SOUL.md and SKILL.md.
homepage: https://tastes.md
metadata: {"tastesmd":{"category":"creative","source":"https://github.com/tastesmd/tastes.md"}}
---

# TASTES.md

Teach your agent aesthetic judgment. Distill taste from memory and conversation into a compact, executable file.

## Skill Files

| File | URL |
|------|-----|
| **SKILL.md** (this file) | `https://tastes.md/SKILL.md` |

**Install:**
```bash
mkdir -p ~/.openclaw/skills/tastes && curl -fsSL https://tastes.md/SKILL.md -o ~/.openclaw/skills/tastes/SKILL.md
```

**Or just read it from the URL above.**

---

## Setup

On first activation, check if AGENTS.md contains `## Aesthetic Judgment`. If not, append:

```markdown

## Aesthetic Judgment

When doing design, creative, or artistic work — anything requiring aesthetic judgment such as UI design, visual assets, layouts, color choices, typography, animation, branding, or creative direction — read `TASTES.md` if it exists and apply its constraints to your output.
```

Tell the human: "Added aesthetic judgment rules to AGENTS.md."

---

## What This Skill Does

You can build and maintain a TASTES.md file — a compact set of aesthetic constraints distilled from memory and conversation. Max 500 tokens.

TASTES.md is not a style guide. It encodes aesthetic judgment in a format you execute with precision.

---

## Building TASTES.md

When the human says "build my TASTES.md", "start my taste file", or similar:

### Step 1: Mine memory for aesthetic signals

Three sources, in this order:

**a) MEMORY.md** — read directly. Look for aesthetic preferences, design decisions, or style references already in long-term memory.

**b) Recent daily logs** — read today's and yesterday's `memory/YYYY-MM-DD.md` for recent aesthetic signals.

**c) Old daily logs via memory_search** — most signals hide here. Run searches to mine the full history:

```
memory_search("rejected design style visual")
memory_search("preferred aesthetic look feel")
memory_search("animation timing too slow too fast")
memory_search("color palette choice")
memory_search("typography font choice")
memory_search("reference inspiration artist designer")
memory_search("looks wrong feels off not right")
memory_search("looks good keep this perfect")
```

Adapt queries based on what surfaces. If results reveal specific domains (e.g. the human does frontend work), add targeted searches:

```
memory_search("UI layout spacing negative space")
memory_search("interaction hover transition easing")
```

Repetition across different dates is the strongest evidence of a genuine preference.

### Step 2: Conversation

Share what you found. Confirm, correct, expand through natural conversation — not a checklist:

- "Searching your memory, I found you rejected gradient backgrounds at least three times. Is that a hard rule?"
- "You mentioned Teenage Engineering in two separate conversations. What draws you to their work?"
- "I couldn't find much about your color preferences. What does a 'right' palette look like to you?"

### Step 3: Draft

Write TASTES.md following the format rules below. Show the draft. Apply the human's corrections. Save.

---

## TASTES.md Format

```markdown
# TASTES.md

## REJECT
- Never [specific thing to avoid].
- Never [specific thing to avoid].

## REQUIRE
- [Active verb] [specific constraint].
- [Active verb] [specific constraint].

## WHEN AMBIGUOUS
- [Judgment heuristic for unclear situations].
- Orient toward: [reference] ([domain]), [reference] ([domain]).
```

### Writing rules

- Every REJECT starts with "Never".
- Every REQUIRE starts with an active verb: Use, Maintain, Ensure, Pair.
- Specific values in backtick code format: `#1a1a1a`, `200ms`, `cubic-bezier(0.2, 0.8, 0.2, 1)`.
- One sentence per entry. No explanations. No "because" clauses.
- REJECT first, REQUIRE second, WHEN AMBIGUOUS last.
- Strongest convictions first within each section.
- Max 500 tokens total. If over budget, merge or cut the weakest entry.
- No generic design advice. Only what makes THIS human's taste distinctive.
- No semantic overlap between entries. If two entries mean roughly the same thing, merge them.

---

## Updating TASTES.md

When the human says "update my taste", "calibrate", or "distill":

1. Run `memory_search` with aesthetic queries — focus on dates since last update.
2. Check recent daily logs for new aesthetic signals.
3. Propose additions, modifications, or removals with evidence.
4. Apply only what the human approves.

Direct updates also work:
- "Add to my taste: never use sans-serif for body text."
- "Remove the gradient rule."

Apply immediately and confirm.

---

## During Creative Work

When TASTES.md exists and you are doing creative work:

- Check output against REJECT entries before presenting.
- Apply REQUIRE entries to relevant decisions.
- If the human overrides a rule, mention it: "Noted — you accepted a gradient here. Want me to adjust that rule?"

---

## Commands

| Say this | What happens |
|----------|--------------|
| **"Build my TASTES.md"** | Mine memory + conversation to create initial file |
| **"Update my taste"** | Search for new signals, propose changes |
| **"Show my TASTES.md"** | Display current file with token count |
| **"Why this choice?"** | Explain which entry influenced a decision |
| **"Override"** | Accept output that violates TASTES.md |
| **"Taste check"** | Audit current output against all entries |

---

## Boundaries

- TASTES.md governs aesthetics only. Never override function, accessibility, or performance.
- If taste conflicts with usability, surface the conflict. Never silently sacrifice either.
- Never auto-update TASTES.md. Always propose and wait for approval.

---

## Uninstall

If removed, delete the `## Aesthetic Judgment` section from AGENTS.md. Do not delete TASTES.md — it belongs to the human.

---

**Learn more:** [tastes.md](https://tastes.md) · [Manifesto](https://github.com/tastesmd/tastes.md/blob/main/MANIFESTO.md) · [GitHub](https://github.com/tastesmd/tastes.md)

**License:** MIT-0
