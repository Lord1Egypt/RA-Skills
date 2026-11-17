# Trigger / boundary wording and the changelog template

## How to write the description (the primary trigger surface)

A good `description` contains three blocks, in this order:

1. **What it does** - one plain-English sentence.
2. **Triggers** - the concrete user phrasings that should fire it. Quote them.
3. **NOT-for** - the concrete cases it must *not* fire on, naming the skill that
   owns each. This block is what prevents mis-triggering.

Minimal shape:

```yaml
description: >-
  <what it does, one sentence>.
  Triggers: <2-4 quoted phrasings>.
  NOT for: <case A (use skill-x)>, <case B (use skill-y)>.
  <one line on network/secrets posture>.
```

Rules:

- Keep it under ~1024 characters; the host may truncate.
- Use full-width colons for Chinese values, or quote the whole value; a bare
  half-width "colon + space" inside an unquoted scalar breaks YAML silently.
- Name the sibling skill that owns each NOT-for case. "NOT for bug hunting" is
  weaker than "NOT for bug hunting (use code-review-assistant)".

## when_to_use

- One line of triggers, one line of explicit non-triggers.
- Mirror the description's NOT-for; it is read by a different host that may rely on
  `when_to_use` instead of `description`.

## Easy-to-confuse boundary

Besides one positive example and one negative example, add one **easy-to-confuse**
example that names the boundary skill. Three examples total are the minimum that
stops both mis-triggers and over-triggers.

## Changelog template (a first-class artifact)

Emit one table in the optimized file (or in the report). One row per change.

| # | Old -> New | Reason | Assumed? | P0? |
|---|---|---|---|---|
| 1 | `allowed-tools` removed from published schema | not a ClawHub field | yes - defaulted per platform matrix | no |
| 2 | long "Advanced" section sunk to `references/` | 8000-token budget | no - explicitly requested | yes |
| 3 | `context: fork` added | isolation as a subtask | yes - inferred from "subtask skill" | no |

Column meanings:

- **Old -> New** - the concrete change, quoting before/after.
- **Reason** - which criterion (T/L/C/B) or hard constraint (H#) drove it.
- **Assumed?** - `yes` means a default was inferred because the original lacked the
  information; state what was inferred. `no` means it was explicit or forced.
- **P0?** - `yes` means the change fixes a mis-trigger, a lost rule, or a budget
  breach; these must be called out to the user first.

Rule: every row that says `assumed: yes` must name the default that was inferred,
so the user can veto it.
