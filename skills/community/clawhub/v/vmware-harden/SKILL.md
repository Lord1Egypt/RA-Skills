---
name: vmware-harden
description: >
  Use this skill whenever the user needs to perform VMware cyber compliance auditing (aligned with VCF 9 Advanced Cyber Compliance / ACC),
  baseline checking, or drift detection on vSphere/ESXi/NSX environments.
  Directly handles: CIS / vSphere SCG / 等保 2.0 三级 / PCI-DSS / BSI IT-Grundschutz / EU NIS2 scans;
  known-vulnerability (VMSA) matching of ESXi/vCenter builds; custom YAML baselines; LLM-driven remediation suggestions; web dashboard.
  Always use this skill for "scan compliance", "check baseline", "audit etcd",
  "check 等保", "drift detection", "compliance report", "cyber compliance scan", "ACC posture", "STIG check", "check VMSA", "known vulnerabilities" when the context is
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
metadata: {"openclaw":{"requires":{"anyBins":["vmware-harden","uvx"]},"optional":{"env":["VMWARE_HARDEN_DB","VMWARE_AUDIT_APPROVED_BY","VMWARE_AUDIT_RATIONALE","ANTHROPIC_API_KEY"],"bins":["vmware-policy"]},"homepage":"https://github.com/vmware-skills/VMware-Harden","os":["macos","linux"]}}
---

# VMware Harden (Compliance & Baseline)

