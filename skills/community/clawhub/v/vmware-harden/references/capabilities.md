# Capabilities

Detailed reference for every MCP tool exposed by `vmware-harden-mcp`.
Source of truth: `vmware_harden/mcp_server/server.py`.

## Automation Level Reference

Per the Enterprise Harness Engineering autonomy framework, every tool in
this skill is **L1 (read-only raw data)** or **L2 (read + analysis)**
with respect to the managed VMware estate. The Twin DuckDB at
`~/.vmware-harden/twin.duckdb` is written by `scan_target`, but no
vSphere/NSX resource is ever modified by this skill.

| Level | Meaning | Tools in this skill |
|:-:|---|---|
| **L1** | Read-only, raw data — agent may auto-call | `list_baselines`, `get_baseline_rules`, `list_violations`, `list_drift_events`, `get_remediation`, `list_stig_controls`, `describe_stig_content_sync` |
| **L2** | Read + analysis (LLM advisor uses Twin evidence only) | `get_remediation` (when populated by `advise`) |
| **L3** | Single write — user must approve | *N/A* — use **vmware-pilot** |
| **L4** | Multi-step plan / apply | *N/A* — use **vmware-pilot** |
| **L5** | Auto-remediation | *N/A* (out of scope by design) |

`scan_target` is classified `risk_level="medium"` by `@vmware_tool` solely
because it triggers heavy upstream I/O (vSphere/NSX collectors) and
writes a snapshot to local DuckDB. It does **not** modify the target.

## Tool 1: `list_baselines`

### Signature

```python
list_baselines() -> dict   # family list envelope
```

### When to use

The agent needs to enumerate which compliance frameworks the user can
scan against — for example to answer "which baselines do you support?"
or to choose the right `baseline_id` before calling `scan_target`.

### Parameters

None.

### Returns

The family list envelope, whose `items` are baseline summaries:

```json
{
  "items": [
    {
      "id": "cis-vmware-esxi-8.0-subset",
      "name": "CIS VMware ESXi 8.0 (subset)",
      "version": "1.0",
      "applies_to": ["host"],
      "rule_count": 12
    }
  ],
  "returned": 6,
  "limit": null,
  "total": 6,
  "truncated": false,
  "hint": null
}
```

If a baseline file fails to load, its entry contains `{"id": "...", "error": "failed to load: ..."}`
instead of the metadata fields.

### Gotchas

- Includes both built-ins and user imports under `~/.vmware-harden/baselines/`.
- Every discovered baseline is listed, so `truncated` is always `false` and
  `total` is exact — this is the complete set, never a page of it.
- The `applies_to` field tells the agent which collectors must run during
  a scan; if the user has only `vmware-aiops` configured (no NSX), pick a
  baseline whose `applies_to` is a subset of the available collectors.

### Typical response tokens

~200–400 tokens (4 baselines × ~80 tokens each).

## Tool 2: `list_violations`

### Signature

```python
list_violations(severity: str | None = None, limit: int = 50, offset: int = 0) -> dict
```

Returns `{violations, total, limit, offset, has_more, coverage, note, snapshot}`.

`snapshot` names the scan the rows come from: `{id, target, finished_at,
later_unfinished, headline, note}`. Failed and running scans are never reported
on, so the rows can be older than the scan just run — when later scans of the
same target did not complete, `later_unfinished` counts them and `note` says so.
Tell the user which scan the answer comes from whenever `note` is set. `snapshot`
is `null` when no scan has completed.

### When to use

Show the agent the current compliance gaps, scoped to the latest
snapshot. Use the `severity` filter to focus the agent on critical /
high items only — this dramatically reduces context burn.

### Reading the result — `violations: []` is not "compliant"

A rule can only judge configuration that was actually gathered, and that fails
two independent ways. A rule whose attribute **no collector produces** is not
executed. A rule that *does* run can still judge nothing about one node, because
the value arrived absent or as the `N/A` sentinel there. Neither is a pass. Read
`coverage` alongside the violation list:

```json
"coverage": {"evaluated": 4, "undetermined": 16, "total": 20,
             "tracked": true, "complete": false,
             "undetermined_rules": [{"rule": "cis-esxi-2.1.1",
                                     "reason": "no collector writes host.ntp_enabled"}],
             "node_checks_evaluated": 3, "node_checks_undetermined": 5,
             "node_checks_total": 8, "nodes_affected": 2, "node_tracked": true,
             "undetermined_node_checks": [{"rule": "cis-esxi-2.2.1",
                                           "node": "host-esxi-02",
                                           "missing": "esxi_build"}],
             "rules_without_targets": []}
```

