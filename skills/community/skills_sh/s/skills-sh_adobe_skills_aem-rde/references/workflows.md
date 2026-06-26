# Common workflows

End-to-end recipes for the things people actually do with `aio aem rde`.

## First-time setup on a new machine

```bash
# 1. Install the AIO CLI
npm install -g @adobe/aio-cli

# 2. Add the RDE plugin
aio plugins:install @adobe/aio-cli-plugin-aem-rde

# 3. Authenticate
aio login

# 4. Pick org / program / RDE
aio aem rde setup
# When asked "Do you want to store … locally?" answer Yes if you'll
# work with multiple RDEs from different directories.

# 5. Verify
aio aem rde setup --show
aio aem rde status
```

If `setup` doesn't list your program, the IMS user lacks Cloud Manager Developer/Deployment-Manager role for it, or there are no RDE-typed environments in that program.

## Pin a project to its own RDE

```bash
cd ~/Dev/customer-x
aio aem rde setup     # answer "yes" to local storage
# … this writes a .aio file in the cwd
```

From now on any `aio aem rde …` run from this directory targets that RDE without affecting other projects.

To verify which RDE you're on:

```bash
aio aem rde setup --show
```

## Deploy an OSGi bundle

```bash
# Maven build first
mvn -pl core -am clean install

# Hot-deploy
aio aem rde install core/target/com.example.foo-1.0.0-SNAPSHOT.jar

# Confirm
aio aem rde status                  # bundle should appear in the list
aio aem rde inspect osgi-bundles    # if inspect topic is enabled
```

If the bundle ends up in `Resolved` instead of `Active`:

```bash
aio aem rde inspect osgi-components -s author    # which DS components didn't satisfy?
aio aem rde logs -e "" -w "" -d com.example      # tail errors+warnings, plus debug for your package
```

## Deploy a content package

```bash
aio aem rde install ui.content/target/customer-x-content-1.0.0-SNAPSHOT.zip
```

For author-only:

```bash
aio aem rde install --target author ui.content/target/customer-x-content-1.0.0-SNAPSHOT.zip
```

## Deploy a single content file

```bash
# Path is auto-derived because the source lives under jcr_root/
aio aem rde install ui.apps/src/main/content/jcr_root/apps/customer-x/components/foo/foo.js

# Or explicit
aio aem rde install --type content-file --path /apps/customer-x/components/foo/foo.js path/to/foo.js
```

## Deploy a dispatcher config

```bash
# From a built dispatcher dir (containing conf.dispatcher.d/)
aio aem rde install dispatcher/src

# Or from a zipped dispatcher
aio aem rde install dispatcher/target/dispatcher.zip
```

## Deploy a frontend module

```bash
# After running the frontend build that produces dist/
aio aem rde install ui.frontend/build
```

The plugin will zip and upload. If the source dir doesn't have a `dist/` and `package.json`, it will refuse to guess `frontend` — pass `--type frontend` if needed.

## Tail logs while iterating

```bash
# All errors + warnings on author
aio aem rde logs -e "" -w ""

# Debug your package, info everywhere else, on publish
aio aem rde logs --target publish -d com.example -i ""

# Highlight slow lines and your service name
aio aem rde logs -e "" -H "took" -H "MyService"

# Pick from existing log configs (if a teammate set one up)
aio aem rde logs --choose
```

Stop with Ctrl-C. The plugin removes the server-side log config on exit.

## Triage a failed deploy

```bash
# 1. What's the env state?
aio aem rde status

# 2. What's the last update look like?
aio aem rde history
# -> note the id of the failing one, e.g. 42

# 3. Per-instance details
aio aem rde history 42

# 4. Logs around the time of failure
aio aem rde logs -e "" -w ""

# 5. (If inspect topic enabled) is the offending bundle / component / config
#    actually present and active?
aio aem rde inspect osgi-bundles -s author com.example.foo
aio aem rde inspect osgi-components -s author
aio aem rde inspect osgi-configurations -s author com.example.MyConfig
```

When everything looks confused and you suspect leftover state, consider `reset`.

## Reset vs. restart vs. snapshot-restore

| Need | Command | Time |
|------|---------|------|
| Get a stuck JVM unstuck without losing artifacts | `aio aem rde restart` | ~3 min |
| Wipe artifacts but keep authored content | `aio aem rde reset --keep-mutable-content` | ~10-20 min |
| Wipe artifacts and content (start clean) | `aio aem rde reset` | ~10-20 min |
| Recover a known-good state | `aio aem rde snapshot restore <name>` | ~10-20 min |
| Same, but keep current code, only roll back content | `aio aem rde snapshot restore <name> --only-mutable-content` | ~5-10 min |

`reset --force` skips the cached base repo — slower but recovers from broken-base scenarios. Always confirm with the user before running any reset.

## Snapshot lifecycle

```bash
# Create a save point before risky changes
aio aem rde snapshot create pre-migration -d "before SCR-1234 migration"

# List
aio aem rde snapshot

# Roll back
aio aem rde snapshot restore pre-migration

# Tidy up
aio aem rde snapshot delete pre-migration         # 7-day soft delete
aio aem rde snapshot delete pre-migration -f      # immediate (only if already in 'removed' state)
aio aem rde snapshot delete --all                 # nuke them all (confirm first!)

# Oh wait, I need that one back
aio aem rde snapshot undelete pre-migration
```

Snapshot create takes 3-8 minutes (lock + persist + unlock); restore takes 10-20 (full restart). Always tell the user the expected wait time so they don't kill the process.

## Switching between RDEs mid-task

```bash
# Inspect current pinning
aio aem rde setup --show

# Re-run the picker — preserves current org but lets you pick a new program/env
aio aem rde setup
```

If you actually want a different IMS org:

```bash
aio logout
aio login    # browser flow against the new org
aio aem rde setup
```

## Scripted CI deploy

```bash
#!/usr/bin/env bash
set -euo pipefail

# Authenticate via JWT (set up once)
# aio config:set ims.contexts.aem-rde-ci '{ "client_id": "...", "..."}'
# aio auth:login --ctx aem-rde-ci  (or use AIO env vars)

aio config:set -l cloudmanager_orgid "$ORG_ID"
aio config:set -l cloudmanager_programid "$PROGRAM_ID"
aio config:set -l cloudmanager_environmentid "$ENV_ID"

aio aem rde install core/target/customer-x.core-${VERSION}.jar --quiet --json
aio aem rde install ui.content/target/customer-x.ui.content-${VERSION}.zip --quiet --json
aio aem rde install ui.frontend/build --type frontend --quiet --json

aio aem rde status --json
```

Don't restart, don't reset, don't snapshot from a generic CI job — those are interactive/slow. Reserve them for explicit pipelines.

## Toggling experimental features

```bash
# Locally (this project only)
aio config set -l -j aem-rde.experimental-features '["aem:rde:inspect","aem:rde:snapshot"]'

# Remove
aio config:delete -l aem-rde.experimental-features

# Confirm
aio aem rde inspect --help
aio aem rde snapshot --help
```
