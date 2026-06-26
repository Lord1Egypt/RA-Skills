# Rule Quality Guide

Use this guide before adding or updating any rule in `CLAUDE.md`.

## A Good Rule Has These Properties

- reusable across multiple future tasks
- understandable without the original session
- concise enough to scan quickly
- specific enough to change behavior
- stable enough that it is unlikely to flip next session
- worth occupying scarce space in `CLAUDE.md`

## A Weak Rule Usually Looks Like This

- tied to one bug or one ticket
- only relevant to one file or path
- based on temporary timing or current urgency
- just a polite confirmation rather than a true preference
- obvious enough that it adds no guidance

## Keep These

- `Prefer concise final answers by default [stable]`
- `Show compare-first only when prompt refinement materially changes execution [stable]`
- `For risky code changes, state verification method explicitly [tentative]`

## Reject or Compress These

- `Today skip tests`
- `This file was hard to read`
- `Use the same approach as the login bug from earlier`
- `The user said perfect after the answer`
- `Do not store full prompt text`
- `Never keep exact prompt text`

The last two should be merged into one concise rule instead of stored separately.

## Compression Heuristics

Before appending a rule, ask:

1. Does an existing rule already cover the same behavior?
2. Can two related rules be merged into one broader reusable rule?
3. Is this really a rule, or just a note from the current task?
4. Would this still be useful a month from now?

If the answer to 3 or 4 is no, do not store it in `CLAUDE.md`.

Also ask:

5. Can I improve the existing guidance by replacing or merging rules instead of adding one more?

If yes, prefer the smaller replacement.

## Per-Session Proposal Budget

One session should usually propose no more than 3 new rules.

Zero new rules is often the best result.

If more candidates appear:

- keep the strongest and most reusable ones
- merge overlapping candidates
- discard weaker session-specific notes

If the target `CLAUDE.md` section is already over budget:

- compact first
- do not append new rules by default
- only add beyond budget when the user explicitly approves

## Scope Test

Write to global `CLAUDE.md` only if the rule is about:

- response style
- collaboration workflow
- tool usage preference
- prompt/confirmation behavior

Write to project `CLAUDE.md` only if the rule is about:

- coding conventions
- architecture
- testing strategy
- repository-specific team practices
