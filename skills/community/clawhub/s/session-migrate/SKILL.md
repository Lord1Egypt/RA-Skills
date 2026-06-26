---
name: session-migrate
description: Produce a copyable handoff prompt so a fresh agent can continue the current conversation in a new chat. Use when the user wants to continue elsewhere, migrate sessions, recover performance from a bloated chat, or prepare a complete next-session prompt with goals, completed work, remaining work, current state, files, repos, URLs, branches, commands, blockers, and suggested skills.
---

# Session Migrate

Create a handoff prompt for a new chat. Output it directly in chat as a copyable Markdown block. Do not write a document unless the user explicitly asks.

The prompt should let a fresh agent continue from the current point with minimal re-explaining.

## Workflow

1. Identify what the next session is meant to do.
   If the user gave a focus, tailor the handoff to that. Otherwise assume the next session should continue the current goal.

2. Summarize only durable context.
   Include decisions, current state, files, repos, URLs, commands, branches, commits, artifacts, and constraints that affect the next agent.

3. Include continuation instructions.
   Tell the next agent what has been done, what remains, what to verify first, and which skills or workflows may help.

4. Avoid duplication.
   Reference existing artifacts, commits, diffs, docs, issues, PRs, and URLs instead of copying their contents.

## Required Sections

Use this structure:

```markdown
Continue this session:

Role:
You are continuing an existing agent session. Use the context below as the source of truth.

Goal:
...

Current state:
...

Completed:
...

Remaining work:
...

Constraints and preferences:
...

Important files and references:
...

Suggested skills:
...

First actions:
...
```

## Rules

- Make the output directly pasteable into a new chat.
- Keep it compact, but do not omit state the next agent would need to avoid redoing work.
- Preserve the user's wording when it contains important constraints or preferences.
- Include exact paths, URLs, branches, commits, PRs, and commands when relevant.
- Say what was verified and what was not.
- Do not invent completed work.
- Do not include secrets, tokens, credentials, or private data unless the user explicitly asks and it is safe.
- If the next agent should stay read-only, say that clearly.
