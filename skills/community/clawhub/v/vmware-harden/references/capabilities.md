# Capabilities

Detailed reference for every MCP tool exposed by `vmware-harden-mcp`.
Source of truth: `mcp_server/server.py`.

## Automation Level Reference

Per the Enterprise Harness Engineering autonomy framework, every tool in
this skill is **L1 (read-only raw data)** or **L2 (read + analysis)**
with respect to the managed VMware estate. The Twin DuckDB at
`~/.vmware-harden/twin.duckdb` is written by `scan_target`, but no
vSphere/NSX resource is ever modified by this skill.

| Level | Meaning | Tools in this skill |
|:-:|---|---|
| **L1** | Read-only, raw data — agent may auto-call | `list_baselines`, `get_baseline_rules`, `list_violations`, `list_drift_events`, `get_remediation` |
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
list_baselines() -> list[dict]
```

### When to use

The agent needs to enumerate which compliance frameworks the user can
scan against — for example to answer "which baselines do you support?"
or to choose the right `baseline_id` before calling `scan_target`.

### Parameters

None.

### Returns

A list of baseline summaries:

```json
[
  {
    "id": "cis-vmware-esxi-8.0-subset",
    "name": "CIS VMware ESXi 8.0 (subset)",
    "version": "1.0",
    "applies_to": ["host"],
    "rule_count": 12
  }
]
```

If a baseline file fails to load, its entry contains `{"id": "...", "error": "failed to load: ..."}`
instead of the metadata fields.

### Gotchas

- Includes both built-ins and user imports under `~/.vmware-harden/baselines/`.
- The `applies_to` field tells the agent which collectors must run during
  a scan; if the user has only `vmware-aiops` configured (no NSX), pick a
  baseline whose `applies_to` is a subset of the available collectors.

### Typical response tokens

~200–400 tokens (4 baselines × ~80 tokens each).

## Tool 2: `list_violations`

### Signature

```python
list_violations(severity: str | None = None) -> list[dict]
```

### When to use

Show the agent the current compliance gaps, scoped to the latest
snapshot. Use the `severity` filter to focus the agent on critical /
high items only — this dramatically reduces context burn.

### Parameters

| Name | Type | Required | Description |
|------|------|:-:|-------------|
| `severity` | `str \| None` | No | Filter by severity, e.g. `"critical"`, `"high"`, `"medium"`, `"low"`. |

### Returns

```json
[
  {
    "id": "v-cis-1.1.1-host-esxi-01",
    "rule_id": "cis-1.1.1",
    "node_id": "host-esxi-01",
    "severity": "critical",
    "baseline_id": "cis-vmware-esxi-8.0-subset",
    "evidence": { "ntp_servers": [], "expected": ["pool.ntp.org"] }
  }
]
```

Returns `[]` when no scans exist or when the latest snapshot is clean.

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
list_drift_events(limit: int = 50) -> list[dict]
```

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
[
  {
    "node_id": "host-esxi-01",
    "field": "ntp.servers",
    "old_value": "pool.ntp.org",
    "new_value": null,
    "detected_at": "2026-05-03 12:34:56"
  }
]
```

### Gotchas

- Reads the **latest snapshot** only; events represent changes **into**
  that snapshot from its predecessor.
- `old_value` and `new_value` are stringified — JSON-typed values may
  appear as their string form.
- Returns `[]` if no snapshots exist or no changes were detected.

### Typical response tokens

- Lab estate, default limit: ~300–1500 tokens.
- Cap the agent's burn by passing a smaller `limit` (e.g. 10) when
  triaging.

## Tool 5: `get_baseline_rules`

### Signature

```python
get_baseline_rules(baseline_id: str) -> list[dict]
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
[
  {
    "id": "cis-1.1.1",
    "title": "Configure NTP",
    "severity": "high",
    "category": "network"
  }
]
```

### Gotchas

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
  "violations": 17
}
```

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
