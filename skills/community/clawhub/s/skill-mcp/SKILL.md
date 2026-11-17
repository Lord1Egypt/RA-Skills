---
name: skill-mcp-demo
description: The example skill shipped with skill-mcp — shows the SKILL.md shape, a bundled reference file, and a declared runnable script.
when-to-use: When checking that skill-mcp is wired up, or when writing a skill's own mcp-host declaration block.
mcp-host:
  version: 1
  run:
    - script: scripts/report.js
      interpreter: node
      timeout: 15
---

# skill-mcp demo

This skill exists so `skill-mcp` does something useful the first time it runs,
and so the shape of a skill it can serve is visible in one file.

## What a skill is

A directory holding `SKILL.md` — YAML frontmatter (`name`, `description`, and
optionally the `mcp-host:` block below) followed by instructions — plus any
files the instructions refer to. Read `references/declaration.md` with
`skill_file` for the declaration block's fields.

## Declaring a runnable script

Only a script named in `mcp-host.run` may be executed, and only through
`skill_run`. This skill declares one:

- `scripts/report.js` — prints what the fence handed it: its argv, its working
  directory, and the NAMES of the environment variables it received.

Run it to see the fence from the inside:

```
skill_run(name: "skill-mcp-demo", script: "scripts/report.js", args: ["hello"])
```

`skill_run` asks the user to confirm first. Where the client cannot show a
confirmation prompt (or the server sets `MCP_CONFIRM_ELICITATION=off`, which
sends every client down this path), that first call starts nothing and returns
a preview of exactly what would run plus a `confirmToken`; once the user
approves, call again with the same arguments and `confirmToken: "<token>"`.

## What the fence does and does not do

It decides **which** code runs and **what it is handed**. It does not make the
code safe — a declared script is still arbitrary code, bounded by whatever the
host running this server bounds it with.
