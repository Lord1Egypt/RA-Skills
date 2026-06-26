---
name: session-learner
description: Use when a session reveals stable user preferences, workflow corrections, or project conventions that should be preserved for future sessions. Also use when user explicitly asks to remember rules, update guidance, or summarize learnings.
---

# session-learner

> A good learning loop stores stable preferences and rules, not ephemeral artifacts.

Extract durable, reusable lessons from the current session and merge them into CLAUDE.md so future sessions are more aligned. Works as a closed loop with `prompt-refiner`, which generates preference signals from user choices.

## Quick Reference

| Signal | Action |
|--------|--------|
| Stable repeated preference | Learn as rule |
| Explicit user correction | Learn immediately |
| One-off different choice | Usually do not learn |
| Full prompt text | Never store |
| Code facts / file paths | Never store |
| Secrets / keys / passwords | Never store |
| Nothing worth learning | Say so, don't force it |

## Core Flow

### Step 1: Scan the session

Review the whole session for two categories:

**A. Workflow preferences and corrections**
- User corrections ("don't do that", "stop ...")
- User-confirmed non-obvious approaches ("yes, exactly", "perfect")
- Output format, communication style, and collaboration flow preferences
- Tool usage guidance
- `prompt-refiner` choice preferences (prefers refined vs original, wants compare-before-execute)

**Judging prompt-refiner preference signals:**
- Repeatedly choosing the same version → store as stable preference
- One-off different choice → don't overfit, may be scenario-specific
- Explicit verbal correction ("don't show me the original anymore") → promote immediately to rule

**B. Project rules and conventions**
- Coding conventions (naming, formatting, comment style)
- Architectural conventions (directory structure, layering, patterns)
- Stack preferences (framework and library usage)
- Testing strategy, deployment flow, and other project-specific rules

For detailed examples of what to learn vs skip, see `references/learning-rules.md`.

### Step 2: Filter noise

Skip:
- One-off debugging details (code and git history capture them)
- Information directly derivable from code (paths, signatures)
- Temporary task state
- Rules already present in CLAUDE.md
- Full prompt text produced by `prompt-refiner` (learn rules and preferences only, never the entire prompt body)

Keep only information that will guide future sessions.

### Step 3: Read current CLAUDE.md

Choose target file by scope:
- **Global rules** → `~/.claude/CLAUDE.md`
- **Project-specific rules** → project `CLAUDE.md`

If a project file is needed and missing, create it.

### Step 4: Merge intelligently

- **Deduplicate**: skip equivalent rules
- **Update**: replace outdated/conflicting rules with newer user preference
- **Classify**: place rules in the most appropriate section
- **Compress**: keep rules short and clear in bullet format

### Step 5: Confirm changes

Show the user:
- Rules to add
- Rules to update (old → new)
- Target file

Wait for confirmation before writing, unless user says "update directly" or the skill is running from an automatic SessionEnd hook.

## Output Format

When updating CLAUDE.md:
- Use markdown bullets (`-`)
- Keep each rule concise
- Include enough context so future Claude understands why it exists
- If the rule comes from a correction, briefly include the reason

## Integration with prompt-refiner

- `prompt-refiner` is a primary source of workflow preference signals.
- Learn the choice pattern (e.g., "user always picks refined version"), not the generated prompt text.
- Over time, the accumulated preferences make `prompt-refiner` increasingly aligned with user habits.

## Notes

- Never record secrets, keys, passwords, or private personal data
- Never store obvious programming common sense
- If the session has nothing worth preserving, say so directly
- Keep CLAUDE.md tidy; if a section grows too large, merge or compress rules
