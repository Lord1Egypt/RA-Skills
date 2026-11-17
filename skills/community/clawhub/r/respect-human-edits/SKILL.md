---
name: respect-human-edits
description: Detect and preserve human code edits
version: 1.0.1
---

# Safe Git Editing & Committing Workflow
Use this skill only when requested by the user to ensure human code edits are preserved and changes are tracked.

### Workflow Steps
1. **Check if gitignored:** 
   Before editing a file, use the terminal command `git check-ignore -v <filepath>` to see if a file is ignored by git.

2. **Check Human Edits:** 
   If ignored: Load the file into context before editing.
   If tracked: Check if the user modified it with the terminal command `git diff -U1 <filepath>`. Any diff is a human edit and must be preserved unless instructed otherwise.

3. **Always commit:** 
   After finishing each series of edits, finish by committing to git with a very concise message.