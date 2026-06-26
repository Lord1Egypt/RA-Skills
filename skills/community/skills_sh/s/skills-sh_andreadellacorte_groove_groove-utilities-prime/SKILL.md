---
name: groove-utilities-prime
description: "Load groove workflow context into the conversation. Run at the start of every session."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) Bash(mkdir:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# groove-utilities-prime

Run the prime shell script and output its result to the conversation:

```bash
bash .agents/skills/groove-utilities-prime/scripts/groove-utilities-prime.sh
```

Do not write to any file (the script handles its own cache updates). Output the script's stdout verbatim.
