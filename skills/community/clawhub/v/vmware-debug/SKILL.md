---
name: vmware-debug
description: >
  Use this skill whenever the user is troubleshooting a VMware/vSphere problem —
  a reported error, an exception, a log dump, a slow or failed VM, a host that
  went sideways — and needs help locating the root cause. It is the diagnostic
  brain of the VMware family: it drives a systematic investigation, pulls the
  right signals from the other skills, correlates events into one timeline,
  ranks root-cause hypotheses, and tells you what to check next even when you
  don't know where to start. Always use this skill for "diagnose this VMware
  issue", "why is my VM slow", "troubleshoot this vSphere error", "what does
  this log mean", "help me figure out what broke" when the context is explicitly
  VMware/vSphere/ESXi/NSX. It is READ-ONLY: it never changes anything. Do NOT
  use it to execute fixes — single fixes go to vmware-aiops, multi-step gated
  remediation goes to vmware-pilot. Do NOT use it for routine inventory or
  health checks with no problem to solve — use vmware-monitor.
installer:
  kind: uv
  package: vmware-debug
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"bins":["vmware-debug"]},"primaryEnv":"NONE"}}
---

# VMware Debug

> **Disclaimer**: Community-maintained open-source project, **not affiliated with,
> endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and "vSphere"
> are trademarks of Broadcom. Source is publicly auditable under the MIT license.

The diagnostic brain of the VMware skill family. You bring the symptom; this skill
runs the investigation and points at the root cause. It **reads and reasons** — it
never writes. Companion skills do the data collection and the fixing.

## What This Skill Does

| Category | What | Read or Write |
|---|---|---|
| Incident correlation | Merge events from many sources into one timeline, detect spikes | Read |
| Root-cause ranking | Score symptom clusters, surface the most likely cause first | Read |
| Next-check ideas | Suggest exactly what to look at next (which skill/tool) when you're stuck | Read |
| Remediation routing | Hand the fix to vmware-aiops (single) or vmware-pilot (gated, multi-step) | Read (routes only) |

**Zero write tools. Zero network access of its own.** It correlates data the agent
has already gathered with the other skills' read tools.

## Quick Install

```bash
uv tool install vmware-debug
vmware-debug categories          # see what it can diagnose
```

## When to Use This Skill

Use it when there is a **problem to solve**: an error message, a stack of logs, an
alarm storm, "my VM won't power on", "storage feels slow", "the host disconnected".

- Need raw inventory/health with no incident? → **vmware-monitor**
- Need to actually run a fix? → **vmware-aiops** (single op) or **vmware-pilot** (gated workflow)
- Need metrics/anomalies? → **vmware-aria**; centralized logs? → **vmware-log-insight**

**Do NOT use when** there is nothing wrong (routine listing → monitor), or when the
user wants the fix executed (→ aiops/pilot). This skill stops at the diagnosis and
a recommended plan.

## Related Skills — Skill Routing

| Symptom touches | Pull signals from | Then |
|---|---|---|
| Storage / datastore / vSAN | vmware-storage, vmware-log-insight | rank → route fix to aiops/pilot |
| Network / firewall / vMotion | vmware-nsx, vmware-nsx-security | run traceflow, check DFW |
| CPU / memory contention | vmware-aria (metrics/anomalies) | rightsizing via pilot |
| HA / DRS / cluster | vmware-monitor, vmware-aiops | cluster remediation via pilot |
| Power / clone / snapshot | vmware-aiops, vmware-monitor | task status, then fix via aiops |
| Auth / cert / login | check creds & cert; (security) | fix config/.env |

## Common Workflows

### 1. "Here's a pile of logs / alarms — what broke?"
1. Collect events with the data-source skills (e.g. `vmware-monitor event_list --vm web01 --since 1h`, `vmware-log-insight log_search ...`, `vmware-aria alert_query ...`).
2. Pass them all to **`incident_timeline`** (envelope below). Read the top hypothesis + `next_checks`.
3. Follow `next_checks` to pull more targeted data; re-run `incident_timeline` to confirm.
4. **Failure branch — no events come back:** the affected target may be unreachable. Run the source skill's `doctor`/health first; a 503/timeout is a *signal* (platform not ready), not a dead end.
5. Produce a diagnosis + recommended fix. Route execution to aiops/pilot. **Do not fix here.**

### 2. "I don't even know what to check"
1. Run **`list_symptom_categories`** (or `vmware-debug categories`) to see the catalogue.
2. Describe the symptom; map it to a category; the `suggested_check` tells you which skill/tool to run first.
3. Collect → `incident_timeline` → narrow. Loop until one hypothesis dominates.

### 3. Hand off the fix (advisor → executor, like vmware-harden)
1. Debug emits a structured diagnosis + a proposed remediation (steps).
2. **Single, low-risk fix** → call the matching **vmware-aiops** tool (it has its own double-confirm).
3. **Multi-step / needs approval / cross-skill** → submit the plan to **vmware-pilot**, which owns the state machine, approval gate, rollback, and audit.
4. **Failure branch — fix is ambiguous or risky:** stop and present the hypotheses to the user; never guess-execute.

## Usage Mode

- **MCP** (in an agent): the agent calls the other skills' read tools, then `incident_timeline` to correlate. This is the primary mode — that's where the cross-skill "联动" happens.
- **CLI** (humans): `vmware-debug triage --events events.json` correlates a JSON array you collected yourself.

## MCP Tools (2 — 2 read, 0 write)

| Tool | What |
|---|---|
| `incident_timeline` | [READ] Correlate pre-fetched events → timeline + spikes + ranked hypotheses + next-check ideas |
| `list_symptom_categories` | [READ] List recognised symptom categories + what to check for each |

**Event envelope** (input to `incident_timeline`): `{ts, source, severity, entity, text, fields}`.
See `references/event-envelope.md`. The agent normalises each source's events into this
shape; debug stays source-agnostic and has no dependency on the other packages.

## CLI Quick Reference

```bash
vmware-debug categories                        # what can it diagnose
vmware-debug triage --events events.json       # correlate a collected event set
cat events.json | vmware-debug triage          # or via stdin
vmware-debug mcp                                # start stdio MCP server (proxy-safe)
```

## Troubleshooting

- **`incident_timeline` raises "event[N] could not be normalised"** — event N is missing a timestamp or has an unparseable one. Every event needs `ts` (ISO-8601, epoch seconds, or millis).
- **All hypotheses come back "uncategorized"** — the symptom isn't in the catalogue yet; widen the window and pull from another source (aria anomalies, log-insight). Consider adding a signature (see `references/routing.md`).
- **No spikes detected on an obvious burst** — you need ≥3 time bins for a baseline; shrink `bin_seconds`.
- **It won't execute the fix** — by design. Route to vmware-aiops or vmware-pilot.

## Audit & Safety

Read-only by construction: no write tools, no network, nothing executed. Remediation
is always routed to aiops/pilot, where the double-confirm / approval / audit gates live
(audit DB `~/.vmware/audit.db`). See `references/setup-guide.md`.

## License

MIT.
