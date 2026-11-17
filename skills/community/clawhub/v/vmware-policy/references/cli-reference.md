# VMware Policy -- CLI Reference

Complete command reference for the `vmware-audit` CLI.

## Global Options

The `vmware-audit` CLI reads from `~/.vmware/audit.db` (SQLite WAL mode), or `$OPS_HOME/audit.db` when `OPS_HOME` is set.

## Commands

### vmware-audit log

Show recent audit log entries with optional filtering.

```bash
vmware-audit log [OPTIONS]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--last` | INTEGER | 20 | Number of recent entries to show |
| `--skill` | TEXT | None | Filter by skill short name, exact match (e.g., `nsx`, `aiops`, `nsx_security` -- not `vmware-nsx`) |
| `--tool` | TEXT | None | Filter by tool name (e.g., `delete_segment`) |
| `--status` | TEXT | None | Filter by status, exact match (see [Status Values](#status-values)) |
| `--workflow-id` | TEXT | None | Filter by workflow ID (from vmware-pilot) |
| `--since` | TEXT | None | Show entries after date (ISO format, e.g., `2026-03-28`) |

**Examples**:

```bash
# Show last 20 entries (default)
vmware-audit log

# Show last 50 entries for NSX skill
vmware-audit log --skill nsx --last 50

# Show denied operations in the last week
vmware-audit log --status denied --since 2026-03-25

# Show entries for a specific tool
vmware-audit log --tool delete_segment --last 10

# Filter by workflow
vmware-audit log --workflow-id wf-abc123
```

**Output columns**: Time, Skill, Tool, Status, Agent, Duration

### vmware-audit export

Export audit log as JSON to stdout for external processing.

```bash
vmware-audit export [OPTIONS]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--format` | TEXT | json | Export format (currently only `json`) |
| `--skill` | TEXT | None | Filter by skill name |
| `--since` | TEXT | None | Export entries after date (ISO format) |
| `--limit` | INTEGER | 10000 | Maximum number of entries to export |

**Examples**:

```bash
# Export all logs as JSON
vmware-audit export --format json > audit-full.json

# Export last month for a specific skill
vmware-audit export --skill aiops --since 2026-03-01 > aiops-march.json

# Pipe to jq for analysis
vmware-audit export | jq '[.[] | select(.status == "denied")]'
```

### vmware-audit stats

Show aggregate audit statistics over a time period.

```bash
vmware-audit stats [OPTIONS]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--days` | INTEGER | 7 | Number of days to analyze |

**Examples**:

```bash
# Last 7 days (default)
vmware-audit stats

# Last 30 days
vmware-audit stats --days 30

# Last 24 hours (approximate)
vmware-audit stats --days 1
```

**Output sections**:
- Total operations count
- Breakdown by status (ok, dry_run, denied, rejected, error, ...)
- Breakdown by skill (sorted by count descending)

### vmware-audit policy

Show which policy rules are in force and, optionally, what they do to one operation. Read-only.

```bash
vmware-audit policy [OPTIONS]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--operation`, `-o` | TEXT | "" | Tool name to evaluate, e.g. `delete_vm` |
| `--skill`, `-s` | TEXT | "" | Skill the tool belongs to (`aiops`, `vdi`, …): its pre-/post-2.0 names count, the same as enforcement. Omitted: every skill's old names for that tool |
| `--env`, `-e` | TEXT | "" | Target environment, e.g. `production` |
| `--risk`, `-r` | TEXT | medium | Risk level the tool declares |

Prints the rule source -- `user`, `packaged-default` (no rules file; the shipped baseline, which denies nothing), `user-unreadable` or `baseline-unreadable` (every operation denied) -- and the number of deny rules and whether a maintenance window is set. Exits with code 1 when the rules could not be loaded.

### vmware-audit undo-list / undo-show

List recorded undo tokens (`--status recorded|applied|expired`, `--last N`), or show the inverse operation recorded for one token (`undo-show <undo_id>`). Read-only -- neither command executes anything.

## Status Values

| Status | Meaning |
|--------|---------|
| `ok` | Operation completed successfully |
| `dry_run` | Completed with `dry_run=True` -- a preview; nothing changed |
| `denied` | Blocked by policy (deny rule, closed/malformed maintenance window, or `rules_unreadable`) |
| `error` | Operation raised; returned `{"error": ...}` or `outcome: "failed"`; exited with a non-zero `SystemExit` / Typer exit; or called `report_tool_failure`. `ok: false` / `success: false` alone are not read (vmware-aiops `vmk_ping` returns `success: false` as its answer) |
| `budget_exceeded` | Stopped by the `@vmware_tool` per-process call budget or runaway guard |
| `rejected` | CLI only: the operator declined the confirmation prompt |
| `interrupted` | Ctrl+C, or an MCP call the client cancelled -- the remote operation may still be running (shown in yellow) |
| `<status>_bypassed` | Call made with `VMWARE_POLICY_DISABLED=1`, from either the MCP (`@vmware_tool`) or the CLI (`@guarded`) surface (e.g. `ok_bypassed`, `error_bypassed`). |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPS_HOME` | Directory for `audit.db` and `rules.yaml` (default `~/.vmware`) |
| `VMWARE_POLICY_DISABLED` | Operator escape hatch: `1` skips all policy evaluation in that process (deny rules, maintenance window, unreadable-rules denial). Auditing continues; a warning is logged per call, and rows from both `@vmware_tool` (MCP) and `@guarded` (CLI) get the `_bypassed` suffix. Restrict who can set it. |

## Database Location

Default: `~/.vmware/audit.db`. The database records parameters and results and should be treated as sensitive -- see the setup guide's *Audit Database Security*.

The database uses SQLite WAL mode for concurrent write safety. Automatic rotation at 100MB with 5 archive retention.
