---
name: repo-surveyor
description: Use when Cartograph CLI or MCP is unavailable and you still need Cartograph-style repo orientation, task context, or documentation inputs from manual file survey.
---

Use this skill only when Cartograph itself is unavailable or when you need to manually verify its outputs.

Manual workflow:
1. Discover source, config, and entry files. Skip generated, vendored, and build output.
2. Rank likely-important files by entry points, fan-in, API surface, and root wiring role.
3. Trace the strongest dependency hubs instead of reading the whole tree.
4. Build the smallest useful file set for the current task.
5. Produce a doc-ready summary from that reduced set.

Output contract:
- Key files
- Dependency hubs
- Minimal task context
- Doc-ready summary

Rules:
- If the OpenProse plugin is enabled, start from the bundled templates in `openprose/`.
- Prefer `use-cartograph` whenever the tool becomes available.
- Keep manual reads narrow.
- Match the same output shape as `use-cartograph`.
