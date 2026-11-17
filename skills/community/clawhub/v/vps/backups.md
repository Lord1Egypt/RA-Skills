# Backups — Restorable, or They Do Not Exist

Read when setting up backups, when asked "am I covered", before any risky change, and when a restore is needed. `backup_target` says where data goes; the restore drill cadence lives in `## Due`.

**Before answering "am I covered"**, read `## Due` in `~/Clawic/data/vps/memory.md` for the last timed restore, and `changes/<year>.md` for the drill table. A backup whose restore has never been timed has an unknown recovery time, which is the same as an unknown outage length.

**Contents:** [Snapshots Are Not Backups](#snapshots-are-not-backups) · [3-2-1 for a Rented Server](#3-2-1-for-a-rented-server) · [What Actually Needs Backing Up](#what-actually-needs-backing-up) · [Databases Need Their Own Job](#databases-need-their-own-job) · [Retention](#retention) · [Encryption and the Passphrase Problem](#encryption-and-the-passphrase-problem) · [The Restore Drill](#the-restore-drill) · [Restoring Under Pressure](#restoring-under-pressure) · [Cost](#cost) · [Backups That Silently Stop](#backups-that-silently-stop)

## Snapshots Are Not Backups

A provider snapshot is a copy of the disk held in the account that can delete it. It is excellent at one job and useless at three others.

| | Snapshot | Backup |
|---|---|---|
| Recovers from a bad upgrade | Yes, and fast | Yes, slower |
| Recovers from provider account loss, closure, or compromise | **No** | Yes, if a copy lives elsewhere |
| Recovers from accidental deletion of the server | Only if the snapshot survived the same click | Yes |
| Restores a single file | Awkward — restore to a new machine, then copy | Yes, directly |
| Restores to a different provider | Usually not | Yes |
| Granularity | Whole disk, per snapshot | Per file, many versions |

Use both. Snapshots are the fast undo before a risky change; backups are what exists when the account does not.

**A snapshot of a running machine is crash-consistent**, equivalent to pulling the power: journaling filesystems and write-ahead-log databases recover from it, and an application that writes several files without atomicity may not. Quiesce or use the database's own dump for anything transactional.

## 3-2-1 for a Rented Server

Three copies, two media or locations, one offsite. Translated to a VPS:

1. The live data on the server.
2. A provider snapshot or the provider's backup add-on — the fast undo.
3. **A copy in a different account, ideally a different provider**: object storage elsewhere, or the user's own machine.

The third copy is the whole rule. A backup inside the account that can be closed for non-payment, compromised through a leaked token, or deleted with one click is copy number two wearing a different name.

Test for the offsite copy: **could you restore with the provider account permanently gone?** If the answer needs that account to log in, it is not offsite.

## What Actually Needs Backing Up

Restores fail on the things nobody listed. Enumerate per host:

- **Application data directories** — the obvious part.
- **Databases** — via a dump or a snapshot-aware method, not by copying files under a running engine.
- **Uploaded and generated files** — often outside the application directory and often the largest.
- **Configuration outside the repository**: reverse proxy config, systemd units, cron jobs, `.env` files, and certificates. Anything hand-edited on the box is unrecoverable if it is not backed up or in version control.
- **The provisioning file** — in the project repository, not on the server (`provisioning.md`).
- **The secret material's location**, not the secrets: which manager holds the database password, the backup passphrase, the API tokens. This belongs in the runbook as pointers.

Explicitly *not* backed up: the operating system, installed packages, and anything the provisioning file can rebuild. Backing up a whole disk to recover an application is how a 20 GB restore becomes a 200 GB one.

## Databases Need Their Own Job

- A file-level copy of a running database's data directory is a corrupt copy unless the engine is quiesced or the tool is engine-aware.
- The reliable pattern: the engine's own dump, on a schedule, to a directory that the file backup then picks up. It costs disk and it works.
- For anything where losing a day is unacceptable, continuous archiving of the write-ahead log gives point-in-time recovery — significantly more machinery, and the correct answer when the data has a revenue number attached.
- **Verify the dump, not the job's exit code.** A dump that ran successfully against the wrong database, or that was truncated by a full disk, exits zero.
- Restore across engine versions is not guaranteed. Note the engine version alongside the dump and in the host's row in `## Hosts`; a dump from a newer major version will not load into an older one, and that fact is only useful if it is written where the restore will read it.

## Retention

- The failure that retention protects against is **not** disk failure — the provider handles that. It is deletion or corruption you do not notice for a while: a bad migration, an accidental delete, ransomware.
- A workable default: daily for two weeks, weekly for two months, monthly for a year. Adjust by how long a silent corruption could go unnoticed, which is the real question.
- **Keep a count, not "everything".** Unbounded retention on per-GB storage is the second most common source of surprise cost in this domain (`costs.md`).
- Prune on a cadence in `## Due`, not by hand when the bill arrives.
- Immutable or append-only retention on the offsite copy defends against the case where the intruder has your backup credentials too. It is the difference between a bad day and a total loss.

## Encryption and the Passphrase Problem

- Encrypt anything leaving the server. Object storage in another account is another account.
- **The passphrase is the backup.** Losing it makes every copy worthless — this is a more common total-loss cause than any hardware failure.
- The passphrase lives in the user's password manager, with a second holder if there is a second person. Never in `~/Clawic/data/`, never in the repository, never only in the head of the person who set it up. The runbook records the pointer: `1password:Infra/backup-passphrase`.
- The backup credential on the server should be **append-only** where the storage supports it: a compromised box can then add backups but not delete history.

## The Restore Drill

The only thing that converts "we have backups" into a number. Quarterly, in `## Due`, with the clock running.

1. Create a scratch server, ideally at the size you would actually use in a disaster.
2. Restore from the offsite copy — not from the snapshot, since the snapshot is the path you already trust.
3. Bring the application up and check it actually works, including the pieces that live outside the data directory.
4. **Write the measured time** into the `## Restore Drills` table of `changes/<year>.md`, with everything that was missing or slowed you down.
5. Destroy the scratch server so it does not become a billed surprise (`costs.md`).

What drills reliably find, in rough order of frequency: the passphrase was in one person's head; configuration outside the data directory was never backed up; the database version on the new box did not match; the restore took four times the estimate because of download throughput; the backup had been failing silently for weeks.

## Restoring Under Pressure

- **Restore to a new machine, never over the live one.** The moment you overwrite, the diagnosis is gone and there is no going back.
- Establish *when* the damage happened before choosing which backup to restore — the most recent backup often already contains the problem.
- After a compromise, restore data only, from a copy predating the entry point (`security.md`).
- Snapshot the damaged machine first, whatever the cause. It is one click and it preserves the only copy of the evidence.
- Announce the recovery-time estimate from the last drill, not from optimism. That number is the reason the drill exists.

## Cost

- Snapshots bill per GB of **disk size**, not of data used, at most providers. A 200 GB disk that is 10% full still stores 200 GB of snapshot on some platforms.
- The managed backup add-on is commonly a flat percentage of the plan price, typically around a fifth. Convenient, and it is a same-account copy, so it never satisfies the third leg of 3-2-1.
- Offsite object storage is cheap to store and metered to retrieve. Restore egress is a real cost that appears exactly when you are already having a bad day — know the number before you need it.
- Deduplicating backup tools change the arithmetic dramatically for daily snapshots of slowly changing data, which is most application data.

## Backups That Silently Stop

The characteristic failure of this domain: the job stopped weeks ago and nothing said anything.

- **Alert on backup age, not on job failure.** A job that no longer runs cannot report a failure. The check is "is the newest backup younger than the interval", evaluated somewhere that is not the server being backed up.
- Common silent causes: the disk filled and the dump truncated; credentials expired; the repository was locked by an interrupted run; retention pruning deleted more than intended; the server was rebuilt and the job was never reinstalled.
- Record the last verified restore in `## Due`. An unverified backup is a plan, not a control.

---

**Write it down.** The backup policy for a host — target, schedule, retention, encryption pointer — goes in `## Hosts` in `~/Clawic/data/vps/memory.md`; the cadence for pruning and drills goes in `## Due`. Every restore drill gets a row in the `## Restore Drills` table of `~/Clawic/data/vps/changes/<year>.md`: date, what was restored, where to, **measured** recovery time, and what was missing. When a drill exposes gaps worth a procedure, write `~/Clawic/data/vps/artifacts/runbook-restore-<host>.md` with the steps, the version constraints, and the passphrase **pointer** — never the passphrase — and add its `## Boxes` line in the same turn.
