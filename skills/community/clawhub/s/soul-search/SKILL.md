---
name: soul
description: Browse categories, preview, apply, and restore OpenClaw SOUL.md personas from a curated remote catalog. Use for /soul categories, /soul list <category>, /soul show <id>, /soul apply <id>, /soul current, /soul restore, /soul refresh, and /soul search <text>.
user-invocable: true
metadata:
  { "openclaw": { "requires": { "bins": ["node"] } } }
---

# soul

Handle `/soul` requests by running the helper script in this skill directory.

## Command forms

- `categories`
- `list <category>`
- `show <id>`
- `apply <id>`
- `current`
- `restore`
- `refresh`
- `search <text>`

## Execution

When invoked, run:

```bash
node {baseDir}/scripts/soul.mjs "$ARGUMENTS"
```

Where `$ARGUMENTS` is the raw argument string following `/soul`.

Then:

- return the helper script output directly to the user
- do not embellish or reinterpret the result unless the output is clearly broken

## Safety rules

- Only trust the configured catalog URL and raw GitHub content derived from its entries.
- Never overwrite `SOUL.md` without first creating a backup in `soul-data/backups/`.
- Write provenance metadata to `soul-data/state.json`.
- After apply/restore, remind the user to start a new session or use `/new` for full effect.
