---
name: checking-uptime-status
description: "Reports the current health and recent history of an Uptimely project: monitor status, open incidents and alerts, uptime over a period, who is on call, maintenance windows, status pages, and telemetry services. Use when the user asks 'is anything down', 'is my site up', 'what incidents are open', 'how did the checkout monitor do this week', 'who is on call', 'is maintenance scheduled', 'show uptime', or wants a status check or monitoring overview. Read-only."
---

# Uptimely status check

Answer "is anything wrong, and who is handling it" for one Uptimely project from live data.

## Connecting and calling the tools

Every tool in this skill comes from the `uptimely` MCP server, the Uptimely connector, and is written here as `uptimely:<tool>`.

- **Tools listed by name:** call them directly, for example `uptimely:uptimely_monitor_list`.
- **Only `uptimely:search_tools` and `uptimely:execute_typescript` listed (Code Mode, the default):** call `uptimely:search_tools` first, then call each tool inside `uptimely:execute_typescript` as `external_<tool>` (for example `external_uptimely_monitor_list`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `uptimely:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects Uptimely and approves that scope.
- **No `uptimely` tools at all:** Uptimely is not connected yet. Install the Uptimely power, which adds the server; it signs in with OAuth on first use.

The Uptimely server's default surface lists two tools, `uptimely:search_tools` and `uptimely:execute_typescript`. Call `uptimely:search_tools` for the declarations, then call each operation below as `external_<name>(...)` inside a `uptimely:execute_typescript` program. Batch independent reads with `Promise.all`, for example the overview, monitor list, and open incidents in one program. A denied call throws an Error whose message starts with its code, such as `PROJECT_ACCESS_DENIED:`. If the operations are listed as individual tools instead, call them directly.

## Tools you will use

- `uptimely:uptimely_project_list`: the projects this connection can reach, with their ids. Takes no input.
- `uptimely:uptimely_project_overview`: monitor, incident, alert, and status page counts plus the project's overall health.
- `uptimely:uptimely_monitor_list`: every monitor with its current status.
- `uptimely:uptimely_monitor_get`: one monitor's configuration.
- `uptimely:uptimely_monitor_status_history`: a monitor's recorded status transitions with durations over a window.
- `uptimely:uptimely_monitor_target_list`: the targets a monitor checks.
- `uptimely:uptimely_incident_list`: incidents, optionally only active ones (`activeOnly`).
- `uptimely:uptimely_incident_get`: one incident with state, severity, root cause, notes, and state timeline.
- `uptimely:uptimely_alert_list`: alerts and their states.
- `uptimely:uptimely_on_call_current`: who is on call now and who is next, per schedule.
- `uptimely:uptimely_maintenance_list`: scheduled and past maintenance windows.
- `uptimely:uptimely_status_page_list`: the project's status pages.
- `uptimely:uptimely_telemetry_service_list`: the project's telemetry services.

## Workflow

1. Get the `projectId`. Every operation except `uptimely:uptimely_project_list` needs it. Call `uptimely:uptimely_project_list`; if it returns one project, use it, and if several, ask the user which one. Reuse the id for every later call.
2. Call `uptimely:uptimely_project_overview`. Lead with the overall health in one line.
3. If anything is not healthy, call `uptimely:uptimely_monitor_list` and name the monitors that are down or degraded, then `uptimely:uptimely_incident_list` with `activeOnly: true` and `uptimely:uptimely_alert_list`, and name the open incidents and active alerts with their state and severity.
4. Call `uptimely:uptimely_on_call_current` and say who is on call now and who is next.
5. Call `uptimely:uptimely_maintenance_list` and mention any window that is in progress or coming up soon, since it can explain a down monitor.
6. For a history question ("how did X do this week"), find the monitor in `uptimely:uptimely_monitor_list`, then call `uptimely:uptimely_monitor_status_history` for the window. Report total downtime, the number of outages, and the longest one.
7. Offer next steps that match what you found: the `responding-to-incidents` skill for an unhandled outage, or the `writing-postmortems` skill for a resolved one.

## Rules

- Never call a write operation from this skill: `uptimely:uptimely_monitor_create`, `uptimely:uptimely_run_monitor_probe`, `uptimely:uptimely_incident_declare`, `uptimely:uptimely_incident_state_change`, `uptimely:uptimely_incident_postmortem_save`, `uptimely:uptimely_alert_create`, or `uptimely:uptimely_alert_state_change`.
- `PROJECT_ACCESS_DENIED` means the id is wrong or the account is not a member. Use `uptimely:uptimely_project_list` to pick a valid id; never guess one.
- Report times in the user's timezone and say which one you used.
- Report only what the tools return. Do not estimate uptime percentages the data does not contain.
