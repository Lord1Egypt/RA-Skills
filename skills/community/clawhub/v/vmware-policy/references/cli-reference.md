# VMware Policy -- CLI Reference

Complete command reference for the `vmware-audit` CLI.

## Global Options

The `vmware-audit` CLI reads from `~/.vmware/audit.db` (SQLite WAL mode).

## Commands

### vmware-audit log

Show recent audit log entries with optional filtering.

```bash
vmware-audit log [OPTIONS]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--last` | INTEGER | 20 | Number of recent entries to show |
| `--skill` | TEXT | None | Filter by skill name (e.g., `vmware-nsx`) |
| `--tool` | TEXT | None | Filter by tool name (e.g., `delete_segment`) |
| `--status` | TEXT | None | Filter by status: `ok`, `denied`, `error`, `ok_bypassed` |
| `--workflow-id` | TEXT | None | Filter by workflow ID (from vmware-pilot) |
| `--since` | TEXT | None | Show entries after date (ISO format, e.g., `2026-03-28`) |

**Examples**:

```bash
# Show last 20 entries (default)
vmware-audit log

# Show last 50 entries for NSX skill
vmware-audit log --skill vmware-nsx --last 50

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
vmware-audit export --skill vmware-aiops --since 2026-03-01 > aiops-march.json

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
- Breakdown by status (ok, denied, error)
- Breakdown by skill (sorted by count descending)

## Status Values

| Status | Meaning |
|--------|---------|
| `ok` | Operation completed successfully |
| `denied` | Blocked by policy rule |
| `error` | Operation failed with exception |
| `ok_bypassed` | Completed with policy disabled (`VMWARE_POLICY_DISABLED=1`) |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `VMWARE_POLICY_DISABLED` | Set to `1` to bypass policy checks (still logged as `_bypassed`) |

## Database Location

Default: `~/.vmware/audit.db`

The database uses SQLite WAL mode for concurrent write safety. Automatic rotation at 100MB with 5 archive retention.
