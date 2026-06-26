---
name: self-improving
description: Global, namespaced learning memory for OpenClaw. Use when users correct output, set stable preferences, ask what was learned, ask for memory stats, or request forgetting learned patterns. Keep memory cross-session, avoid context mixing, and enforce strict privacy boundaries.
metadata: {"openclaw":{"os":["darwin","linux","win32"]}}
---

# Self-Improving (Global + Namespaced)

Maintain global learning while preventing cross-project pollution.

## Storage Root

Store only in:

```text
~/.openclaw/self-improving/
  global/
    rules.md
    corrections.md
  contexts/
    <context-key>/
      rules.md
      corrections.md
      meta.md
  index.md
```

Never write outside this root unless the user explicitly asks.

## Context Key

Compute a stable `context-key` in this order:
1. If in a git repo, use `<host>-<owner>-<repo>` when available.
2. Else use sanitized absolute workspace path.
3. If user gives explicit project scope, append that suffix.

Use `global/*` only for cross-context rules.
Use `contexts/<context-key>/*` for local rules.

## Load Strategy

Default read set:
- `global/rules.md`
- active `contexts/<context-key>/rules.md`

When user asks cross-project/global questions, read additional context folders and cite exact source file.

## Learning Triggers

Learn only from explicit signal:
- direct correction
- explicit preference
- repeated correction (3 times)

Do not learn from silence, guesses, or one-off temporary requests.

## Promotion Gates

Write every candidate to active `corrections.md`.
Promote to context `rules.md` only after explicit confirmation.
Promote to global `rules.md` only when:
- user says it is global, or
- rule is confirmed in 2+ different contexts.

Detailed procedures: `operations.md`.

## Conflict Handling

Conflict precedence:
1. active context rule
2. global rule
3. ask user if ambiguity remains

Record conflicts and resolutions in corrections logs.
Detailed policy: `conflict-resolution.md`.

## Retention and Compaction

Keep files concise, deduplicated, and auditable.
Apply retention windows and archive stale entries by policy.
Detailed policy: `retention-policy.md`.

## Safety Guardrails

Never store:
- credentials or secrets
- financial, medical, biometric, identity-sensitive data
- third-party private information

If uncertain, ask before writing.

## User Requests

- "What did you learn?" -> recent corrections (active context + global summary)
- "Show my rules" -> active context rules and global rules
- "Memory stats" -> counts by scope, file, and last update
- "Forget X" -> remove in active context, then ask about global/all contexts
- "Forget everything" -> ask scope first: active context, global only, or all contexts

Do not auto-backup before deletion unless user asks for export.

## Response Transparency

When behavior uses learned memory, cite source file:
- `global/rules.md`
- `contexts/<context-key>/rules.md`
