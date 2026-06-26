---
name: self-improving-session
description: Extracts durable workflow preferences and project conventions from a session, then proposes the smallest valid update to global or project CLAUDE.md files. Trigger when the user asks to remember rules, when repeated preference patterns appear, or at session end for non-trivial sessions.
---

# self-improving-session

> Good session learning captures durable guidance, not conversational residue.

Extract reusable lessons from the current session and propose the smallest valid update to `CLAUDE.md`. The goal is not to remember everything. The goal is to preserve only rules that improve future sessions while keeping the rule set small.

This skill works standalone.
It can learn from ordinary sessions or from sessions shaped by `self-improving-prompt`.

When paired together:
- `self-improving-prompt` shapes task framing and execution behavior
- `self-improving-session` reviews the resulting session and extracts durable workflow rules

This skill should learn from behavior patterns, corrections, and repeated outcomes, not from storing the refined prompt text itself.

## Security and Runtime

- Instruction-only skill; no bundled scripts or external services required
- No credentials, API keys, or network access required for normal use
- Does not modify system configuration; may propose writing to `CLAUDE.md` files after user confirmation
- Optional session-end automation belongs in README only and is not required for core skill behavior

## Quick Reference

| Signal | Action |
|--------|--------|
| Explicit user correction | Add or update a `[stable]` rule immediately |
| Explicit durable project rule | Add as `[stable]` project rule |
| Repeated preference seen 2 times across meaningfully different tasks | Add as `[tentative]` |
| Repeated preference seen 4 times across multiple task contexts | Upgrade to `[stable]` |
| One-off scenario-specific choice | Skip |
| Full prompt text | Never store |
| Code facts, file paths, temporary state | Never store |
| Nothing worth learning | Say so directly |

## Core Principle

Prefer under-learning to over-learning. A noisy `CLAUDE.md` harms future sessions more than a missed weak signal.
The best outcome is often:

- no change, or
- one compact replacement that improves existing guidance without increasing rule count

## Step 1: Scan the Session

Look for two categories:

### A. Workflow preferences and corrections

- Explicit user corrections
- Repeated output-format preferences
- Collaboration-flow preferences
- Tool-usage preferences
- Repeated `self-improving-prompt` workflow choices

Only treat a signal as durable if it appears reusable across tasks.

### B. Project rules and conventions

- Coding conventions
- Architecture decisions
- Tech-stack preferences
- Testing and deployment rules
- Team or repo-specific collaboration conventions

## Step 2: Filter Noise

Skip:

- One-off debugging details
- Temporary workarounds
- Facts already derivable from code
- Rules already documented clearly elsewhere
- Full prompts produced by `self-improving-prompt`
- Generic praise such as "perfect" or "yes exactly" unless it clearly confirms a reusable workflow rule

Do not learn courtesy language as a durable preference.
See `references/rule-quality.md` for what counts as a strong, reusable rule versus noise.

## Step 3: Classify Scope

Choose the destination by scope:

- Cross-project workflow rules -> `~/.claude/CLAUDE.md`
- Project-specific engineering conventions -> project `CLAUDE.md`
- Temporary lessons or one-off incident notes -> separate task notes, not `CLAUDE.md`

Do not mix personal workflow rules into a project convention section.

## Step 4: Apply Confidence Rules

Use one consistent threshold:

- Explicit correction or explicit permanent instruction -> `[stable]`
- Same reusable preference observed 2 times across meaningfully different tasks -> `[tentative]`
- Same reusable preference observed 4 times across multiple task contexts -> `[stable]`

If the evidence is weaker than that, do not learn it.

## Step 5: Merge Carefully

- Deduplicate rules with the same meaning
- Merge wording variants into one concise rule
- Do not let a new `[tentative]` overwrite an existing `[stable]`
- Only explicit correction can rewrite an existing `[stable]`
- Keep the total rule set compact
- Prefer compressing or replacing low-quality rules rather than appending near-duplicates
- Prefer replacing multiple weaker rules with one stronger rule when possible
- If existing rules already cover the behavior, propose no change

## Rule Budget

To prevent `CLAUDE.md` bloat:

- Keep global workflow rules under about 20 bullets
- Keep project-specific convention rules under about 15 bullets unless the project genuinely requires more
- If a section grows too large, merge or compress instead of appending
- A single session should usually propose no more than 3 new rules unless the user explicitly asks for broader guidance cleanup
- If the target `CLAUDE.md` section is already over budget, compact first and do not append new rules unless the user explicitly approves
- Zero new rules is a normal and healthy outcome

## Confidence Markers

- `[tentative]`: observed twice and likely reusable, but not well validated yet
- `[stable]`: explicitly stated or validated repeatedly
- `[corrected: YYYY-MM-DD]`: old rule superseded by explicit user correction

Example:

```markdown
- Prefer concise final answers by default [stable]
- Show refined prompts only when refinement materially improves execution [stable]
- Write scope explicitly for risky code tasks [tentative]
- ~~Always use popup confirmation~~ -> Use compare-first only when refinement adds substantial value [corrected: 2026-04-14]
```

## Event Consumption from self-improving-prompt

If `self-improving-prompt` emits abstract events, use them as weak evidence only.

Examples:

- `choose_refined`
- `choose_original`
- `explicit_no_compare`
- `explicit_compare_first`

Rules:

- A single event is not enough to create a durable rule unless paired with an explicit verbal instruction
- Repeated events may support a `[tentative]` or `[stable]` rule using the thresholds above
- The refined prompt may have shaped the session, but the refined prompt text itself should not be stored as a durable rule
- Never store the refined prompt text itself

## Confirmation Before Writing

By default, show the user:

- new rules to add
- existing rules to update
- target file

Then wait for confirmation before writing.

Skip confirmation only when:

- the user explicitly says to update directly, or
- the skill is running automatically at session end with prior permission to write

If interactive confirmation is unavailable, fall back to plain-text confirmation.

## Output Format

When writing rules:

- Use concise markdown bullets
- Separate `Global Workflow Rules` from `Project Conventions`
- Keep each rule broadly reusable
- Include a confidence marker at the end
- Prefer the smallest valid update: no change, replacement, merge, or at most a few additions

Before adding a rule, validate it against `references/rule-quality.md`.

## Notes

- Do not store secrets, passwords, tokens, or sensitive personal data
- Do not store full prompt text
- Do not store temporary task state
- If there is nothing durable to learn, say so plainly

Optional session-end automation examples are documented in `README.md`. They are convenience setup, not a requirement of the skill itself.
