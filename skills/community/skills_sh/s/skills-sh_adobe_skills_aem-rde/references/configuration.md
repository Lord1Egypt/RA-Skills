# Configuration & multi-environment patterns

## The three Cloud Manager IDs

Every RDE command reads three keys from `aio` config:

| Key | What it identifies |
|-----|--------------------|
| `cloudmanager_orgid` | IMS organization (`<id>@AdobeOrg`) |
| `cloudmanager_programid` | Cloud Manager program |
| `cloudmanager_environmentid` | The actual RDE environment within the program |

Two helper keys are also written by `setup` and used in human-readable output:

| Key | Purpose |
|-----|---------|
| `cloudmanager_programname` | Program display name |
| `cloudmanager_environmentname` | Environment display name |

Plus one notification toggle:

| Key | Purpose |
|-----|---------|
| `rde_enableNotifications` | When `true`, long-running tasks emit desktop notifications. |

## Storage hierarchy

`aio-lib-core-config` (used by all `aio config:*` commands) reads in priority order:

1. **Environment variables** — `AIO_<KEY>` overrides everything (e.g. `AIO_CLOUDMANAGER_ORGID`). Useful for one-off CI overrides.
2. **Local file** — `.aio` in the current working directory or any ancestor. **Strongly recommended** when you have more than one RDE.
3. **Global file** — `~/.config/aio/config.json` (or platform equivalent). Used when there's no local config.

Use `-l, --local` with `aio config:set` / `aio config:delete` to write to the local `.aio` file. Without that flag the command writes globally.

```bash
# Pin this repo to a specific RDE
aio config:set -l cloudmanager_orgid 1234@AdobeOrg
aio config:set -l cloudmanager_programid 12345
aio config:set -l cloudmanager_environmentid 67890
```

`aio aem rde setup` always asks "Do you want to store the information you enter in this setup procedure locally?" — answering yes writes to `.aio`.

## Working with multiple RDEs

> **Single-user constraint:** Per Adobe's official AEM documentation, ideally only one developer should use a given RDE at a time. Concurrent deployments from multiple developers race against each other and produce confusing state. For team workflows, give each developer their own RDE rather than sharing.

The clean pattern is **one `.aio` file per project**:

```
~/Dev/
├── customer-a/
│   ├── .aio          # pins to customer A's RDE
│   └── …
└── customer-b/
    ├── .aio          # pins to customer B's RDE
    └── …
```

When running RDE commands, `cd` into the right project — config resolution starts from your CWD, walking upward.

If you actually want one RDE for everything, use the global config (no `-l`). The setup wizard guards against confusion: when the last RDE command was more than 24h ago, it asks "Do you want to continue running the command on `cm-pXXXX-eYYYY`?" before proceeding.

## Switching IMS organizations

The token cached by `aio login` is org-bound. To move between orgs:

```bash
aio logout
aio login
aio aem rde setup
```

There's no shortcut — `setup` only enumerates organizations the current token is valid for.

## Experimental feature flags

`inspect` and `snapshot` topics ship in the plugin but stay hidden until enabled via `aem-rde.experimental-features`. The init hook (`src/lib/hooks/experimental-features-init-hook.js`) reads this list and registers/unregisters those topics at oclif boot time.

Enable per-project:

```bash
# inspect only
aio config set -l -j aem-rde.experimental-features '["aem:rde:inspect"]'

# both inspect and snapshot
aio config set -l -j aem-rde.experimental-features '["aem:rde:inspect","aem:rde:snapshot"]'
```

Note `-j` for JSON parsing of the array.

To disable: overwrite with `'[]'` or delete the key (`aio config:delete aem-rde.experimental-features`).

## Notifications

Desktop notifications via `node-notifier` fire for slow operations (snapshot create/restore, env reset, status `--wait`). Toggle with:

```bash
aio aem rde setup --enable-notifications
aio aem rde setup --disable-notifications
```

These write to global aio config, not local — they're a per-user preference.

## Inspect the active config

`aio aem rde setup --show` prints something like:

```
Current configuration: cm-p12345-e67890: My Program - dev-rde-01 (organization: 1234@AdobeOrg)
```

`aio config:get cloudmanager_orgid` (etc.) reads individual keys; `aio config:list` dumps everything resolved (local merged over global).

## CI / build environments

For non-interactive use (build pipelines, GitHub Actions, etc.):

1. Authenticate via JWT or OAuth Server-to-Server credentials, **not** the interactive `aio login`. Configure an IMS context with a service-account credential and set `AIO_RUNTIME_AUTH` / `aio config set ims.contexts.<name>.…` accordingly.
2. Set the three Cloud Manager IDs:
   ```bash
   aio config:set -l cloudmanager_orgid "$ORG_ID"
   aio config:set -l cloudmanager_programid "$PROGRAM_ID"
   aio config:set -l cloudmanager_environmentid "$ENV_ID"
   ```
3. Always pass `--quiet --json` to RDE commands so output is parseable and prompts are skipped.
4. Avoid `setup` (it's interactive) and `logs` / inspect's `request-logs:enable` / `request-logs:disable` (they intentionally don't support `--json`).
5. Honour the exit codes: `1`/`5` retryable, `2`/`3` config/validation (don't retry), `4`/`40` deployment (depends on the step).

## Where the config actually lives

If something looks "stuck" on the wrong env, check:

```bash
# Which file is currently winning?
aio config:list

# Local file, if any:
cat .aio          # Project-pinned
cat ~/.config/aio/config.json   # Global (path varies by OS)

# Drop a stale local config:
aio config:delete -l cloudmanager_orgid
aio config:delete -l cloudmanager_programid
aio config:delete -l cloudmanager_environmentid
```

The `.aio` file is JSON-ish (YAML-compatible). Editing it by hand is fine for emergencies.
