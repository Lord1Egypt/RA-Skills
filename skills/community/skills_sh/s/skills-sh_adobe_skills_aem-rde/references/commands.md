# `aio aem rde` — Per-command reference

All commands inherit `--organizationId`, `--programId`, `--environmentId`, `--quiet`, and (where applicable) `--json` unless noted. Both `aio aem rde <cmd>` and `aio aem:rde:<cmd>` notations work.

## Stable commands

### `aio aem rde setup`

Interactive setup for the three Cloud Manager IDs (org / program / environment). `enableJsonFlag: false` — does not produce JSON output. Always picks `rde`-typed environments only (filters others out). Asks if you want to store config locally (`.aio` file in current dir) or globally.

| Flag | Description |
|------|-------------|
| `-s, --show` | Print current config and exit (no prompts). |
| `-e, --enable-notifications` | Turn on desktop notifications for long tasks (snapshot, reset). Stored in global aio config. |
| `-d, --disable-notifications` | Turn them off. |

Internals:
- Lists IMS organizations via `Ims.fromToken`. Single org auto-selected.
- Lists programs and environments via Cloud Manager SDK; uses `inquirer-autocomplete-prompt` so the user can type to filter.
- Persists `cloudmanager_orgid`, `cloudmanager_programid`, `cloudmanager_environmentid`, plus name fields `cloudmanager_programname` / `cloudmanager_environmentname`.

### `aio aem rde status`

Shows env state + a grouped listing of deployed artifacts.

| Flag | Description |
|------|-------------|
| `--wait` | Block until env reports `Ready`, polling every 10s. Notifies on completion if notifications are enabled. |

