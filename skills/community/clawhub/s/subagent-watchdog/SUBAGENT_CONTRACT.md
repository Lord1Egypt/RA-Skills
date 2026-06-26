# Subagent contract (mandatory)

When a subagent is spawned for a task with label `<label>`, it must:

1) Save full results to the project files (as instructed).
2) Create a completion marker file:

- `subagent-watchdog/state/<label>.done`

The marker file must include:
- UTC timestamp
- what files were written/updated

3) Keep chat output minimal:
- one line: `Wrote: <paths>`
- up to 5 bullets listing option names only (no raw report content)
