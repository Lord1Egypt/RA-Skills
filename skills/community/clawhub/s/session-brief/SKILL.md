---
name: session-brief
description: Produce a compact, complete context dump of the current session directly in chat. Use when the user wants the current conversation summarized for reference, asks for a context dump, says the chat is bloated or slow, or wants a concise session state without creating files or migrating to a new chat.
---

# Session Brief

Dump the current session context directly in chat. Do not create a file unless the user explicitly asks.

The brief should be compact but complete enough for the user to understand the current state without rereading the whole thread.

## Output Contract

Return one copyable Markdown block with:

- current goal or topic
- key decisions and constraints
- what has already been done
- current state
- important files, repos, URLs, branches, commands, or artifacts
- open questions, blockers, or next likely steps
- anything the user explicitly wanted preserved

Keep it factual. Separate confirmed state from assumptions.

## Compression Rules

- Preserve decisions, constraints, state, names, paths, URLs, commands, and unresolved work.
- Drop greetings, transient status updates, repeated explanations, and dead ends unless they explain the current state.
- Reference existing artifacts by path, URL, commit, PR, or issue instead of restating their full contents.
- Include exact file paths and commit hashes when they matter.
- Do not include secrets, tokens, private credentials, or unnecessary personal data.

## Shape

Use this structure unless the user asks for another format:

```markdown
Session brief:

Current goal:
...

Decisions and constraints:
...

Done:
...

Current state:
...

Important references:
...

Next:
...
```

For tiny sessions, compress to a short paragraph.
