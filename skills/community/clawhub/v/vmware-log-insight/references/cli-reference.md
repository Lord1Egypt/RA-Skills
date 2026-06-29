# vmware-log-insight CLI Reference

All commands are read-only. Global options: `--target/-t <name>` (target from
config; default if omitted) and `--config/-c <path>` (override config file).

## search — search log events

```bash
vmware-log-insight search [OPTIONS]
  -q, --text TEXT       Free-text search (CONTAINS)
  -l, --last TEXT       Relative window: 1h, 30m, 7d   [default: 1h]
  -n, --limit INTEGER   Max events (1..20000)          [default: 50]
      --json            Raw JSON output (table otherwise)
```

Examples:
```bash
vmware-log-insight search -q "scsi apd" -l 2h
vmware-log-insight search -q error -l 30m --json
```

## aggregate — time series + spike detection

```bash
vmware-log-insight aggregate [OPTIONS]
  -q, --text TEXT       Free-text search
  -l, --last TEXT       Relative window                [default: 1h]
      --agg TEXT        COUNT|UCOUNT|AVG|MIN|MAX|SUM|STDDEV|VARIANCE|SAMPLE  [default: COUNT]
      --bin-ms INTEGER  Bin width in milliseconds      [default: 60000]
```

Returns JSON: `{aggregation, bin_width_ms, constraints, bins:[{timestamp_ms, value}], spikes:[{timestamp_ms, value, zscore}]}`.

## fields — discover queryable fields

```bash
vmware-log-insight fields [--name SUBSTR]
```

## alert — alert queries (read-only)

```bash
vmware-log-insight alert list [--name SUBSTR] [-n LIMIT]
vmware-log-insight alert get <alert_id>
vmware-log-insight alert history <alert_id> [-n LIMIT]
```

## doctor / mcp / version

```bash
vmware-log-insight doctor [--skip-auth]   # config, .env perms, network, auth, version, MCP import
vmware-log-insight mcp                     # start stdio MCP server (no network during startup)
vmware-log-insight version                 # installed skill version
```

## Query constraint grammar

Time and field filters are encoded as `/`-joined `field/OPERATOR/value` segments
on the API path (`GET /api/v2/events/{constraints}`):

- Time (relative): `timestamp/LAST/<ms>` — built from `--last`.
- Time (absolute): `timestamp/>/<begin_ms>` and `timestamp/</<end_ms>`.
- Text: `text/CONTAINS/<value>`.
- Operators: `CONTAINS`, `=`, `!=`, `<`, `>`, `EXISTS`, `LAST`.

Values are URL-encoded automatically. If no time window is given, the query
defaults to the last hour (never unbounded).

> The exact wire grammar is confirmed against the published v1/v2 docs; a future
> real-appliance test may refine the separator. Only `constraints.py` would change.
