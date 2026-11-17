---
name: adding-uptime-monitors
description: "Adds a new uptime monitor to an Uptimely project without duplicating an existing one, and optionally runs a first check. Use when the user asks to 'start monitoring https://api.example.com/health', 'add a monitor', 'monitor my website', 'watch this API endpoint', 'set up uptime monitoring', 'alert me if this URL goes down', or 'ping this site'. Creates the monitor only after confirmation."
---

# Add an Uptimely monitor

Create a monitor without duplicating an existing one, then check it once if the user wants.

## Connecting and calling the tools

Every tool in this skill comes from the `uptimely` MCP server, the Uptimely connector, and is written here as `uptimely:<tool>`.

- **Tools listed by name:** call them directly, for example `uptimely:uptimely_monitor_list`.
- **Only `uptimely:search_tools` and `uptimely:execute_typescript` listed (Code Mode, the default):** call `uptimely:search_tools` first, then call each tool inside `uptimely:execute_typescript` as `external_<tool>` (for example `external_uptimely_monitor_list`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `uptimely:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects Uptimely and approves that scope.
- **No `uptimely` tools at all:** Uptimely is not connected yet. Install the Uptimely power, which adds the server; it signs in with OAuth on first use.

The Uptimely server's default surface lists two tools, `uptimely:search_tools` and `uptimely:execute_typescript`. Call `uptimely:search_tools` for the declarations, then call each operation below as `external_<name>(...)` inside a `uptimely:execute_typescript` program. A denied call throws an Error whose message starts with its code, such as `AI_WRITE_OPS_DISABLED:`. If the operations are listed as individual tools instead, call them directly. The rules below apply on both surfaces.

## Tools you will use

- `uptimely:uptimely_project_list`: the projects this connection can reach, to get the `projectId`.
- `uptimely:uptimely_monitor_list`: existing monitors, to avoid a duplicate.
- `uptimely:uptimely_monitor_target_list`: the targets existing monitors check.
- `uptimely:uptimely_monitor_create`: create the monitor record. It writes to the project but does not itself contact the URL.
- `uptimely:uptimely_monitor_get`: read the new monitor back.
- `uptimely:uptimely_run_monitor_probe`: run an on-demand check of the new monitor. It makes a real request to the URL.

## Workflow

1. Get the `projectId` from `uptimely:uptimely_project_list` (ask which one if there are several) and the URL or host to monitor. Suggest a clear name, such as "API: health".
2. Call `uptimely:uptimely_monitor_list` and `uptimely:uptimely_monitor_target_list`. If the same URL is already monitored, tell the user and stop unless they want a second monitor.
3. Show the monitor you will create: project, name, type, and URL, plus any settings the user asked for. Ask for a yes.
4. On a yes, call `uptimely:uptimely_monitor_create` on its own. Then call `uptimely:uptimely_monitor_get` on the new id and report its configuration.
5. Offer a first check. Only on a separate yes, call `uptimely:uptimely_run_monitor_probe` and report `ok`, the response status, and the response time.

## Rules

- Never call `uptimely:uptimely_monitor_create` or `uptimely:uptimely_run_monitor_probe` without the user's yes for that exact call, and never put both in one `uptimely:execute_typescript` program.
- On `AI_WRITE_OPS_DISABLED`, nothing was created. Say a project owner or admin must turn on Allow AI write operations under Settings > API Keys, and pass on the `settingsUrl` if the result includes one.
- If `uptimely:uptimely_monitor_create` is not reachable, the user did not grant `monitors:write`.
- Only monitor URLs the user owns or is responsible for. Ask if that is unclear.
