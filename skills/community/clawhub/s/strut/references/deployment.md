# Deployment

Procedures for deploying strut services to a VPS.

## Quick Deploy

```bash
strut my-stack deploy --env prod --dry-run   # Preview
strut my-stack deploy --env prod             # Deploy
```

`deploy` targets whatever host the stack maps to. For a VPS-mapped stack it runs the full pipeline on that host over SSH: updates the repo → runs migrations → deploys → verifies health → rolls back if unhealthy. For a stack with no VPS it deploys against local Docker. `--local` forces local; `--require-remote` refuses to fall back to it. `release` is an alias for `deploy --require-remote`.

## Manual Deploy Steps

```bash
strut my-stack update --env prod              # Sync strut repo on VPS
strut my-stack deploy --env prod              # Deploy containers
strut my-stack health --env prod --json       # Verify
```

## Stop Containers

Stopping a production stack takes it offline. `--volumes` also deletes the stack's Docker volumes, which holds database data, so use it only after a verified backup and the user's approval. Run `--dry-run` first and confirm with the user before stopping `--env prod`.

```bash
strut my-stack stop --env prod --dry-run      # Preview
strut my-stack stop --env prod                # Stop containers
strut my-stack stop --env prod --volumes      # Stop + remove volumes (deletes data)
```

## Service Profiles

```bash
strut my-stack deploy --env prod                          # core (default)
strut my-stack deploy --env prod --services messaging     # + messaging
strut my-stack deploy --env prod --services full          # everything
```

## Deploy Modes

```bash
strut my-stack deploy --env prod --standard     # in-place (default)
strut my-stack deploy --env prod --blue-green    # stand up green, health-gate, swap, drain blue
```

## First-Time Setup

1. Create an env file from the template, fill in secrets (`VPS_HOST`, registry creds, DB passwords).
2. Configure `strut.conf` with registry type and org.
3. Deploy: `strut my-stack deploy --env prod`.

## Migrations

```bash
strut my-stack migrate postgres --status --env prod   # Check
strut my-stack migrate postgres --up --env prod       # Apply
strut my-stack migrate neo4j --down 1 --env prod      # Rollback one (can discard data)
```

`--down` can remove schema objects and the data in them. Back up that database first (`strut my-stack backup neo4j --env prod`) and get the user's approval before running it on production.

## Rollback

```bash
strut my-stack rollback --env prod            # Restore previous deploy snapshot
```

A rollback restarts services on the previous snapshot, so expect a brief interruption. Confirm with the user before running it on production. It is separate from database migrations: if the schema also has to change back, that is a `migrate --down` with the backup and approval described above.

## Ship and Rebuild

```bash
strut my-stack ship --env prod                       # commit, push, then rebuild on the remote host
strut my-stack rebuild --env prod                     # build images on target + redeploy (BUILD_MODE=local)
strut my-stack rebuild --env prod --no-cache          # rebuild without the Docker layer cache
```

`ship` is the "edit locally, deploy remotely" workflow: it commits, pushes, then SSHes over and runs `rebuild` on the target host. `rebuild` always builds natively on whichever host runs it — pointing `ship`/`rebuild` at a Raspberry Pi builds arm64 images directly on that Pi, with no cross-compilation involved.

### Multi-arch / ARM builds

Set `PLATFORMS` in `services.conf` (or pass `--platform` to `rebuild`/`ship` for a one-off) to build for architectures other than the host's, via `docker buildx`:

```bash
strut my-stack rebuild --env prod --platform linux/arm64,linux/amd64   # multi-arch manifest
strut my-stack rebuild --env prod --platform linux/arm64               # single cross-arch build
```

- **Unset `PLATFORMS`** (the default): plain `docker compose build`, no buildx dependency — safe for older Docker installs on some Pi images.
- **Single platform matching the host's own arch**: same plain `docker compose build` path.
- **Single platform different from the host's arch**: builds via `docker buildx bake --load` (loads the cross-arch image into the local Docker image store).
- **More than one platform**: builds via `docker buildx bake --push`. buildx cannot load a multi-arch manifest into the local image store, so this *requires* `REGISTRY_TYPE`/`REGISTRY_HOST` to already be configured — it pushes the manifest to that registry instead of running locally.

Before a `PLATFORMS` build runs, strut warns (but doesn't block) if the target host's architecture isn't among the platforms being built — resolved from `arch=<value>` on the host's entry in `strut.conf`'s `[hosts]` section, or a best-effort `uname -m` probe over SSH:

```ini
[hosts]
pi-ops = pi@pi-ops.local:22 <path-to-ssh-key> arch=arm64
```

## Deploy History / Releases

Every deploy and release appends a durable, structured record (timestamp,
git SHA, deploy mode, env, outcome, and — for `release` — the actor who
triggered it) to `stacks/<stack>/.deploy-history.jsonl`, alongside the
existing rollback snapshot in `stacks/<stack>/.rollback/`.

```bash
strut my-stack releases --env prod                     # List past deploys/releases, newest first
strut my-stack releases --env prod --json --limit 20    # For CI/automation
strut my-stack releases show HEAD --env prod            # Full detail for the latest release
strut my-stack releases show 20260420-091500 --env prod # Full detail for a specific release
```

`releases show <id>` accepts the same refs as `rollback diff`: a release ID
(the rollback snapshot basename), `HEAD` (latest), or `HEAD~N` (Nth older) —
release IDs and rollback snapshot IDs share the same ID space, so:

```bash
strut my-stack releases --env prod                      # Find the release you're investigating
strut my-stack rollback diff HEAD~1 HEAD --env prod      # Compare it against the one before
```

Note: a release's `release_id` is the snapshot captured *before* that
release ran — i.e. what `rollback` (which always restores the latest
snapshot) would put back if run right after that release, not a snapshot
of what that release itself deployed. For the same reason, `releases show`
labels its per-service image list "Rollback-to images (pre-release state)"
(`rollback_images` in `--json` output) rather than "Images" — they're the
tags that release would revert to, not the tags it shipped.

## Local vs VPS Semantics

- `deploy` / `stop` — target the host the stack maps to; local Docker when it maps to none
- `release` — alias for `deploy --require-remote`
- `update` — syncs the strut repo on the VPS (no container restart)
- `shell` / `exec` — SSH to the VPS

## Best Practices

1. Always `--dry-run` first for destructive commands.
2. Back up before major changes: `strut my-stack backup all --env prod`.
3. Use `--no-sync` when changing config rather than code — it skips the git sync and just restarts. Use `--require-remote` in CI so an unresolved host fails instead of deploying to the runner.
4. Keep `services.conf` health checks current — they gate deploy success.
