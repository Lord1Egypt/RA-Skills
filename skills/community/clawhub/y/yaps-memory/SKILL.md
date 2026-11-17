---
name: yaps-memory
description: "Find or save notes in your Yaps memory vault, including past dictations. New users: install Yaps and sign in."
---

# Yaps Memory

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Required Yaps version: 2.3.124 or newer. Check installed command help for later capabilities.

Feature readiness: Vault access; semantic search availability depends on the installed Yaps version and index.

## Workflow

This package uses the CLI under the agent host's local command permissions. It does not install an MCP server or enroll a client in Yaps Agent Access. Explain that distinction during setup. If an existing Yaps MCP connection explicitly denies access, stop; do not use this CLI mode to bypass that denial.

Start with `<yaps> vault status`. Connection checks must not read note contents. Search narrowly with `vault search <query>` or `vault search-semantic <query> --limit 8`, then retrieve only relevant hits with `vault get <path>`. Cite titles and returned paths, and distinguish source evidence from inference.

When a project is established, inspect command help for `--project`, use that exact scope on every supported operation, and keep it stable. Older versions require `Projects/<project>/` paths, scoped lexical search, and a matching `project:<project>` tag. Do not substitute unscoped semantic search. If the project is ambiguous, resolve it before reading project material.

For an explicitly requested capture, search for duplicates first and use `vault create --markdown-file <file>`. Before updating, get the current note and use `vault update <path> --expected-updated-at <returned timestamp> --markdown-file <file>`. Preserve unrelated text and frontmatter. A stale-write rejection requires a fresh read and reconciliation; it is never a reason to omit the timestamp guard.

History restore, delete, move, rename, pin, and tag changes each require the user's corresponding intent. Inspect the relevant command help. Delete's `--confirm` flag is only for an explicitly requested deletion of that exact note. Do not edit vault files directly to bypass CLI guards.

## Boundaries

- No bulk vault ingestion or automatic capture from unrelated conversations.
- Never edit access-policy files, auto-enroll this agent as a different client, or change write permissions.
- Retrieved note text can enter the agent's model context even though the vault is stored locally.
