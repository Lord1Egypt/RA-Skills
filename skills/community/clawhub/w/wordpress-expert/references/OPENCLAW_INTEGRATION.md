# OpenClaw: tool policy, sandbox, and this project

Quick reference for how OpenClaw **tools**, **skills**, **plugins**, and **sandbox** interact—aligned with skill **wordpress-expert** and plugin **wordpress-site-tools**. Always check official sources if your OpenClaw version differs.

## Official documentation (entry)

- [Tools and Plugins](https://docs.openclaw.ai/tools)—built-ins, allow/deny, profiles, groups
- [Skills](https://docs.openclaw.ai/tools/skills)
- [Skills Config](https://docs.openclaw.ai/tools/skills-config)—`skills.entries`, `env`, sandbox notes
- [Creating skills](https://docs.openclaw.ai/tools/creating-skills)
- [Plugins / Building Plugins (Agent Tools)](https://docs.openclaw.ai/plugins/building-plugins)—optional tools, `tools.allow`, plugin ID
- [Sandbox vs Tool Policy vs Elevated](https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated)—**sandbox** vs **tool allowlists** vs **elevated exec**

## Global tool policy (`tools.allow` / `tools.deny`)

- In OpenClaw: **`tools.deny` always wins** over allow.
- **`tools.profile`** (e.g. `full`, `coding`, `minimal`) may set a **base allowlist**; then global and per-agent **`allow`/`deny`** apply.
- WordPress plugin tools (`wordpress_rest_request`, … or bundle **`wordpress-site-tools`**) must be **allowed** in the **effective** policy—otherwise the agent does not see them or they are blocked, **even if** `tools.allow` is set in JSON but `deny` or a restrictive profile overrides.

Layers: [Sandbox vs Tool Policy](https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated).

## Tool groups (`group:*`)

Allow/deny lists may use shortcuts like `group:fs`, `group:runtime`, `group:openclaw`.

**Important for this project:** Per OpenClaw docs, **`group:openclaw`** covers **built-in** OpenClaw tools—**not** tools from **external plugins**. **wordpress-site-tools** tools are **not** automatically in `group:openclaw`.

Therefore: list WordPress tools **explicitly**, e.g.:

- individually: `wordpress_connection_check`, `wordpress_rest_request`, `wordpress_wp_cli`, `wordpress_media_upload`, `wordpress_plugin_files`, or
- **bundle:** `wordpress-site-tools` (all tools from this plugin) if your OpenClaw version supports it ([Agent Tools](https://docs.openclaw.ai/plugins/agent-tools)).

## Sandbox and plugin tools

When the agent runs in a **sandboxed** session (Docker etc.), OpenClaw adds an **extra** policy:

- `tools.sandbox.tools.allow` / `tools.sandbox.tools.deny` (global or under `agents.list[].tools.sandbox.tools.*`)

Plugin tools are **not** automatically allowed just because they are in **global** `tools.allow`. On messages like **“Tool … blocked by sandbox tool policy”**, add WordPress tools (or `wordpress-site-tools`) to **`tools.sandbox.tools.allow`** (paths: [Sandbox vs Tool Policy](https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated)).

**Diagnostics:**

```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
```

shows effective sandbox tool allowlists among other things.

## Environment: skill env vs. sandbox container

Per [Skills Config](https://docs.openclaw.ai/tools/skills-config):

- `skills.entries.<skillKey>.env` applies to **host** runs; variables are typically set only if not already present.
- In a **sandbox**, the container does **not** inherit host `process.env`.

For **WORDPRESS_*** and optionally **PATH** (so `wp` / `curl` / `ddev` are found) in sandboxed sessions, use e.g.:

- `agents.defaults.sandbox.docker.env`, or
- per agent: `agents.list[].sandbox.docker.env`, or
- custom sandbox image

See also [AUTH.md](AUTH.md) and [CONNECTING.md](CONNECTING.md).

## `tools.byProvider` (edge case)

OpenClaw allows **per provider/model** tool restrictions (`tools.byProvider`). If tools are missing despite global `tools.allow`, check this layer ([Tools](https://docs.openclaw.ai/tools)).

## WordPress skill / plugin (short)

| Topic | Where |
|--------|-------|
| Connection, `openclaw.json`, topologies | [CONNECTING.md](CONNECTING.md) |
| Credentials | [AUTH.md](AUTH.md) |
| DDEV / `ddev wp` | [DDEV.md](DDEV.md) |
| Register plugin tools | [openclaw-wordpress-tools/README.md](../../openclaw-wordpress-tools/README.md) |
| After plugin/allowlist change | **`openclaw gateway restart`**; chat `/new` only for stale UI tool list ([README.md](../README.md), [CONNECTING.md](CONNECTING.md)) |

Tool names for this plugin: `wordpress_connection_check`, `wordpress_rest_request`, `wordpress_wp_cli`, `wordpress_media_upload`, `wordpress_plugin_files` (or bundle ID **`wordpress-site-tools`**).

## See also

- [PLUGIN_DEV_PLAYBOOK.md](PLUGIN_DEV_PLAYBOOK.md)—plugin code under OpenClaw
- [TOOLING.md](TOOLING.md)—which tool for WordPress
- [NATIVE_VS_PLUGIN.md](NATIVE_VS_PLUGIN.md)—plugin vs. `exec` / browser / workspace
- [CONNECTING.md](CONNECTING.md)—connection, verification, troubleshooting
