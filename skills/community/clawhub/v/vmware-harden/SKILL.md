---
name: vmware-harden
description: >
  Use this skill whenever the user needs to perform VMware compliance auditing,
  baseline checking, or drift detection on vSphere/ESXi/NSX environments.
  Directly handles: CIS / vSphere SCG / 等保 2.0 三级 / PCI-DSS / BSI IT-Grundschutz / EU NIS2 scans;
  custom YAML baselines; LLM-driven remediation suggestions; web dashboard.
  Always use this skill for "scan compliance", "check baseline", "audit etcd",
  "check 等保", "drift detection", "compliance report" when the context is
  explicitly VMware/vSphere/ESXi.
  Do NOT use for general vSphere monitoring (use vmware-monitor or vmware-aiops),
  network changes (use vmware-nsx), or executing remediations directly
  (this skill only suggests; execution goes through vmware-pilot).
installer:
  kind: uv
  package: vmware-harden
allowed-tools:
  - Bash
  - Read
  - Write
metadata: {"openclaw":{"requires":{"env":["VMWARE_HARDEN_DB"],"bins":["vmware-harden"],"config":["~/.vmware-harden/twin.duckdb"]},"primaryEnv":"VMWARE_HARDEN_DB"}}
---

# VMware Harden (Compliance & Baseline)

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and "vSphere" are trademarks of Broadcom. Source code is publicly auditable at [github.com/zw008/VMware-Harden](https://github.com/zw008/VMware-Harden) under the MIT license.

AI-native VMware compliance scanner — built-in CIS / vSphere SCG / 等保 2.0 三级 / PCI-DSS / BSI IT-Grundschutz / EU NIS2 baselines, drift detection, LLM-driven remediation advice, and a web dashboard.

> **Companion skills**: [vmware-aiops](https://github.com/zw008/VMware-AIops) (inventory + collectors data source; host/VM remediation target), [vmware-monitor](https://github.com/zw008/VMware-Monitor) (read-only inspection), [vmware-storage](https://github.com/zw008/VMware-Storage) (datastore remediation target), [vmware-nsx](https://github.com/zw008/VMware-NSX) (segment/gateway evidence), [vmware-nsx-security](https://github.com/zw008/VMware-NSX-Security) (DFW evidence + remediation target), [vmware-aria](https://github.com/zw008/VMware-Aria) (metrics correlation), [vmware-avi](https://github.com/zw008/VMware-AVI) (load balancer evidence), [vmware-vks](https://github.com/zw008/VMware-VKS) (Tanzu Kubernetes evidence), [vmware-pilot](https://github.com/zw008/VMware-Pilot) (remediation execution with approval gates), [vmware-policy](https://github.com/zw008/VMware-Policy) (audit log). See [references/cross-skill-workflows.md](./references/cross-skill-workflows.md) for end-to-end remediation flows that span pilot + sibling skills.

## What This Skill Does

| Category | Tools | Count | Read or Write |
|----------|-------|-------|---------------|
| Baseline Management | 6 built-in baselines (CIS ESXi 8.0, vSphere SCG v8, 等保 2.0 L3, PCI-DSS 4.0, BSI ITGS, EU NIS2) + custom YAML loader | 6+N | Read |
| Scanning | Multi-collector (vCenter, ESXi, NSX, vSAN, K8s) → typed Twin store | 1 pipeline | Read (no target writes) |
| Drift Detection | Snapshot-to-snapshot configuration diff (per-node added/removed/changed fields) | 1 type | Read |
| Remediation Advisor | LLM-driven (Anthropic) suggestions per violation; mock fallback when no key | 1 advisor | Read |
| Web Dashboard | FastAPI + Jinja2 read-only UI for violations / drift / advice | 1 server | Read |
| MCP Server | Compliance query tools | 6 | All Read |

## Quick Install

```bash
uv tool install vmware-harden
vmware-harden baseline list
```

For first-time use, ensure a vmware-aiops target is configured (harden uses aiops collectors) and optionally set `ANTHROPIC_API_KEY` for live remediation advice.

## When to Use This Skill

Use vmware-harden when the user needs to:

- Run a **compliance scan** against CIS / vSphere SCG / 等保 2.0 三级 / PCI-DSS / BSI IT-Grundschutz / EU NIS2
- **Author or import a custom YAML baseline** (e.g., internal corporate baseline)
- Detect **drift** between two scans of the same target
- Get **AI-suggested remediation steps** for a violation (advice only — does not execute)
- Browse a **web dashboard** of compliance posture across multiple targets

**Do NOT use this skill when**:

- The task is general vCenter/ESXi monitoring or read-only inspection → use **vmware-monitor**
- The task is VM lifecycle, snapshots, or guest operations → use **vmware-aiops**
- The user wants to actually **execute** a remediation (set advanced setting, change DFW rule, etc.) → use **vmware-pilot** (multi-step approval-gated workflow)
- The task is purely NSX networking/segments → use **vmware-nsx**

## Related Skills — Skill Routing

| User Intent | Recommended Skill |
|-------------|-------------------|
| "Scan ESXi for CIS compliance" | **vmware-harden** ← this skill |
| "Check 等保 2.0 三级" | **vmware-harden** |
| "What changed since last week?" (drift) | **vmware-harden** |
| "Fix this violation now" | **vmware-pilot** (approval-gated execution) |
| "List VMs / hosts / alarms" | **vmware-monitor** |
| "Reconfigure / power / migrate VM" | **vmware-aiops** |
| "Edit DFW rule" | **vmware-nsx-security** |
| "Browse audit log" | **vmware-policy** (`vmware-audit log`) |

## Common Workflows

### 1. First-time scan with 等保 2.0 三级

1. Install: `uv tool install vmware-harden`
2. Verify aiops is configured: `vmware-aiops doctor` — harden reuses aiops connection for the vCenter collector
3. List baselines: `vmware-harden baseline list` — confirm `dengbao-2.0-level3-vmware` is present
4. Scan: `vmware-harden scan --baseline dengbao-2.0-level3-vmware --target prod-vcenter`
5. Report: `vmware-harden report --format json > violations.json` (or `vmware-harden web` for the rendered dashboard)

   **Failure branch**: If you see `ConnectError: vmware-aiops target not found`, the aiops side is not configured. Run `vmware-aiops init` first; harden cannot scan without a working collector.

### 2. Custom baseline import + scan

1. Author YAML under `~/.vmware-harden/baselines/my-corp.yaml` (see references for schema)
2. Validate: `vmware-harden baseline validate ~/.vmware-harden/baselines/my-corp.yaml`
3. Import: `vmware-harden baseline import ~/.vmware-harden/baselines/my-corp.yaml`
4. Scan: `vmware-harden scan --baseline my-corp --target prod-vcenter`

   **Failure branch**: `baseline validate` failure usually means a `check.path` references a node type the collectors do not produce (e.g. `nsx.gateway.*` when no NSX collector ran). See [references/cli-reference.md](./references/cli-reference.md) for valid node paths and the baseline schema.

### 3. Drift investigation

1. Run scan today: `vmware-harden scan --target prod-vcenter --baseline cis-vmware-esxi-8.0-subset`
2. Run scan again next week (or after a change window): same command
3. View drift: `vmware-harden drift` (renders the latest snapshot vs its prior snapshot for the same target)
4. Get advice on critical drift: `vmware-harden advise --violation-id <id>` or `vmware-harden advise --all-critical` (uses `ANTHROPIC_API_KEY`; falls back to mock template if unset)
5. Open web view: `vmware-harden web --port 8080` then navigate to `/drift`

   **Failure branch**: If `vmware-harden drift` reports `No drift detected since previous snapshot`, both scans likely ran against the same state. Ensure two scans actually completed against the same `--target`; the Twin DB at `~/.vmware-harden/twin.duckdb` must contain at least two snapshots for that target.

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local CLI scans by an operator | **CLI** | Direct, scripts well into CI |
| AI agent integration | **MCP** | 6 read-only tools, structured responses |
| Reviewing posture interactively | **Web** | `vmware-harden web` — sortable tables, drift timeline |
| CI/CD pipeline gates | **CLI** | Exit code reflects compliance pass/fail |

## MCP Tools (6 — 6 read, 0 write)

| Category | Tool | Description |
|----------|------|-------------|
| Baseline | `list_baselines` | All built-in + imported baselines (id, framework, version) |
| Baseline | `get_baseline_rules` | Rules for a given baseline_id (severity, references) |
| Violation | `list_violations` | Current violations, filterable by severity |
| Violation | `get_remediation` | Remediation suggestion for a violation_id (LLM or mock) |
| Drift | `list_drift_events` | Recent drift events from snapshot diff |
| Scan | `scan_target` | Trigger a scan against a target (read-only on the target) |

All 6 tools are **read-only** with respect to vSphere/NSX. Writes to the local Twin DuckDB are scan-internal and do not modify any VMware resource. Actual remediation execution is intentionally **deferred to vmware-pilot** (approval-gated).

## CLI Quick Reference

```bash
vmware-harden baseline list
vmware-harden baseline import <path>
vmware-harden baseline validate <path>
vmware-harden scan --baseline <id> --target <name>
vmware-harden report [--format text|json]
vmware-harden drift [--format text|json]
vmware-harden advise (--violation-id <id> | --all-critical)
vmware-harden web [--host 127.0.0.1] [--port 8080]
```

> Full CLI reference: see [references/cli-reference.md](./references/cli-reference.md)
> Full capabilities table with response token estimates: see [references/capabilities.md](./references/capabilities.md)

## Troubleshooting

### "vmware-aiops target not found" / collectors return empty
Harden does not connect to vCenter directly — it relies on vmware-aiops collectors. Run `vmware-aiops doctor` and confirm the `--target` name matches an aiops target.

### `ANTHROPIC_API_KEY` not set — advice looks generic
The advisor falls back to a deterministic mock template when no API key is present. Set `export ANTHROPIC_API_KEY=...` in your shell or in `~/.vmware-harden/.env` for live LLM-driven suggestions.

### `uvx` reports "UnknownIssuer" behind a corporate TLS proxy
Don't use `uvx` for the MCP server in this environment. Use the entry point installed by `uv tool install`:

```json
{
  "command": "vmware-harden-mcp",
  "args": []
}
```

This avoids `uvx` re-resolving PyPI through the corporate MitM proxy. As a workaround, `UV_NATIVE_TLS=true` lets uv use the system CA store. See CLAUDE.md 踩坑 #25.

### "Twin DB not found" on first MCP call
Run at least one scan first: `vmware-harden scan --baseline cis-vmware-esxi-8.0-subset --target <t>`. The DuckDB file is created on first scan at `~/.vmware-harden/twin.duckdb` (override with `VMWARE_HARDEN_DB`).

### 等保 baseline rules are not firing (all checks "skipped")
The 等保 baseline references node types from multiple collectors (vCenter advanced settings + ESXi NTP + NSX DFW). If only the vCenter collector ran, rules referencing `nsx.*` paths skip with status "no evidence". Run a scan with all collectors enabled, or filter the baseline to only the relevant rules.

### Web dashboard shows 0 violations even after a scan
Verify the dashboard is reading the same DuckDB. If `VMWARE_HARDEN_DB` is set in your shell but not in the systemd/launchd unit running `vmware-harden web`, the web server reads the default `~/.vmware-harden/twin.duckdb` while your scans wrote elsewhere.

## Audit & Safety

1. **Source code**: [github.com/zw008/VMware-Harden](https://github.com/zw008/VMware-Harden) — MIT license, publicly auditable.
2. **Config / state files**: custom baselines in `~/.vmware-harden/baselines/*.yaml`; Twin DuckDB at `~/.vmware-harden/twin.duckdb`. No passwords are stored — all credentials live in the upstream skill (`~/.vmware-aiops/.env`).
3. **Webhook data scope**: none. Harden makes **no outbound network calls** other than (a) optional Anthropic API requests when `ANTHROPIC_API_KEY` is set for advisor suggestions, and (b) the local web dashboard bound to `127.0.0.1` by default.
4. **TLS verification**: harden does not connect to vCenter/NSX directly — TLS handling is delegated to vmware-aiops. The advisor's HTTPS calls to `api.anthropic.com` use system TLS verification (no opt-out).
5. **Prompt injection protection**: advisor LLM context is built exclusively from typed Twin queries (rule id, severity, evidence dict) — no free-text user input is forwarded. Evidence text passes through `_sanitize()` (truncate ≤500 chars, strip C0/C1 control characters).
6. **Least privilege**: all 6 MCP tools are read-only. Remediation execution is intentionally not exposed — agents that need to apply a fix must invoke **vmware-pilot**, which provides approval gates and audit logging.

All MCP operations are audited via the `@vmware_tool` decorator (vmware-policy dependency) to `~/.vmware/audit.db`. View with `vmware-audit log --last 20`.

> Full setup / security / AI platform compatibility: see [references/setup-guide.md](./references/setup-guide.md)

## License

MIT — [github.com/zw008/VMware-Harden](https://github.com/zw008/VMware-Harden)
