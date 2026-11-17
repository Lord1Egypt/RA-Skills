---
name: scope
description: Drift guard that fires during execution when the agent is about to touch a file or run a command outside the boundaries agreed in recon. Compares the pending action against recon's proposed self-rules and the original task description. On drift, stops, shows the specific action that exceeds scope, and offers three options (proceed with justification, defer to follow-up, revert). Prevents silent scope creep where a small task quietly becomes a large one.
license: MIT
---

# Scope

The original task is a contract. When the agent starts doing work outside that contract, it has drifted. This skill catches the drift.

## When this runs

This skill fires when the agent is about to:
- Write or modify a file that was not listed in recon's "What I found" section
- Run a shell command that touches resources outside the project directory
- Add a dependency that was not part of the original plan
- Refactor code that was not part of the task description
- Perform any action whose justification is "while I'm here" or "this should also..."

This skill does NOT fire for:
- Files that are clearly required by the task but weren't listed in recon (missing inspection)
- Test files for code the agent just wrote (part of the task)
- Trivial formatting changes to files already in scope

## Procedure

### 1. Pause before acting

Do not execute the out-of-scope action. The pause is the value.

### 2. Produce the drift report

Output exactly this template wrapped in a markdown code block. Make absolutely sure the closing fence is on its own line:

```markdown
## Scope Drift Detected

### Original task
[one sentence from recon's task summary]

### Action about to be taken
- File or resource: [path or command]
- Why: [one sentence justification]

### Why this is out of scope
- recon listed: [the files/resources that were in scope]
- This action touches: [what it touches]
- Mismatch: [the specific boundary being crossed]

### Options

1. Proceed with justification
   - Justification: [why this is required after all]
   - Risk: [what could go wrong]

2. Defer to follow-up
   - Add to follow-up list: [yes/no]
   - Task to create: [one-line description]

3. Revert
   - Undo the change: [what needs reverting]
   - Return to: [the last in-scope state]

### Awaiting decision
Reply "1", "2", or "3".
```

### 3. Wait

Do not take any action until the user chooses.

### 4. On user choice

- Option 1: proceed, but append the justification to the session log
- Option 2: add the item to the follow-up list, return to in-scope work
- Option 3: revert the change and resume from the last in-scope state

## Rules for this skill

- Only fire on real drift, not on incomplete recon. If the agent forgot to list a required file, that is a recon mistake, not drift.
- Always show the specific boundary that is being crossed. "This is out of scope" is not enough.
- Never block silently. Every drift detection must produce a report.
- Deferring is the default option. Proceeding with justification requires a real reason.

## Common mistakes

- Firing on every file write. This skill is for drift, not for normal task execution.
- Triggering because the agent forgot to list a file in recon. That is not drift; that is an inspection gap. Fix recon, do not fire scope.
- Blocking silently. If the skill fires, the user must see the report.
- Treating "defer to follow-up" as a failure. It is often the correct choice.
- Letting "while I'm here" justifications proceed without the user's confirmation.
