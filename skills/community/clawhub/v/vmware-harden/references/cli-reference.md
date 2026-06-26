# CLI Reference

Full command reference for `vmware-harden`. Source of truth: `vmware_harden/cli/`.

The CLI is a Typer app with seven top-level command groups: `scan`, `report`,
`baseline`, `drift`, `advise`, `web`, `doctor`. Run `vmware-harden --help`
for the auto-generated overview.

## scan

Run a compliance scan against a target. The scan loads the baseline,
collects evidence via the upstream `vmware-aiops` collectors, evaluates
rules, persists the snapshot to the Twin DuckDB, and computes drift versus
the previous snapshot for the same target.

### Synopsis

```bash
vmware-harden scan --target <name> [--baseline <id>] [--db <path>]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--target` | vCenter target name from upstream `vmware-aiops` config. | (required) |
| `--baseline` | Built-in or imported baseline id. | `cis-vmware-esxi-8.0-subset` |
| `--db` | Twin DuckDB path. | `~/.vmware-harden/twin.duckdb` |

### Examples

```bash
# Default CIS subset
vmware-harden scan --target lab-vc01

# 等保 2.0 三级 against production
vmware-harden scan --target prod-vc --baseline dengbao-2.0-level3-vmware

# Custom DB path (e.g. CI artifact)
vmware-harden scan --target lab-vc01 --db /tmp/ci-twin.duckdb
```

The scan prints one line per collector with the count of entities
gathered, then the total violation count. Drift events versus the prior
snapshot are persisted automatically when a previous snapshot exists for
the same `--target`.

## report

Show the most recent snapshot's violations.

### Synopsis

```bash
vmware-harden report [--db <path>] [--format text|json]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--db` | Twin DuckDB path. | `~/.vmware-harden/twin.duckdb` |
| `--format` | Output format — `text` or `json`. | `text` |

> HTML rendering is **not** a CLI flag; use `vmware-harden web` for the
> rendered dashboard.

### Examples

```bash
vmware-harden report
vmware-harden report --format json > violations.json
```

If no scans have run yet, the command prints a hint to run
`vmware-harden scan` first and exits 0.

## baseline

Manage compliance baselines. Built-ins ship inside the package; user
imports live under `~/.vmware-harden/baselines/`.

### baseline list

```bash
vmware-harden baseline list
```

Prints one baseline id per line (built-ins + imports). No options.

### baseline validate

Validate a YAML file against the baseline schema **without** importing.

```bash
vmware-harden baseline validate <path>
```

| Argument | Description |
|----------|-------------|
| `path` | YAML file to validate. |

Exit codes: `0` ok, `1` validation error, `2` file not found.

### baseline import

Validate, then copy a YAML file into `~/.vmware-harden/baselines/`.
Invalid files are never persisted.

```bash
vmware-harden baseline import <path> [--name <stem>]
```

| Flag | Description | Default |
|------|-------------|---------|
| `path` | YAML file to import. | (required, positional) |
| `--name` | Override destination filename stem. | source filename stem |

### Examples

```bash
vmware-harden baseline list
vmware-harden baseline validate ./my-corp.yaml
vmware-harden baseline import ./my-corp.yaml --name corp-prod
```

## drift

Show drift events from the most recent snapshot relative to its prior
snapshot for the same target. (Drift is computed and persisted by `scan`;
this command only renders.)

### Synopsis

```bash
vmware-harden drift [--db <path>] [--format text|json]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--db` | Twin DuckDB path. | `~/.vmware-harden/twin.duckdb` |
| `--format` | `text` or `json`. | `text` |

### Examples

```bash
vmware-harden drift
vmware-harden drift --format json | jq '.[] | select(.field == "ntp.servers")'
```

If no scans exist, the command prints a hint and exits 0. If no drift was
detected versus the prior snapshot, it prints
`No drift detected since previous snapshot.`

## advise

Generate LLM-driven remediation suggestions for one or all critical
violations of the latest snapshot. Persists each suggestion to the Twin
so `report` / `get_remediation` can return it later.

### Synopsis