> Self-test: [guide](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and "vSphere" are trademarks of Broadcom. Source code is publicly auditable at [github.com/vmware-skills/VMware-Harden](https://github.com/vmware-skills/VMware-Harden) under the MIT license.

AI-native VMware compliance scanner — built-in CIS / vSphere SCG / 等保 2.0 三级 / PCI-DSS / BSI IT-Grundschutz / EU NIS2 baselines, a VMSA known-vulnerability check, drift detection, LLM-driven remediation advice, and a web dashboard.

> **Companion skills**: [vmware-aiops](https://github.com/vmware-skills/VMware-AIops) (inventory + collectors data source; host/VM remediation target), [vmware-monitor](https://github.com/vmware-skills/VMware-Monitor) (read-only inspection), [vmware-storage](https://github.com/vmware-skills/VMware-Storage) (datastore remediation target), [vmware-nsx](https://github.com/vmware-skills/VMware-NSX) (segment/gateway evidence), [vmware-nsx-security](https://github.com/vmware-skills/VMware-NSX-Security) (DFW evidence + remediation target), [vmware-aria](https://github.com/vmware-skills/VMware-Aria) (metrics correlation), [vmware-avi](https://github.com/vmware-skills/VMware-AVI) (load balancer evidence), [vmware-vks](https://github.com/vmware-skills/VMware-VKS) (Tanzu Kubernetes evidence), [vmware-pilot](https://github.com/vmware-skills/VMware-Pilot) (remediation execution with approval gates), [vmware-policy](https://github.com/vmware-skills/VMware-Policy) (audit log). See [references/cross-skill-workflows.md](./references/cross-skill-workflows.md) for end-to-end remediation flows that span pilot + sibling skills.

## What This Skill Does

| Category | Tools | Count | Read or Write |
|----------|-------|-------|---------------|
| Baseline Management | 9 built-in baselines (CIS ESXi 8.0/9.0, vSphere SCG v8/v9, vSphere 9 STIG, 等保 2.0 L3, PCI-DSS 4.0, BSI ITGS, EU NIS2) + custom YAML loader | 9+N | Read |
| Known Vulnerabilities | `vmsa-advisories`: ESXi and vCenter builds against an offline VMSA catalog (NVD + CISA KEV + Broadcom build KBs) → affected / fixed / unknown | 1 baseline | Read |
| Scanning | Multi-collector (vCenter, ESXi, NSX, vSAN, K8s) → typed Twin store | 1 pipeline | Read (no target writes) |
| Drift Detection | Snapshot-to-snapshot configuration diff (per-node added/removed/changed fields) | 1 type | Read |
| Remediation Advisor | LLM-driven (Anthropic) suggestions per violation; mock fallback when no key | 1 advisor | Read |
| Web Dashboard | FastAPI + Jinja2 read-only UI for violations / drift / advice | 1 server | Read |
| MCP Server | Compliance query tools | 8 | All Read |

For VMSA reports, read each node's `cves`, `cve_results` and `fixed_in`. Rule severity describes the
whole advisory; `max_affected_cvss` describes the CVEs still affecting that node. Missing mappings or
builds remain unknown. See [advisory evidence and refresh provenance](references/cli-reference.md#advisories).

## Quick Install

```bash
uv tool install "vmware-harden[collectors]==1.20.0"
vmware-harden baseline list
```

The `[collectors]` extra is what `scan` needs: inventory is read through vmware-aiops / vmware-storage / vmware-nsx-security, and `uv tool install` isolates each tool's environment — installing those packages on their own leaves harden unable to import them. Plain `uv tool install vmware-harden==1.20.0` is enough to report on an existing twin DB.

For first-time use, ensure a vmware-aiops target is configured (harden uses aiops collectors) and optionally set `ANTHROPIC_API_KEY` for live remediation advice.

## When to Use This Skill

Use vmware-harden when the user needs to:

- Run a **compliance scan** against CIS / vSphere SCG / **vSphere 9 STIG-aligned** / 等保 2.0 三级 / PCI-DSS / BSI IT-Grundschutz / EU NIS2
- **Author or import a custom YAML baseline** (e.g., internal corporate baseline)
- Detect **drift** between two scans of the same target
- Get **AI-suggested remediation steps** for a violation (advice only — does not execute)
- Browse a **web dashboard** of compliance posture across multiple targets

**Do NOT use this skill when**:

- The task is general vCenter/ESXi monitoring or read-only inspection → use **vmware-monitor**
- The task is VM lifecycle, snapshots, or guest operations → use **vmware-aiops**
- The user wants to actually **execute** a remediation (set advanced setting, change DFW rule, etc.) → use **vmware-pilot** (multi-step approval-gated workflow)
- The task is purely NSX networking/segments → use **vmware-nsx**
- The user wants **continuous, fleet-wide compliance enforcement + automated remediation** across the estate → use **VCF Operations SPM/ACC (UI)**. VCF Operations 9.1 Automated Configuration Compliance / Security Posture Management is UI- and schedule-driven (paid Salt engine) and exposes **no public compliance API**. harden is the complementary, **API-scriptable, DuckDB-persisted, cross-target point-in-time scanner** for CI and agent workflows; it does not replace SPM/ACC. See [references/stig-content-sync.md](./references/stig-content-sync.md).

## Related Skills — Skill Routing

| User Intent | Recommended Skill |
|-------------|-------------------|
| "Scan ESXi for CIS compliance" | **vmware-harden** ← this skill |
| "Scan against the vSphere 9 STIG" | **vmware-harden** (`--baseline vsphere-stig-v9-subset`) |
| "Continuous fleet-wide enforcement + auto-remediation" | **VCF Operations SPM/ACC (UI)** — no public API; harden is the scriptable point-in-time scanner |
| "Check 等保 2.0 三级" | **vmware-harden** |
| "What changed since last week?" (drift) | **vmware-harden** |
| "Fix this violation now" | **vmware-pilot** (approval-gated execution) |
| "List VMs / hosts / alarms" | **vmware-monitor** |
| "Reconfigure / power / migrate VM" | **vmware-aiops** |
| "Edit DFW rule" | **vmware-nsx-security** |
| "Browse audit log" | **vmware-policy** (`vmware-audit log`) |

## Common Workflows

### 1. First-time scan with 等保 2.0 三级

1. Install: `uv tool install "vmware-harden[collectors]==1.20.0"` (the extra carries the inventory collectors `scan` reads through)
2. Verify aiops is configured: `vmware-aiops doctor` — harden reuses aiops connection for the vCenter collector
3. List baselines: `vmware-harden baseline list` — confirm `dengbao-2.0-level3-vmware` is present
4. Scan: `vmware-harden scan --baseline dengbao-2.0-level3-vmware --target prod-vcenter`
5. Report: `vmware-harden report --format json > violations.json` (or `vmware-harden web` for the rendered dashboard). The JSON is an object — `{"violations": [...], "coverage": {...}, "snapshot": {...}}` — read `coverage` before reporting a result, and `snapshot` to say which scan it is (a failed scan is excluded, so `snapshot.note` warns when the results predate later failed scans); an empty `violations` list only means nothing was found among the checks that could be made.

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

### 4. Known vulnerabilities (VMSA)

0. Optional: `vmware-harden advisories update` refreshes KEV (exploited-in-the-wild) flags from CISA (and, with `--nvd`, missing CVSS from NVD) into a local cache, and lists ESXi/vCenter KEV CVEs the catalog does not carry yet. It never changes which builds fix what. `vmware-harden advisories show` prints the catalog date and when KEV was last refreshed.
1. Scan: `vmware-harden scan --baseline vmsa-advisories --target prod-vcenter` — one rule per catalogued advisory, over the ESXi hosts and the vCenter itself
2. Report: `vmware-harden report` (each affected component shows its fix and whether the CVE is in CISA KEV) or `vmware-harden report --format csv > vmsa.csv` for the security team
3. Read the result as three states: **affected** (a violation, with the release that fixes it), **fixed**, and **unknown** (listed per node with the reason). A clean result means "no open advisory known as of the catalog date" (printed in every rule) — never "not vulnerable"; advisories published after that date are not in the catalog.

   **Failure branch**: A component listed as unknown has a reason beside it — an unreadable build, a line the advisory does not list (or that reached end of support), a branch the sources disagree on, or a product the catalog does not carry yet. None of these is a pass; check the advisory on Broadcom's site for that component.

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local CLI scans by an operator | **CLI** | Direct, scripts well into CI |
| AI agent integration | **MCP** | 8 read-only tools, structured responses |
| Reviewing posture interactively | **Web** | `vmware-harden web` — sortable tables, drift timeline |
| CI/CD pipeline gates | **CLI** | Exit code reflects compliance pass/fail |

## MCP Tools (8 — 8 read, 0 write)

| Category | Tool | Description |
|----------|------|-------------|
| Baseline | `list_baselines` | All built-in + imported baselines (id, framework, version) |
| Baseline | `get_baseline_rules` | Rules for a given baseline_id (severity, references) |
| STIG | `list_stig_controls` | vSphere 9 STIG-aligned controls (id, severity, ESXi advanced setting) |
| STIG | `describe_stig_content_sync` | How harden syncs STIG content + routing to SPM/ACC (no compliance API) |
| Violation | `list_violations` | Current violations, filterable by severity |
| Violation | `get_remediation` | Remediation suggestion for a violation_id (LLM or mock) |
| Drift | `list_drift_events` | Recent drift events from snapshot diff |
| Scan | `scan_target` | Trigger a scan against a target (read-only on the target) |

All 8 tools are **read-only** with respect to vSphere/NSX. Writes to the local Twin DuckDB are scan-internal and do not modify any VMware resource. Harden never runs a remediation: the CLI-only `vmware-harden apply` saves a Suggestion as a **pending** vmware-pilot workflow and stops — nothing changes until someone runs it through pilot and approves its gate (see [references/cross-skill-workflows.md](./references/cross-skill-workflows.md)).

**List results are enveloped.** `list_baselines`, `get_baseline_rules`, and `list_drift_events` return `{items, returned, limit, total, truncated, hint}` rather than a bare list, so completeness is stated rather than inferred — read the rows from `items`, and treat `truncated: true` as "there is more, raise `limit`". Because the twin is a local DuckDB, `total` is a real count, not an estimate: a page that exactly fills `limit` is still reported `truncated: false` when it is genuinely the whole set. `list_violations` keeps its own older `{violations, total, limit, offset, has_more}` envelope with the same guarantee.

**An empty violation list is not a compliance verdict.** A rule can only judge configuration that was actually gathered, and that fails two independent ways — both reported, neither as passing:

- **No collector produces the attribute**, so the rule was never run → `coverage.undetermined` with `undetermined_rules` naming the attribute. Collector work.
- **The rule ran but found no value on a given node** (host unreachable, account lacks the privilege, setting absent on that build) → `coverage.node_checks_undetermined` with `undetermined_node_checks` naming the rule, node and missing attribute. Access work. A rule that found no node of its type at all is listed in `coverage.rules_without_targets`.

`list_violations` and `scan_target` return the full `coverage` block (`{evaluated, undetermined, total, tracked, complete, undetermined_rules, node_checks_evaluated, node_checks_undetermined, node_checks_total, nodes_affected, node_tracked, undetermined_node_checks, rules_without_targets}`) plus a `note` summarising it. Read it before summarising: when `complete` is false, say what was not checked and never call the estate compliant or clean. `tracked: false` means the snapshot predates coverage tracking; `node_tracked: false` means it predates per-node tracking (pre-v1.10.0) — re-scan rather than assume either.

## CLI Quick Reference

```bash
vmware-harden baseline list
vmware-harden baseline import <path>
vmware-harden baseline validate <path>
vmware-harden scan --baseline <id> --target <name>
vmware-harden report [--format text|json|csv]
vmware-harden scan --baseline vmsa-advisories --target <name>   # known vulnerabilities
vmware-harden advisories show | update [--nvd]                  # catalog date / optional KEV (+NVD) refresh
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
  "command": "vmware-harden",
  "args": ["mcp"]
}
```

This avoids `uvx` re-resolving PyPI through the corporate MitM proxy. The legacy `vmware-harden-mcp` console script still works and is equivalent. As a workaround, `UV_NATIVE_TLS=true` lets uv use the system CA store. See CLAUDE.md 踩坑 #25.

### "Twin DB not found" on first MCP call
Run at least one scan first: `vmware-harden scan --baseline cis-vmware-esxi-8.0-subset --target <t>`. The DuckDB file is created on first scan at `~/.vmware-harden/twin.duckdb` (override with `VMWARE_HARDEN_DB`).

### 等保 baseline reports most rules as not evaluated
Three different causes, and the report distinguishes them. A rule whose attribute no collector produces is recorded `undetermined` with the reason naming that attribute — see `coverage.undetermined_rules`; those are collector work, tracked in RELEASE_NOTES. Separately, the 等保 baseline spans several collectors (vCenter advanced settings + NSX DFW), so if only the vCenter collector ran, the DFW rules have no nodes to match — they appear in `coverage.rules_without_targets`, not as passes. Third, individual hosts missing a value show up in `coverage.undetermined_node_checks`; that one is usually privilege or reachability, not a missing collector. Run a scan with all collectors installed, or pick a baseline whose `applies_to` matches what you have.

### Web dashboard shows 0 violations even after a scan
Verify the dashboard is reading the same DuckDB. If `VMWARE_HARDEN_DB` is set in your shell but not in the systemd/launchd unit running `vmware-harden web`, the web server reads the default `~/.vmware-harden/twin.duckdb` while your scans wrote elsewhere.

## Audit & Safety

1. **Source code**: [github.com/vmware-skills/VMware-Harden](https://github.com/vmware-skills/VMware-Harden) — MIT license, publicly auditable.
2. **Config / state files**: custom baselines in `~/.vmware-harden/baselines/*.yaml`; Twin DuckDB at `~/.vmware-harden/twin.duckdb`; the optional advisory refresh cache at `~/.vmware-harden/advisories-cache.json`. No passwords are stored — all credentials live in the upstream skill (`~/.vmware-aiops/.env`).
3. **Webhook data scope**: none. Harden makes **no outbound network calls** other than (a) optional Anthropic API requests when `ANTHROPIC_API_KEY` is set for advisor suggestions, (b) the local web dashboard bound to `127.0.0.1` by default, and (c) `vmware-harden advisories update`, run only on request and audited, which downloads public data from cisa.gov (KEV feed) and, with `--nvd`, nvd.nist.gov (one request per catalogued CVE), and sends nothing about your estate.
4. **TLS verification**: harden does not connect to vCenter/NSX directly — TLS handling is delegated to vmware-aiops. The advisor's HTTPS calls to `api.anthropic.com` and the advisory refresh's calls to cisa.gov / nvd.nist.gov use system TLS verification (no opt-out).
5. **Prompt injection protection**: advisor LLM context is built exclusively from typed Twin queries (rule id, severity, evidence dict) — no free-text user input is forwarded. Evidence text passes through `_sanitize()` (truncate ≤500 chars, strip C0/C1 control characters).
6. **Least privilege**: all 8 MCP tools are read-only, and no harden command changes a VMware system. The CLI-only `apply` hands a Suggestion to **vmware-pilot** as a pending workflow; execution happens only in pilot, after its approval gate, under the sibling skill's own gate and audit.

All MCP operations are audited via the `@vmware_tool` decorator (vmware-policy dependency) to `~/.vmware/audit.db`. View with `vmware-audit log --last 20`.

**Environment scoping**: policy rules apply per environment, and skills that connect to a VMware estate declare `environment:` per target in their `config.yaml`. Harden has no such config — it reads through vmware-aiops and writes only its local Twin DB — so it reports a constant `local`. `scan_target` is its only state-changing tool, and the state it changes is the snapshot in that local DB; its vCenter interaction is read-only collection. No harden tool mutates a remote VMware estate, so there is no production change for an environment-scoped rule to protect.

> Full setup / security / AI platform compatibility: see [references/setup-guide.md](./references/setup-guide.md)

## License

MIT — [github.com/vmware-skills/VMware-Harden](https://github.com/vmware-skills/VMware-Harden)

## Current evidence boundary

DFW section_name comes from the actual parent policy display_name. Missing parent names remain undetermined. Library posture/pairwise snapshot helpers do not imply a CLI/MCP feature, and inherited baselines do not establish 9.x live validation. See `references/capabilities.md`.