- `complete: true` — every rule ran and reached a verdict on every node in its
  scope; an empty violation list does mean compliant against this baseline.
- `complete: false` — say what was checked and what was not. State both ratios;
  do not summarise the scan as "compliant" or "clean".
- `undetermined` / `undetermined_rules` — nothing collects that attribute.
  Collector work; the affected rules did not run at all.
- `node_checks_undetermined` / `undetermined_node_checks` — the rule ran, but
  that node had no value to judge. Usually the scanning account's privileges or
  the host's reachability, not a missing collector. Counted in (rule, node)
  pairs; `nodes_affected` is the distinct node count.
- `rules_without_targets` — the rule ran and found no node of its type at all,
  so its "no violations" covers an empty set. Often a collector that returned
  nothing.
- `tracked: false` — the snapshot predates coverage tracking (pre-v1.9.0).
  `node_tracked: false` — it predates per-node tracking (pre-v1.10.0). Either
  way its coverage is unknown; re-scan before drawing a conclusion.

Both `undetermined_rules` and `undetermined_node_checks` are capped pages;
`undetermined_rules_truncated` / `undetermined_node_checks_truncated` say so.
The counts beside them are always complete.

`note` carries the same statement in prose, or `null` when coverage is complete.

### Parameters

| Name | Type | Required | Description |
|------|------|:-:|-------------|
| `severity` | `str \| None` | No | Filter by severity, e.g. `"critical"`, `"high"`, `"medium"`, `"low"`. |

### Returns

```json
{
  "violations": [
    {
      "id": "v-cis-2.2.1-host-esxi-01",
      "rule_id": "cis-esxi-2.2.1",
      "node_id": "host-esxi-01",
      "severity": "high",
      "baseline_id": "cis-vmware-esxi-8.0-subset",
      "evidence": { "id": "host-esxi-01", "name": "esxi-01",
                    "category": "patching", "title": "Ensure ESXi build is current" }
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0,
  "has_more": false,
  "coverage": { "...": "see above" },
  "note": null
}
```

`violations` is `[]` when no scans exist, or when nothing was found among the
rules that could be evaluated. It is **not** a statement that the estate is
clean — check `coverage.complete` before saying so.

### Gotchas

- Only returns violations from the **most recent snapshot** (the entire
  estate's last `scan_target` call). It is not a cross-snapshot query.
- `evidence` is parsed JSON; if the stored evidence is not valid JSON it
  comes back as `null` rather than raising.
- For very large estates, always pass `severity="critical"` or
  `severity="high"` first to keep the agent's context small.

### Typical response tokens

- Empty: ~10 tokens.
- Filtered (`severity="critical"`), typical lab: ~500–1500 tokens.
- Unfiltered, large estate (200 violations): can exceed 8 000 tokens —
  prefer the filter.

## Tool 3: `get_remediation`

### Signature

```python
get_remediation(violation_id: str) -> dict | None
```

### When to use

Fetch the persisted remediation suggestion for a single violation. Call
this **after** the user (or a previous turn) has run
`vmware-harden advise` against the same `violation_id`; otherwise the
result is `None` and the agent should suggest running `advise` first.

### Parameters

| Name | Type | Required | Description |
|------|------|:-:|-------------|
| `violation_id` | `str` | Yes | Violation id (matches `id` from `list_violations`). |

### Returns

A `Suggestion` dict (Pydantic `model_dump(mode="json")`) or `None`:

```json
{
  "summary": "Configure NTP servers on the ESXi host to align with corporate policy.",
  "execution_plan": { "steps": [ ... ] },
  "impact_prediction": {
    "affects_running_workload": false,
    "requires_maintenance_window": false
  },
  "confidence": 0.82,
  "human_review_required": true
}
```

### Gotchas

- Returns `None` if `advise` has not been run for this violation.
- The advisor never executes anything — it produces *suggestions only*.
  Execution is intentionally routed through **vmware-pilot**.
- Suggestions generated under the `MockProvider` (no `ANTHROPIC_API_KEY`)
  carry `confidence=0.5` and `human_review_required=true` and contain a
  generic placeholder summary.

### Typical response tokens

~300–800 tokens depending on the size of `execution_plan.steps`.

## Tool 4: `list_drift_events`

### Signature

```python
list_drift_events(limit: int = 50) -> dict   # family list envelope + snapshot
```

The envelope carries the same `snapshot` block as `list_violations`.

### When to use

Surface what changed between the most recent two snapshots of any
target. Useful for "what changed since last week" or as a triage feed
when a sudden compliance drop appears.

### Parameters

| Name | Type | Required | Description |
|------|------|:-:|-------------|
| `limit` | `int` | No | Max events to return (default `50`). |

### Returns

```json
{
  "items": [
    {
      "node_id": "host-esxi-01",
      "field": "ntp.servers",
      "old_value": "pool.ntp.org",
      "new_value": null,
      "detected_at": "2026-05-03 12:34:56"
    }
  ],
  "returned": 1,
  "limit": 50,
  "total": 1,
  "truncated": false,
  "hint": null
}
```

### Gotchas

- Reads the **latest snapshot** only; events represent changes **into**
  that snapshot from its predecessor.
- `old_value` and `new_value` are stringified — JSON-typed values may
  appear as their string form.
- Returns an empty envelope (`total: 0`) if no snapshots exist or no changes
  were detected — a complete answer of zero rows, not a maybe.
- `total` is the snapshot's exact change-event count (a `COUNT(*)` over the
  same predicate, served by `idx_change_event_snapshot`), so `truncated`
  answers definitively whether rows were left behind. Raise `limit` when it
  is `true`.