Output sections (each printed for both author and publish):
- Bundles — `<bundleSymbolicName>-<bundleVersion>`
- Configurations — `<configPid>`
- (others depending on what's deployed)

Throws `UNEXPECTED_API_ERROR` if status payload includes an error.

### `aio aem rde install <location>`

The deployment workhorse. Accepts a local path or a public URL (http/https) — automatically distinguishes:
- Bare paths and `file://…` are treated as local files.
- `http(s)://…` does a HEAD request to follow redirects and learn content-length.

Argument:

| Arg | Required | Description |
|-----|----------|-------------|
| `location` | yes | URL or filesystem path to the artifact (or directory for `frontend`/`dispatcher-config`/`env-config`). |

Flags:

| Flag | Description |
|------|-------------|
| `-t, --type` | One of `osgi-bundle`, `osgi-config`, `content-package`, `content-file`, `content-xml`, `dispatcher-config`, `frontend`, `env-config`. Auto-guessed if omitted. |
| `-p, --path` | JCR repository path. Required for `content-file` and `content-xml` (auto-guessed if source path is under `…/jcr_root/…`). |
| `-s, --target` | `author` or `publish`. Defaults to **both** when omitted (delivery to one, then the other). |
| `-f, --force` | Force install — used when env is stuck on a previous upload. |
| `-r, --restart` | Run `aio aem rde restart` after a successful deploy. Adds 2-5 minutes; rarely needed. |
| `-q, --quiet` | Suppress progress bar / spinner output. |

Type guessing rules (when `--type` omitted):

| Source | Guessed |
|--------|---------|
| `*.jar` | `osgi-bundle` |
| `*.json` | `osgi-config` |
| Local zip with `jcr_root/` entry | `content-package` |
| Local zip with `conf.dispatcher.d/` entry | `dispatcher-config` |
| Local zip with `dist/` and `package.json` | `frontend` |
| Local zip with any `*.yaml` | `env-config` |
| Remote zip | one of `[content-package, dispatcher-config, frontend]` (will fail if ambiguous — pass `--type`) |
| `*.xml` with `--path` | `content-xml` |
| Other extension with `--path` | `content-file` |

Directory inputs only work for `frontend`, `dispatcher-config`, and `env-config` — the plugin builds the zip via `frontendInputBuild` / `dispatcherInputBuild` / `configInputBuild`. A directory + any other type is rejected.

After upload the plugin tracks the deployment via `loadUpdateHistory`, polling per-instance progress and writing them into the JSON result's `items` array. On failure throws `INTERNAL_INSTALL_ERROR` (exit 4 territory).

### `aio aem rde delete <id>`

Removes one or more bundles/configs by id.

| Arg | Required | Description |
|-----|----------|-------------|
| `id` | yes | Bundle Symbolic Name (`com.example.foo`), BSN-version (`com.example.foo-1.0.0`), or OSGi config PID. |

| Flag | Description |
|------|-------------|
| `-t, --type` | Restrict to `osgi-bundle` or `osgi-config`. Both checked if omitted. |
| `-s, --target` | Restrict to one instance (default: both). |
| `-f, --force` | Force the deletion. |
| `-q, --quiet` | Quiet mode. |

Behaviour: lists current artifacts via `loadAllArtifacts`, filters by id, deletes each match, then writes the per-update history into result. If no artifact matches, throws `DELETE_NOT_FOUND` with helpful context (which type, which target).

### `aio aem rde history [id]`

Without an id: lists all updates done to the env (status + summary).

With an id: pulls the full per-instance install/delete progress for that update — same data shown live during `install`/`delete`. Validates the id is a non-negative integer (`INVALID_UPDATE_ID` otherwise).

### `aio aem rde logs`

Continuous log tail. Creates an AEM log configuration on the server, polls every 500 ms, prints colorized log lines until SIGINT. `enableJsonFlag: false`.

| Flag | Description |
|------|-------------|
| `-f, --format` | Logback format string. Default: `%d{dd.MM.yyyy HH:mm:ss.SSS} *%level* [%thread] %logger %msg%n` |
| `-t, --trace <logger>` | Add logger at TRACE level. Repeatable. |
| `-d, --debug <logger>` | Add logger at DEBUG level. Repeatable. |
| `-i, --info <logger>` | Add logger at INFO level. Repeatable. Default `-i ""` if no level flags given. |
| `-w, --warn <logger>` | Add logger at WARN level. Repeatable. |
| `-e, --error <logger>` | Add logger at ERROR level. Repeatable. |
| `--color / --no-color` | Colorize output by level (TRACE gray, DEBUG cyan, INFO green, WARN yellow, ERROR red). |
| `--choose` | Interactive picker over existing log configurations. |
| `-H, --highlight <substr>` | Print matching lines in white. Repeatable. |
| `-s, --target` | `author` (default) or `publish`. |

Behavior notes:
- AEM permits a small number of concurrent log configs per env; on `405` the plugin prompts to remove an existing one.
- A small per-line delay (≈ `500ms / linecount`) makes the tail feel fluid.
- SIGINT/SIGTERM both stop and clean up the server-side log config.
- 404 means the configuration was removed remotely (e.g. by another user creating a new one) — the plugin stops gracefully.

### `aio aem rde restart`

Restarts both author and publish. No flags beyond the common ones. Triggers a "restarted" desktop notification if enabled.

### `aio aem rde reset`

Long-running env reset.

| Flag | Description |
|------|-------------|
| `--keep-mutable-content` | Reset code/config but preserve content. |
| `-f, --force` | Don't reuse a cached base repo — slower but recovers from broken state. |
| `--wait / --no-wait` | Default `--wait`. Without it, the API call returns once the reset is queued. |

Reset is destructive: it wipes all deployed artifacts. Always confirm with the user before running.

## Experimental commands — `aem:rde:inspect:*`

Enable with:
```bash
aio config set -l -j aem-rde.experimental-features '["aem:rde:inspect"]'
```

All inspect subcommands accept `--target` (defaults to `author`) and `--include` for a substring filter on the listing.

### `aio aem rde inspect inventory [id]`

Lists framework inventory items (table with `format` and `id` columns). With an id, fetches one item.

### `aio aem rde inspect osgi-bundles [id]`

OSGi bundle listing on the chosen target. With an id (BSN), prints the full bundle details.

### `aio aem rde inspect osgi-components [name]`

OSGi DS components.

### `aio aem rde inspect osgi-configurations [pid]`

OSGi configurations as managed by Configuration Admin.

### `aio aem rde inspect osgi-services [id]`

Registered OSGi services (numeric service id).

### `aio aem rde inspect request-logs [id]`

Lists request log entries on the chosen target. With an id, fetches one entry. Request logging must be enabled first.

### `aio aem rde inspect request-logs enable`

Turns on request logging (`enableJsonFlag: false`). Pass logger config like the `logs` command (`-i`, `-d`, etc.) and an optional `-f` format.

### `aio aem rde inspect request-logs disable`

Turns it off. `enableJsonFlag: false`.

## Experimental commands — `aem:rde:snapshot:*`

Enable with:
```bash
aio config set -l -j aem-rde.experimental-features '["aem:rde:snapshot"]'
```

Snapshot APIs additionally require the customer to be enrolled in the snapshot EAP — the API returns `451` (`NON_EAP`) otherwise.

### `aio aem rde snapshot`

List snapshots in a table sorted by `Last Used` (descending by default). Columns: name, description, usage, size, state, created, lastUsed.

| Flag | Description |
|------|-------------|
| `-s, --sort` | Sort key; prefix `-` for reverse. Default `-Last Used`. |

### `aio aem rde snapshot create <name> [-d <description>]`

Locks the RDE while a content+deployment snapshot is taken, then unlocks.

| Arg | Description |
|-----|-------------|
| `name` | Required. Must be unique within the env. |

| Flag | Description |
|------|-------------|
| `-d, --description` | Free-text description shown in `snapshot` listing. |

Phases (with progress spinners):
1. **Requesting** — submit job (<1m).
2. **Waiting for backend** — backend picks up the action.
3. **Locking & creating** — RDE is locked, snapshot taken (2-5m).
4. **Unlocking** — RDE returns to `Ready` (1-2m).

If the progress percentage doesn't advance for 15 minutes the plugin throws `SNAPSHOT_CREATION_STUCK`. Other failures: `ALREADY_EXISTS` (409), `INVALID_STATE` (503), `SNAPSHOT_LIMIT` (507).

### `aio aem rde snapshot restore <name>`

Replaces RDE state with the snapshot. Restarts the env after restore.

| Arg | Description |
|-----|-------------|
| `name` | Required. |

| Flag | Description |
|------|-------------|
| `--only-mutable-content` | Only restore mutable content (no deployment rollback). Faster, no restart. |

Phases: requesting → backend pickup → restoring (2-5m) → restart (5-10m). Errors include `SNAPSHOT_NOT_FOUND` (404 with that detail), `SNAPSHOT_DELETED` (404 with deleted detail), `INVALID_STATE` (406), `DEPLOYMENT_IN_PROGRESS` (503).

### `aio aem rde snapshot delete <name>`

Marks a snapshot for deletion (7-day retention by default). With `--all`, deletes every snapshot in the env (concurrently). With `-f, --force`, wipes immediately rather than soft-deleting.

| Arg | Description |
|-----|-------------|
| `name` | Required unless `--all` is set. |

| Flag | Description |
|------|-------------|
| `-a, --all` | Mark every snapshot for deletion. |
| `-f, --force` | Force-delete (no retention period). Snapshot must already be in `removed` state — otherwise throws `SNAPSHOT_WRONG_STATE`. |

### `aio aem rde snapshot undelete <name>`

Cancels a pending deletion. Errors: `SNAPSHOT_NOT_FOUND` (404 with that detail), `SNAPSHOT_LIMIT` (507) if undeleting would push you past the snapshot quota.
