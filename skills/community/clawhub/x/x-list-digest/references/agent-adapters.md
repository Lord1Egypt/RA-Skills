# Host adapters

| Host | User skill path | Browser | Scheduler |
|---|---|---|---|
| Codex | ~/.agents/skills/x-list-digest | Actual supplied browser tools and their documentation | Available automation tools |
| Hermes | ~/.hermes/skills/x-list-digest | Native browser_exec with an explicitly authorized connection | Native cron tools |
| Claude Code | ~/.claude/skills/x-list-digest | Configured browser MCP/bridge | Actual host scheduler |
| OpenClaw | ~/.openclaw/skills/x-list-digest | Native browser using an authorized logged-in profile | Native cron tools |

Discovery paths are not proof of successful runtime compatibility. A shared source can be linked into supported discovery paths after authorized installation. Preserve local config and user edits on upgrades.

Hermes browser_exec requires browser and terminal tools. Read its current tool documentation; its outer language is Python, with JavaScript inside native `js(...)`. Do not assume helper names or a `workspace` global outside the supported runtime. Use `host_collector.run_native` rather than generating another loop.

Codex must follow its actual browser tool contract. A tool may restrict evaluation or omit JavaScript globals. Read DOM datetime/href/text/aria-label and convert counts in the host environment; unknowns are null. A displayed tab is not proof of browser access. Do not use another connection or tool to evade restrictions.

Use an explicitly connected authorized backend. Do not force Hermes local=true when an independent native browser is already selected. A locked real profile is a backend blocker, not an empty list; do not close the user's ordinary browser or claim cloud access after switching local=false. No cookie copying or credential export.

If browser and data processing run on different machines, transfer only observed JSON/JSONL through supported tools. Feishu publication must run where the selected native CLI credentials are available. Installing a cloud CLI does not connect local credentials.