### Typical response tokens

- Lab estate, default limit: ~300–1500 tokens.
- Cap the agent's burn by passing a smaller `limit` (e.g. 10) when
  triaging.

## Tool 5: `get_baseline_rules`

### Signature

```python
get_baseline_rules(baseline_id: str) -> dict   # family list envelope
```

### When to use

The agent needs to explain to the user what a baseline checks for, or to
correlate a `rule_id` from `list_violations` to a human-readable title /
category.

### Parameters

| Name | Type | Required | Description |
|------|------|:-:|-------------|
| `baseline_id` | `str` | Yes | A baseline id from `list_baselines`. |

### Returns

```json
{
  "items": [
    {
      "id": "cis-1.1.1",
      "title": "Configure NTP",
      "severity": "high",
      "category": "network"
    }
  ],
  "returned": 20,
  "limit": null,
  "total": 20,
  "truncated": false,
  "hint": null
}
```

### Gotchas

- The whole baseline is returned, so `truncated` is always `false` and
  `total` is the exact rule count.
- Raises (and the MCP layer surfaces a tool error) if the
  `baseline_id` is not a built-in. User imports are loaded via the same
  loader, so imported ids work too.
- The full `check.path` / `expect` payload is **not** returned — only
  the metadata. To inspect the raw YAML, look under
  `vmware_harden/baselines/builtins/<id>.yaml` or
  `~/.vmware-harden/baselines/`.

### Typical response tokens

~300–600 tokens (12–20 rules × ~25 tokens).

## Tool 6: `scan_target`

### Signature

```python
scan_target(
    target: str,
    baseline: str = "cis-vmware-esxi-8.0-subset"
) -> dict
```

### When to use

Trigger a fresh compliance scan from inside the agent loop. This is the
**only** tool in the skill that performs heavy network I/O (it walks the
upstream `vmware-aiops` collectors against the live vCenter / NSX).

### Parameters

| Name | Type | Required | Description |
|------|------|:-:|-------------|
| `target` | `str` | Yes | vCenter target name from upstream `vmware-aiops` config. |
| `baseline` | `str` | No | Baseline id. Default `"cis-vmware-esxi-8.0-subset"`. |

### Returns

A small summary:

```json
{
  "snapshot_id": "snap-2026-05-03T12:34:56-...",
  "target": "lab-vc01",
  "baseline": "cis-vmware-esxi-8.0-subset",
  "hosts": 4,
  "violations": 17,
  "coverage": {"evaluated": 4, "undetermined": 16, "total": 20,
               "tracked": true, "complete": false,
               "undetermined_rules": [
                 {"rule": "cis-esxi-2.1.1",
                  "reason": "no collector writes host.ntp_enabled"}],
               "node_checks_evaluated": 3, "node_checks_undetermined": 5,
               "node_checks_total": 8, "nodes_affected": 2,
               "node_tracked": true,
               "undetermined_node_checks": [
                 {"rule": "cis-esxi-2.2.1", "node": "host-esxi-02",
                  "missing": "esxi_build"}],
               "rules_without_targets": []},
  "note": "16 of 20 rules could not be evaluated — ... unknown, not compliant. 5 of 8 per-node checks could not be made across 2 node(s) — ..."
}
```