```bash
vmware-harden advise (--violation-id <id> | --all-critical) [--db <path>]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--violation-id` | Single violation id to advise on. | — |
| `--all-critical` | Advise on every `severity=critical` violation in the latest snapshot. | `false` |
| `--db` | Twin DuckDB path. | `~/.vmware-harden/twin.duckdb` |

You must pass exactly one of `--violation-id` or `--all-critical`; otherwise
the command exits 2.

### LLM provider selection

| Condition | Provider |
|-----------|----------|
| `ANTHROPIC_API_KEY` is set | `AnthropicProvider` (real LLM) |
| `ANTHROPIC_API_KEY` is unset | `MockProvider` with a deterministic canned response, plus a stderr warning |

### Examples

```bash
export ANTHROPIC_API_KEY=sk-ant-...
vmware-harden advise --violation-id v-cis-1.1.1-host-esxi-01

# Bulk advise everything critical
vmware-harden advise --all-critical
```

## web

Serve the FastAPI + Jinja2 read-only dashboard via uvicorn.

### Synopsis

```bash
vmware-harden web [--db <path>] [--host <addr>] [--port <int>]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--db` | Twin DuckDB path. | `~/.vmware-harden/twin.duckdb` |
| `--host` | Bind address. | `127.0.0.1` |
| `--port` | Bind port. | `8080` |

### Examples

```bash
vmware-harden web                       # http://127.0.0.1:8080/
vmware-harden web --host 0.0.0.0 --port 9000
```

Exits 1 with a message if the Twin DuckDB does not exist; run a scan
first.

## doctor

Run environment diagnostics. Added in v1.5.18 to give users (and CI) a
single command that confirms whether their install is wired up correctly
before they run a scan.

### Synopsis

```bash
vmware-harden doctor
```

### Options

None. The command takes no flags or arguments.

### What it checks

Source of truth: `vmware_harden/doctor.py::run_diagnostics`.

| Check | Severity on failure | What it means |
|-------|--------------------:|---------------|
| Python version | error | Python `>= 3.10` required. |
| Twin DB | warn | `~/.vmware-harden/twin.duckdb` exists; if missing, run a scan first. |
| Built-in baselines | error | At least 4 built-in baselines load successfully. |
| `vmware-aiops` | warn | Optional — host/VM collectors. |
| `vmware-storage` | warn | Optional — datastore collector. |
| `vmware-nsx-security` | warn | Optional — DFW collector. |
| `vmware-policy` | **error** | **Required** — provides the `@vmware_tool` audit decorator. |
| `ANTHROPIC_API_KEY` | warn | Unset → advisor falls back to `MockProvider`. |
| `vmware-pilot` | info | Optional — required only by `vmware-harden apply --pilot real`. |
| Audit DB dir | warn / error | `~/.vmware/audit.db` parent dir is writable. |

### Example output

```
  ✓ Python version                  Python 3.12.7
  ✓ Twin DB                         /Users/me/.vmware-harden/twin.duckdb
  ✓ Built-in baselines              6 loaded
  ✓ vmware-aiops                    vmware_aiops available
  ⚠ vmware-storage                  install: `uv tool install vmware-storage` (datastore collector)
  ⚠ vmware-nsx-security             install: `uv tool install vmware-nsx-security` (DFW collector)
  ✓ vmware-policy                   vmware_policy available
  ⚠ ANTHROPIC_API_KEY               unset — Advisor will use MockProvider
  i vmware-pilot                    optional — `vmware-harden apply --pilot real` requires it
  ✓ Audit DB dir                    /Users/me/.vmware

  All checks passed (3 warning(s))
```

### Exit codes

- `0` — no `error` results (warnings are non-fatal).
- `1` — at least one `error` result (e.g. Python `< 3.10`, missing
  `vmware-policy`, or audit dir not writable).

Use `doctor` as a non-zero gate in CI before running `scan` in pipelines.

## MCP server entry point

Registered as a separate console script:

```bash
vmware-harden-mcp        # FastMCP stdio server (used by MCP clients)
```

Configure your MCP client to spawn `vmware-harden-mcp` directly. See
`references/setup-guide.md` for full client configurations.
