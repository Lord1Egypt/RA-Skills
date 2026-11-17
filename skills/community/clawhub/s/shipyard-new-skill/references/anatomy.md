# What a good skill looks like

## Front matter

```
---
name: weekly-report
description: Write the weekly team report from merged pull requests and closed issues. Use for "weekly report", "status update", "what did we ship", or "team summary".
---
```

- `name`: lowercase words joined by dashes, at most 64 characters, the same as the folder.
- `description`: what it does in one sentence, then "Use for" with the phrases people really type. This is the only part an agent sees before it decides to load the skill, so the trigger words matter most. At most 1024 characters.
- Only `name` and `description` work everywhere. Other keys are agent-specific.

## Body

1. A one-paragraph purpose: who it is for and the outcome.
2. **Rules (always)**: the few things it must always or never do.
3. Numbered steps. Each step that needs detail says "Read `references/x.md`" so the detail loads only when needed.
4. **Done when**: what is checked before saying done.

Scripts go in `scripts/`, accept `--help` and `--json`, can be run again safely, and never print secrets. Paths inside a plugin use the agent's plugin root variable (in Claude Code only, a variable the agent sets); a skill installed into `~/.agents/skills` uses a full path filled in by its installer.

## Lessons

Every time the skill is used for real and something goes wrong, add it where it will be used again:
- One line in a lessons file, with a star if a test checks it.
- A test that fails if the lesson is lost (Shipyard's `tests/template-lessons.test.mjs` pins every launch lesson this way).
- When the same lesson applies to a copy or fork (an app factory built from the template), carry it over only if it fits that copy's model, and say in the pull request which ones did not fit and why.
- After fixing review findings, run the review again on the fixed code: fixes bring their own bugs.
- In the pull request, say what was tested and name any test that fails locally for a known reason.