`violations` is only meaningful together with `coverage`: rules whose data no
collector gathers are **not executed**, and a rule that did run still judged
nothing about a node whose value was missing. Both count as undetermined rather
than passing. Do not report an estate as compliant when `coverage.complete` is
false — say how many rules were evaluated out of how many, and how many per-node
checks were made out of how many. See
[Tool 2](#tool-2-list_violations) for the full field description.

### Gotchas

- **This is the heavy tool.** Lab scans of CIS subset against 4 hosts
  take 5–30 s. 等保 2.0 三级 across multi-collector estates can take
  minutes. Agents should not call this in tight loops; prefer
  `list_violations` to reread the latest snapshot.
- Risk level is `"medium"` in `@vmware_tool` (audited) although the
  target is not modified — the elevation reflects upstream API load and
  local DuckDB writes.
- Requires a working `vmware-aiops` target with the same name; if the
  upstream is unconfigured, the underlying collectors raise and the tool
  returns a tool error to the agent.

### Typical response tokens

~80–150 tokens (the response is intentionally a compact summary; the
agent should follow up with `list_violations` for details).

## Performance & Correctness Notes

### Snapshot-keyed indexes (v1.5.19)

`vmware_harden/store/schema.py` declares `CREATE INDEX IF NOT EXISTS`
indexes on `violation.snapshot_id`, `node_state.snapshot_id`, and
`change_event.snapshot_id`. Every `list_violations` /
`list_drift_events` / `report` query filters by `snapshot_id`; without
these indexes DuckDB performed a full table scan whose cost grew with
the cumulative scan history. New installs pick the indexes up on first
`scan`; existing installs pick them up on the next `scan` after upgrade
(the `IF NOT EXISTS` guard makes this idempotent — no migration needed).
See CLAUDE.md 踩坑 #28.

### Orphan violations are preserved in reports (v1.5.19)

`vmware-harden report` (and the corresponding `list_violations` MCP
tool) use `LEFT JOIN nodes` with `COALESCE(name, '[orphan]')` so
violations whose node has been deleted between scans **still appear** in
the result set, labelled `[orphan]`. The previous `INNER JOIN` silently
dropped them, which made drift scenarios (node deleted, violations went
away) appear falsely clean. Agents should treat a violation whose node
renders as `[orphan]` as a deleted-node finding worth surfacing to the
user. See CLAUDE.md 踩坑 #29.

---

## Tool 7: `list_stig_controls`

### Signature

```python
list_stig_controls(limit: int = 50, offset: int = 0) -> dict
```

### When to use

Inspect the `vsphere-stig-v9-subset` catalog without running a scan — to answer
"which STIG controls does harden cover, and which ESXi setting does each
govern?", or to map a violation's `rule_id` back to its advanced setting.

### Parameters

| Name | Type | Required | Description |
|------|------|:-:|-------------|
| `limit` | `int` | No | Page size. Default 50. |
| `offset` | `int` | No | Row offset for paging. Default 0. |

### Returns

The family list envelope `{items, returned, limit, total, truncated, hint}`.
Each item is `{id, title, severity, category, advanced_setting}`, where
`advanced_setting` is the ESXi advanced setting the control governs (e.g.
`Security.AccountLockFailures`). The catalog is paged locally, so `total` is
exact.

### Gotchas

- Rule ids use harden's own `stig-esxi9-*` namespace and are **not** DISA
  V-IDs / STIG-IDs. The stable cross-reference to official content is
  `advanced_setting`, not the id.
- The catalog is static content; it says nothing about any estate. Run
  `scan_target` for findings.

### Typical response size

12 controls, ≈ 900 tokens for the full catalog.

---

## Tool 8: `describe_stig_content_sync`

### Signature

```python
describe_stig_content_sync() -> dict
```

### When to use

Answer "why doesn't harden just call the VCF Operations compliance API?", or
decide whether a continuous-enforcement request belongs to harden or to VCF
Operations SPM/ACC.

### Parameters

None.

### Returns

`{compliance_api_available, why_no_api, content_sources, mechanism,
routing_note, importer_status}` — static, local, no I/O.

### Gotchas

- `importer_status` is `"deferred"`: `import_inspec_profile()` raises
  `NotImplementedError`. Do not present InSpec/Cinc import as available.
- Routing, not capability: for fleet-wide continuous enforcement the answer is
  VCF Operations SPM/ACC (UI-driven), not harden.

### Typical response size

≈ 400 tokens.

## VMRC clipboard evidence

`vm.isolation_copy_disabled` represents both per-VM copy/paste disable settings being
explicitly true. Either explicit false fails that configuration requirement; absent,
unreadable, malformed or duplicate settings cannot establish compliance. A disconnected
VM contributes no measured security facts. The collector retains only the derived
boolean, never raw extraConfig or unrelated guestinfo values. This is not a runtime
clipboard test. SCG `scg-vm-5` and its inherited v9 rule report missing facts as node gaps.

## Maintenance safety boundary

DFW section_name comes from the actual parent policy display_name. Missing parent names remain undetermined. Library posture/pairwise snapshot helpers do not imply a CLI/MCP feature, and inherited baselines do not establish 9.x live validation.
