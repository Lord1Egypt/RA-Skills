# Configuration

Create a private JSON file from the example. Replace every placeholder before use. The executor requires `--config` explicitly and refuses an empty repository list.

Required top-level fields:
- `repositories`: array of approved entries with unique, non-sensitive `id` and absolute `path`.
- `state_dir`: private directory for `latest.json`; use a dedicated directory outside Git and indexed memory.
- `lock`: absolute dedicated run-marker path. Existing markers block the run and are never removed automatically.

Optional:
- `budget_seconds` (480), `command_timeout_seconds` (15).
- `discovery_root`: explicitly approved absolute discovery root. Omit to disable discovery.
- `discovery_depth` (4): bounded walk depth. Client/data/cache/release directories are excluded heuristically; choose the root carefully.

Repository fields:
- `remote` (origin), `base` (origin/main).
- `github`: owner/repository identifier, needed only for `--github`.
- `runtime`: absolute runtime working directory.
- `service`: optional systemd service name; enabling it requires all database fields below.
- `database_env_key`: exact non-secret environment key containing the database directory.
- `database_filename`: filename joined to that directory.
- `database_default`: verified absolute application default when the process does not define the directory key. Verify this against the application; the auditor cannot infer it.
- `deploy_lock` (.deploy.lock): relative deployment lock filename.

Protect the configuration and parent state directory with private permissions. Never put credentials in this file. Authentication belongs to the installed CLI or protected credential infrastructure.

Run without network or persistence for an initial check:
```bash
python3 scripts/audit.py --config /absolute/path/to/private-config.json --pretty
```
Network checks intentionally remain unknown in that run. Add `--fetch --github --persist --report` for the approved operational workflow.
