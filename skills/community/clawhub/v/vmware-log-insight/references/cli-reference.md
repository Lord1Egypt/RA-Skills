# vmware-log-insight CLI Reference

All commands are read-only. Global options: `--target/-t <name>` (target from
config; default if omitted) and `--config/-c <path>` (override config file).

## search — search log events

```bash
vmware-log-insight search [OPTIONS]
  -q, --text TEXT       Word(s) to match (CONTAINS; whole words, `*` wildcard)
  -l, --last TEXT       Relative window: 1h, 30m, 7d   [default: 1h]
  -n, --limit INTEGER   Max events (1..200; larger is lowered, with a note)  [default: 50]
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
  -q, --text TEXT       Word(s) to match
  -l, --last TEXT       Relative window                [default: 1h]
      --agg TEXT        COUNT|SAMPLE, or UCOUNT|AVG|MIN|MAX|SUM|STDDEV|VARIANCE with --field  [default: COUNT]
  -f, --field TEXT      Field the function applies to (a name from `fields`)
      --bin-ms INTEGER  Bin width in milliseconds      [default: 60000]
```

Returns JSON: `{aggregation, field, bin_width_ms, constraints, bins:[{timestamp_ms, end_ms, value}], spikes:[{timestamp_ms, end_ms, value, zscore}]}`,
bins oldest first. The appliance omits bins with no events; for COUNT and UCOUNT they are
added back as 0 (`filled_empty_bins: true`), for the others they stay missing. For `SAMPLE`
each bin's value is one example event. COUNT and SAMPLE refuse `--field`; the other
seven require it (the appliance answers HTTP 400 otherwise). AVG/MIN/MAX/SUM/STDDEV/
VARIANCE need a NUMBER field, e.g. `--agg UCOUNT --field hostname`.

## fields — discover queryable fields

```bash
vmware-log-insight fields [--name SUBSTR]   # name + type (STRING, NUMBER, ...)
```

## alert — alert queries (read-only)

```bash
vmware-log-insight alert list [--name SUBSTR] [-n LIMIT]
vmware-log-insight alert get <alert_id>
vmware-log-insight alert history <alert_id> [-n LIMIT]
```

## doctor / mcp / version

```bash
vmware-log-insight doctor [--skip-auth]   # config, .env perms, network, auth, version, query API (/fields), MCP import
vmware-log-insight mcp                     # start stdio MCP server (no network during startup)
vmware-log-insight version                 # installed skill version
```

## Query constraint grammar

Time and field filters are encoded as `/`-joined `field/<OPERATOR value>` pairs
on the API path (`GET /api/v2/events/{constraints}`) — the operator and value
share one path segment, separated by an encoded space:

- Time (relative): `timestamp/LAST%20<ms>` — built from `--last`. The appliance
  reads LAST as a 32-bit millisecond count, so a window longer than ~24.8 days is
  sent as `timestamp/%3E%20<now - window>` instead (8.18.7 answers HTTP 400 to the
  LAST form there).
- Time (absolute): `timestamp/%3E%20<begin_ms>` and `timestamp/%3C%20<end_ms>`,
  epoch **milliseconds**; a value that looks like seconds, or begin after end, is
  refused before any call.
- Text: `text/CONTAINS%20<value>` — matches whole words, not substrings
  (`localhost` matches `localhost.localdomain`; `localdom` matches nothing;
  `localdom*` matches again — `*` is a wildcard). With no match, the result's
  `note` says this, because 0 events for part of a word is not "no such logs".
- Existence: `<field>/EXISTS` (no value).
- Operators: `CONTAINS`, `=`, `!=`, `<`, `>`, `EXISTS`, `LAST`.

Values are URL-encoded automatically. If no time window is given, the query
defaults to the last hour (never unbounded).

> The exact wire grammar is confirmed against the published v1/v2 docs; a future
> real-appliance test may refine the separator. Only `constraints.py` would change.
