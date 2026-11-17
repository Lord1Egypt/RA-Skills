# Releasing Onto a Box — and Undoing It

Getting a new version onto a machine that is already serving, without dropping requests and without a rebuild standing between you and a rollback. CI/CD pipeline design belongs to the `deploy` skill; this file is what happens on the target host.

**Before deploying**, read `## Services` in `~/Clawic/data/server/memory.md` (or `services.md` if `## Boxes` points there) for the supervisor and reload command in use, and the last rows of `deploys/<year>.md` for what is currently live and what the previous release directory is called. A rollback target you have to reconstruct is not a rollback target.

**Contents:** [The Release Directory](#the-release-directory) · [The Deploy Sequence](#the-deploy-sequence) · [Rollback](#rollback) · [Migrations Are the Hard Part](#migrations-are-the-hard-part) · [Configuration and Secrets](#configuration-and-secrets) · [Assets and Cache Busting](#assets-and-cache-busting) · [Health Gate](#health-gate) · [Blue-Green on One Machine](#blue-green-on-one-machine) · [Deploying Containers](#deploying-containers) · [Deploy Failure Modes](#deploy-failure-modes) · [Write It Down](#write-it-down)

## The Release Directory

```
/srv/api/
├── releases/
│   ├── 2026-07-24T0912-a41b7e/
│   └── 2026-07-25T1740-7c02bb/
├── current -> releases/2026-07-25T1740-7c02bb
└── shared/
    ├── env            # secrets, 0640, never in a release
    ├── uploads/       # user data, symlinked into each release
    └── log/
```

- The release directory name carries the commit, so "what is running" is answerable by `readlink current` — no build metadata endpoint required.
- Anything that must survive a deploy lives in `shared/` and is symlinked in. An uploads directory inside the release directory is deleted by the third cleanup and nobody notices for a week.
- Keep the last 5 releases and prune the rest. Fewer than 3 and you cannot skip back over a bad one; more than 10 and disk becomes the surprise.
- **The symlink flip must be atomic.** `ln -sfn new current` on the same filesystem replaces in one operation; `rm current && ln -s new current` leaves a window with no `current` at all, and a worker restarting in that window fails to start.

## The Deploy Sequence

1. **Build elsewhere.** A release directory is populated by copy or by pulling an artifact, never compiled in place: a failed build on the target leaves a half-release and a busy CPU on a serving box.
2. **Prepare the new release fully** — dependencies installed, assets compiled, symlinks to `shared/` in place — while the old one keeps serving.
3. **Run expand-phase migrations** (below), which are safe against the running old code.
4. **Flip the symlink.**
5. **Reload, do not restart** (SKILL.md Rule 6): `systemctl reload`, `pm2 reload`, or a graceful signal. Workers pick up the new `current` as they recycle.
6. **Health gate**: poll `health_path` until it passes, with a deadline. Failing the gate means rolling back now, not investigating while broken.
7. **Contract-phase migrations** only after the new code has been healthy long enough that you are not going back.
8. **Write the row** to `deploys/<year>.md` — version, migration phase, and the exact rollback target (last section).

Steps 3 and 7 are one migration split in two; collapsing them is the most common cause of a deploy that cannot be rolled back.

## Rollback

```
ln -sfn releases/<previous> current && systemctl reload api
```

Seconds, no network, no build, no registry. This is the entire justification for the release-directory layout.

What breaks rollback, in order of frequency:

- **A destructive migration.** Once a column is dropped, the old code cannot run. Expand/contract exists for exactly this.
- **Assets purged for the old release** while a client still holds an HTML page referencing them. Keep old asset bundles for at least one release cycle.
- **A config change outside the release.** If the deploy edited a proxy vhost or an env file, the symlink flip does not undo it — so record what changed outside the release directory, in the deploy row.
- **Pruning too aggressively**: the release you need is the one that was cleaned up this morning.

"Roll back by deploying the previous commit" is a build under pressure, at the worst hour, exercising a path nobody tested. It is not a rollback plan.

## Migrations Are the Hard Part

Expand/contract, always, because during any reload both versions of the code are briefly alive:

| Phase | Deploy | Safe because |
|---|---|---|
| Expand | Add the column nullable, add the new table, add the index concurrently, dual-write | Old code ignores what it does not know |
| Migrate | Backfill in batches, verify | Nothing reads the new shape as truth yet |
| Switch | New code reads the new shape | Old code still works if you roll back |
| Contract | Drop the old column, remove dual-write — in a **later** deploy | Only after rollback is off the table |

- **Never rename a column in one step.** Add, dual-write, backfill, switch reads, drop.
- **Adding a NOT NULL column with a default rewrites the table** on older database versions and locks it for the duration. Add nullable, backfill, then add the constraint.
- **Index creation locks writes** unless created concurrently; the concurrent variant is slower and can leave an invalid index that must be dropped and retried.
- **Long migrations do not belong in the deploy path.** A migration that takes 20 minutes and holds a lock is an outage with a progress bar. Run it separately, ahead of the deploy that needs it.
- Every migration needs a stated rollback: reversible, or explicitly one-way and therefore gating the rollback window. Write which one it is in the deploy row.

## Configuration and Secrets

- Configuration lives outside the release (`shared/env`, `/etc/<app>/env`, or the supervisor's environment file), so a rollback does not revert a config change and a config change does not require a deploy.
- A new release that needs a new variable must tolerate its absence for the length of the deploy, or the variable is set *before* the flip. Ordering config after code is a reliable way to produce a broken health gate.
- The app should fail loudly at startup on a missing required variable rather than at first use — a silent default in production is worse than a failed deploy.
- Never write secret values into anything under `~/Clawic/data/`: the deploy row records `env:DATABASE_URL` or `file:/srv/api/shared/env`, never the contents (`memory-template.md`).

## Assets and Cache Busting

- Hashed filenames (`app.9f2c1d.js`) let assets be immutable and cached for a year; the HTML that references them must be revalidated on every request (`static.md`).
- During a deploy, a browser holds an HTML page listing the old filenames. If the old assets are gone, that page breaks until reload — which is why old bundles stay for at least one release, and why assets are uploaded *before* the flip, never after.
- With a CDN, purge only the HTML. Purging hashed assets does nothing useful and empties a warm cache.

## Health Gate

`health_path` must be a real check of *this* instance: process up, config loaded, essential local state ready. Give it a deadline (30-60s is generous for most apps) and a decision:

```
for i in $(seq 1 30); do
  curl -fsS http://127.0.0.1:8000/healthz >/dev/null && exit 0
  sleep 2
done
exit 1   # the caller rolls back
```

Readiness includes dependencies; liveness does not (SKILL.md Rule 9). A deploy gate should use readiness — a new release that cannot reach the database is not ready even though the process is alive. And a health endpoint that only returns `200 OK` unconditionally passes every gate including the ones it should fail.

## Blue-Green on One Machine

Two instances on adjacent ports, the proxy pointing at one:

1. Green (8001) is live; deploy blue (8002) with the new release.
2. Health-check blue directly on its port — with real requests, not just `/healthz`.
3. Change the proxy's upstream to 8002 and reload: existing connections finish on green, new ones go to blue.
4. Keep green running for the rollback window, then stop it.

Costs double memory during the window and requires the app to tolerate two instances against one database (usually fine; not fine if it holds an exclusive lock, runs a scheduler, or writes to the same local cache directory). Give exactly one instance the scheduler role, or a duplicated cron fires twice.

Socket activation (`processes.md`) gives most of the benefit for a single instance with none of the memory cost: systemd holds the listening socket and queues connections during the restart.

## Deploying Containers

- Deploy by **digest**, not by tag: `image: app@sha256:…`. A moving tag means two boxes silently run different code, and "roll back to `latest`" is meaningless (`containers.md`).
- Pull before switching (`docker compose pull`), so the download is not part of the downtime window and a registry outage fails before anything stops.
- `docker compose up -d` recreates only changed services; it is closer to a reload than a restart, but in-flight requests still drop unless a proxy drains the old container first.
- Rollback is `up -d` with the previous digest — which means the previous digest has to be written down, in the deploy row, at deploy time.

## Deploy Failure Modes

| Symptom | Cause |
|---|---|
| New code serving old behavior | Workers never recycled — reload not wired (`ExecReload` missing), or the app caches `current` at boot and needs a restart |
| 502s for a few seconds every deploy | Restart instead of reload, or no drain before stopping the old instance |
| Works, then fails minutes later | A worker recycled into the new code and hit a missing migration or variable |
| Fails only on the first deploy after a reboot | Something was set by hand and never persisted — an environment variable, a symlink, a limit |
| Disk full during deploy | Release directories never pruned, or the build ran on the target |
| Half the requests on new code, half on old | Multiple upstreams and only one was updated |
| Rollback did not restore behavior | A config file or migration outside the release changed too |

## Write It Down

Every release gets its row in `~/Clawic/data/server/deploys/<year>.md`: date, service, version or commit, whether a migration ran and in which phase, **the rollback target as an exact release directory or image digest**, anything changed outside the release, and the result (`memory-template.md`). A rollback gets its own row with the reason and how long it took. If the deploy sequence for this service has any step a stranger would not guess, it belongs in `~/Clawic/data/server/artifacts/runbook-deploy-<service>.md` with its `## Boxes` line added the same turn.
