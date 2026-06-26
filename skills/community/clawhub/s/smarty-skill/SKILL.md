---
name: smarty-skills-infra
description: Always active in every session. Learns user preferences from corrections and stated preferences, distills axioms, applies them as defaults. Makes every other skill better over time.
---

# Smarty Skills-Infra

You maintain a lightweight memory of this user's preferences, judgments, and working style. Memory operations never interrupt the user's workflow.

## At Session Start

Do this before addressing the user's request.

1. Read `memory/context-infra/context-profile.md` if it exists. Treat axioms as your own defaults — adapt when the situation differs. If missing, skip.

2. Check `memory/context-infra/observations.log`. If it has **15+ entries since the last `## Reflected` marker**, reflect *before* starting the user's task. Say exactly: *"Consolidating patterns from recent work."* Then follow **When Reflecting** below. Never interrupt a task to reflect.

On first session (no files exist), skip both steps and start observing.

## During Every Task

Record ONLY when a trigger fires:
- **Correction**: the user changes, rewrites, or redirects your output
- **Stated preference**: the user explicitly says they prefer, want, or dislike something
- **Retraction**: the user asks to forget, stop applying, or undo a remembered preference

Most tasks produce zero observations.

Append one line to `memory/context-infra/observations.log`:

```
YYYY-MM-DD | domain | signal | "Preference in ≤15 words."
```

- `domain`: organic label (e.g. code-style, architecture, communication, tooling, testing, workflow)
- `signal`: correction | stated-preference | retraction

**One observation per preference per session.**

**Bootstrap mode** (first 2 sessions) — cast a wider net: also note what the user accepts without comment and consistent choices.

Do not record: routine completions, project-specific facts, or one-time decisions.

## When Reflecting

Four steps:

1. **Group**: Read observations and profile. Cluster by domain, merging near-duplicates.
2. **Promote**: Promote when a pattern appears across **3+ distinct contexts** (different days or projects), has **no contradictions**, and is a **preference not a fact**. Each axiom must be specific enough to change behavior, yet general enough to apply across projects. See `references/profile-format.md` for format.
3. **Maintain**: Increment strength for reinforced axioms. Mark contradictions as contested. Remove axioms targeted by a retraction immediately — no threshold needed. Merge related axioms. Move unconfirmed (30+ days) to Dormant. Cap at 25 — if at cap, merge related axioms or demote lowest-strength to Dormant before promoting.
4. **Clean up**: Rewrite the profile. Rewrite `observations.log`: keep only un-promoted entries, prepend `## Reflected YYYY-MM-DD`.

Create missing files on first write. Never fail silently.

### Example

Observations:
```
2026-01-15 | code-style | correction | "User shortened verbose function name."
2026-01-18 | code-style | correction | "User rejected descriptive name, asked for abbreviation."
2026-02-01 | code-style | stated-preference | "User uses 2-3 word function names in new project."
```

3 distinct contexts, 0 contradictions — promoted:
```
- I prefer short, concise names — abbreviate rather than spell out.
  strength: 3 | domain: code-style | last-confirmed: 2026-02-01
```

NOT promoted if all observations were same-session — same-session repeats count as one context.
