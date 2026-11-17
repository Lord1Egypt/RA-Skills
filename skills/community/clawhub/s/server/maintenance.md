# Keeping It Alive — Cadences, Backups, Upgrades, Restores

The work that has no deadline and therefore never happens, until it happens all at once. This file is the recurring list and the two procedures nobody rehearses.

**At the start of every session**, check the `## Due` table in `~/Clawic/data/server/memory.md` against today's date and state anything overdue in one line — a statement, not a question. That table is the only reason any of this gets done twice.

**Contents:** [The Cadences](#the-cadences) · [Backups: What, Where, How Often](#backups-what-where-how-often) · [The Restore Drill](#the-restore-drill) · [Upgrades](#upgrades) · [Reboots](#reboots) · [The Monthly Sweep](#the-monthly-sweep) · [Uptime and Health Monitoring](#uptime-and-health-monitoring) · [Decommissioning](#decommissioning) · [Handover](#handover) · [Write It Down](#write-it-down)

## The Cadences

Seed `## Due` with these when a box is first taken on; adjust the intervals to what the user will actually sustain, because a schedule nobody keeps is worse than a shorter one they do.

| What | Every | Why this interval |
|---|---|---|
| Certificate expiry sweep — served expiry, not the file | Month | 90-day certificates renew at 30 days out; a monthly check catches a broken renewal with weeks to spare (`tls.md`) |
| Domain registrar expiry | Quarter | Nothing renews it automatically unless auto-renew is on and the card is valid |
| OS and runtime security updates | Month, or automatic with a known reboot policy | The window between disclosure and mass exploitation is days |
| Container image rebuild/pull | Month | Pinning without rebuilding runs a two-year-old base forever (`containers.md`) |
| Disk, inode and log-rotation check | Month | The most preventable outage there is (`logs.md`) |
| Backup restore drill | Quarter | An untested backup is a hypothesis (below) |
| Dependency vulnerability scan | Month | The vulnerability arrives after your last deploy |
| Review of what is listening | Quarter | Services accumulate; the exposure sweep is four commands (`security.md`) |
| Capacity re-measurement | Before any launch, and half-yearly | Traffic grows past a limit that was always there (`capacity.md`) |
| Self-hosted app upgrades | Month, reading release notes | Breaking migrations are one-way (`selfhosted.md`) |

Each entry, once run, updates its `Last run` and `Next due` in `## Due` the same turn. A checklist without a last-run date gets skipped for two quarters and nobody notices.

## Backups: What, Where, How Often

**What** — enumerate before configuring anything; the omission is always discovered at restore time:

| Class | Examples | Recoverable without a backup? |
|---|---|---|
| Databases | Postgres, MySQL, SQLite files, embedded stores | No |
| User content | Uploads, media, documents, photo originals | No |
| Configuration | Unit files, vhosts, compose files, env structure | Only if it is in a repository — and the env *values* are not |
| Secrets | Keys, tokens, certificates | Rotate rather than restore, but you need the list of what exists |
| Derivatives | Thumbnails, caches, indexes, compiled assets | Yes — exclude them and the backup shrinks by an order of magnitude |
| The OS | Packages, kernel | Yes, by rebuilding — which is why a rebuild script beats a disk image |

**How** — a running database is not backed up by copying its files: use `pg_dump`/`mysqldump`, the app's own export, a filesystem or volume snapshot that is crash-consistent, or stop the service first. A file-level copy of a live database restores as corruption, quietly.

**Where** — the 3-2-1 shape, stated plainly: at least one copy **off the box**, and at least one copy the box's own credentials cannot delete. Ransomware and a bad `rm -rf` both walk every path the server can write to; an append-only or separately-credentialed destination is what survives them. A snapshot on the same provider, in the same account, is a convenience, not an off-site backup.

**How often** — from the data's tolerance, not from habit: `RPO` is how much you can afford to lose. Hourly database dumps and daily content sync is a common shape; a photo library that only changes when someone uploads can be event-driven.

**Retention** — enough generations to survive a corruption you did not notice for a while: dailies for two weeks, weeklies for two months, monthlies for a year is a defensible default. A single overwritten copy backs up your corruption on schedule.

**Verify** — a backup job that silently fails is the norm, not the exception. Check the age and size of the newest artifact, and alert on *absence*, not just on error: the most common failure is a job that stopped running entirely.

## The Restore Drill

Quarterly, into a scratch location, timed. Never into production.

1. Pick a service, and pretend the box is gone.
2. Provision a scratch target (a VM, a container, a spare host).
3. Restore from the backup **as documented**, following only the runbook — no improvising, because improvising is what proves the runbook is missing something.
4. Bring the service up and verify with a real request, not a process check.
5. **Record the elapsed time** and everything that was missing from the runbook, in `~/Clawic/data/server/artifacts/runbook-restore-<service>.md`. That list is the whole value of the exercise: it is always ownership, an environment variable, a database role, a certificate, or a path nobody wrote down.
6. Update the runbook, then destroy the scratch target.

The measured time is your real RTO. The number people assume is invariably a third of what the drill shows, and the difference is entirely made of small missing steps.

Restore-drill results go in `## Due` (last run) and the findings in the runbook artifact; a drill that revealed a gap serious enough to have caused an outage also belongs in `incidents/<year>.md`.

## Upgrades

Order of risk, lowest to highest: application dependency < container image patch < runtime minor < OS point release < database major < OS major.

- **Read the release notes for anything that migrates data.** For self-hosted apps this is the entire risk assessment (`selfhosted.md`).
- **Back up before, always** — for a database or a stateful app, immediately before, not last night's.
- **Know the previous version**: the release directory, the image digest, or the package version. `apt` keeps old packages in its cache and that is often the fastest rollback available.
- **One thing at a time**, with a check between. An OS upgrade and an application upgrade in the same window means the bisect afterwards is manual and slow.
- **Sequential major versions** for anything that migrates a database; skipping is unsupported more often than not, and the failure surfaces after the migration has already run.
- **Restart what needs restarting.** A library upgrade does not take effect in a long-running process until it restarts; `needrestart` and equivalents list what is still running old code. A patched box running the unpatched process in memory is a patched box in the report only.
- Unattended security updates are the right default for a box with no on-call, paired with an explicit reboot policy — automatic, in the maintenance window, or manual with a monthly reminder. What is not acceptable is installing kernel updates forever and never rebooting.

## Reboots

- Before: check that everything is `enabled`, not merely running (`systemctl list-unit-files --state=enabled`), that the container runtime is enabled, and that nothing critical is running from a shell (`processes.md`).
- After: verify each service in `## Services` answers, not just that the box pings. The whole point of a reboot test is to discover the service somebody started by hand in March.
- A scheduled reboot in the maintenance window is far cheaper than an unplanned one at peak. A box with an uptime of 400 days is not a boast; it is an untested boot sequence carrying an unpatched kernel.

## The Monthly Sweep

Twenty minutes, in this order:

| Check | Command or place |
|---|---|
| Disk and inodes | `df -h`, `df -i` — investigate anything above 80% |
| Journal size | `journalctl --disk-usage` |
| Log rotation is working | Newest rotated file is recent, and `access.log` is not the biggest file on the box |
| Failed units | `systemctl list-units --state=failed` |
| Unhealthy or restarting containers | `docker compose ps` per stack, or `docker ps --filter health=unhealthy` |
| Restart counts | A service that restarted 400 times is crash-looping successfully enough that nobody noticed |
| Certificate expiry, from the wire | For every hostname in `domains.md` (`tls.md`) |
| Pending updates and reboot-required | The distro's mechanism |
| Backup freshness | Newest artifact's age and size, per service |
| Memory headroom | Swap in use at all on a server is a signal, not a state |

Record the date in `## Due` and anything found in the relevant box. A sweep with no written outcome is indistinguishable from a sweep nobody did.

## Uptime and Health Monitoring

- An external check beats an internal one: something outside the box, hitting a real URL, from a network that is not yours. A monitor running on the machine it monitors reports nothing at the moment it matters.
- Check what a user does — fetch a page and assert on its content — not just that a port accepts a connection. A proxy serving a 502 answers TCP perfectly.
- Alert on: down, certificate expiring within 14 days, disk above 90%, and the backup job not having run. Four alerts that fire rarely beat forty that fire weekly and get muted.
- A dead-man's switch for anything scheduled (the backup pings a service when it finishes; the service alerts if the ping does not arrive) catches the failure mode alerting on errors cannot: the job that stopped running.
- Deep observability — metrics, traces, dashboards — is the `monitoring` skill's territory; what belongs here is the minimum that tells you the service is down before a user does.

## Decommissioning

Retiring a service is a procedure, not a `stop`:

1. Confirm nothing depends on it — DNS records, other services, cron jobs, webhooks registered elsewhere.
2. Take a final backup and verify it opens.
3. Stop and disable the unit or stack; leave it in place, off, for a cooling-off period.
4. Remove the proxy vhost and the DNS record; keep the certificate until the record is gone, then let it lapse.
5. Delete the data, the volumes, and the release directories.
6. **Delete the row** from `## Services`, the host row from `servers.md` if the machine is gone, and the domain row from `domains.md` if it was released — noting the date in `memory.md`. An inventory that only grows stops being an inventory (`memory-template.md`).

Step 6 is the one that gets skipped, and its cost is a phantom entry that someone tries to debug two years later.

## Handover

If someone else may have to run this box — including yourself after a year away — the minimum written set is: what runs on it (`## Services`), what the hostnames and certificates are (`domains.md`), how a release ships and rolls back (`deployment.md` plus the deploy log), where the backups are and how a restore goes (the drill runbook), and where the secrets live as pointers, never values.

That set is exactly what this skill's boxes already hold. Keeping them current *is* the handover document, which is the argument for writing them as you go rather than at the end.

## Write It Down

Every recurring item lives in `## Due` with its interval, last run and next due, updated the same turn it runs (`memory-template.md`). The backup and restore procedure for each service goes to `~/Clawic/data/server/artifacts/runbook-restore-<service>.md` with the measured RTO from the last drill and its `## Boxes` line added the same turn. Upgrades that changed behavior go in `deploys/<year>.md`; anything that broke goes in `incidents/<year>.md` with the real cause. Decommissioned services get their rows deleted, with the date noted — not left behind as history.
