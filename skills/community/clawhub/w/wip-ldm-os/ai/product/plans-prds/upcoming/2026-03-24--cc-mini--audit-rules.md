# Plan: ldm audit-rules (instruction dead weight detection)

**Date:** 2026-03-24
**Author:** cc-mini (with Parker)
**Issue:** #183
**Status:** Upcoming

## Context

Our CLAUDE.md is 368 lines. Some rules are defaults the model already follows. Some conflict with each other. Some were added to fix one bad session. Some are reference data, not instructions. Over-prompting makes output worse, not better.

Inspiration: Ole Lehmann (@itsolelehmann) on cutting half his Claude setup and getting better output. Anthropic's own team found their scaffolding was making Claude worse.

## What to build

`ldm audit-rules` (or `ldm doctor --rules`): reads all instruction files, classifies each rule, recommends cuts.

### Input files

1. `~/.ldm/shared/rules/` (when created)
2. `~/.ldm/agents/*/rules/` (when created)
3. `~/.claude/CLAUDE.md`
4. `~/.claude/rules/` (when populated)
5. `~/.openclaw/workspace/TOOLS.md`
6. Any skills with instruction content

### Five checks per rule

| # | Check | Example of what gets flagged |
|---|-------|-----|
| 1 | Default behavior? | "Read files before editing" ... model already does this |
| 2 | Conflicts? | "Be concise" + "Always explain your reasoning" |
| 3 | Duplicates? | Same rule in CLAUDE.md and TOOLS.md |
| 4 | One-off fix? | Rule added after one bad session, not a general principle |
| 5 | Vague? | "Use a good tone" ... interpreted differently every time |

### Output

```
=== AUDIT RESULTS ===

CUT (12 rules):
  - "Be careful not to introduce security vulnerabilities" ... default behavior
  - "Read files before editing" ... default behavior
  - "Keep solutions simple" ... too vague, interpreted differently each time
  ...

CONFLICTS (3 pairs):
  - CLAUDE.md:45 "be concise" vs CLAUDE.md:180 "explain your reasoning"
  ...

DUPLICATES (5):
  - Boot sequence in CLAUDE.md:268 AND .ldm/agents/cc-mini/CONTEXT.md:1
  ...

KEPT (25 rules):
  - "Never use em dashes" ... not default, specific, necessary
  - "Never squash merge" ... not default, would squash otherwise
  ...
```

### Implementation

**File:** `wip-ldm-os-private/bin/ldm.js` (add `cmdAuditRules()`)

1. Discover all instruction files (glob for .md in known locations)
2. Extract individual rules (split by headers, bullet points, bold text)
3. Send to LLM with the 5-check prompt
4. Parse response into structured output
5. Display as report (no auto-delete)

### Process for using it

1. Run `ldm audit-rules`
2. Read the report
3. Delete flagged rules
4. Run 3 most common tasks with trimmed setup
5. Did output stay the same or get better? The deleted rules were dead weight.
6. Did something break? Add back just that one rule.

Goal: minimum viable setup. Simpler over time.

### When to run

- Before the CLAUDE.md split into rules/ (cut first, then organize)
- After adding 5+ new rules (periodic hygiene)
- After model upgrades (new model may handle things the old one needed rules for)
- Part of `ldm doctor` health check (optional, behind a flag)

## Caveats

- Requires LLM call. Not free. One call per audit is fine.
- Don't auto-delete. Preview only. Some "redundant" rules are belt-and-suspenders for critical things.
- "Default behavior" changes across model versions. What Opus 4.6 does by default, Haiku might not.
- Rules that look vague might have specific context in this org. "Be concise" means something specific to Parker (no trailing summaries). The audit should surface these for human review, not auto-cut.

## Related

- CLAUDE.md three-level split (workspace migration plan)
- rules/ folder architecture (.ldm/ as source, .claude/ as deployment target)
- #177 (plan-first workflow ... audit-rules could be a pre-planning step)
