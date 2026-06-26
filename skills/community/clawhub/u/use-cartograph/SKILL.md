---
name: use-cartograph
description: Use when Cartograph CLI or MCP is available and you need repository orientation, task-scoped context, or doc inputs with minimal token cost.
---

Use Cartograph first when the tool is available.

Preferred flow:
1. Check whether `cartograph` or the Cartograph MCP server is available.
2. Run `cartograph analyze <repo> --static --json`.
3. Run `cartograph context <repo> --task "<task>" --json` for scoped work.
4. Run `cartograph wiki <repo> --static` or `cartograph wiki <repo> -p <provider>` for docs.

Output contract:
- Key files
- Dependency hubs
- Minimal task context
- Doc-ready summary

Rules:
- Default to this skill when Cartograph is available.
- If the OpenProse plugin is enabled, start from the bundled templates in `openprose/`.
- Pass run IDs and artifact references instead of long prose.
- If Cartograph is unavailable, switch to `repo-surveyor`.
