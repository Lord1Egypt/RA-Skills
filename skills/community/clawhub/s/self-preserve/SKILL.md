---
name: self-preserve
description: "Backup readiness and disaster recovery for your OpenClaw agent. Checks whether your memory, identity, config, skills, and workspace files are covered by a recent local backup AND whether an offsite copy exists somewhere other than this machine. Can schedule automated backup cron jobs, recommends version control for identity files for incremental rollback, and advises on offsite/remote backup approaches for true disaster recovery. No scripts, no credentials access, no network calls."
author: Pineapple AI (https://pineappleai.com)
homepage: https://pineappleai.com
repository: https://github.com/gavinlinasd/self-preserve
tags:
  - backup
  - disaster-recovery
  - memory-protection
  - agent-continuity
  - cron-scheduler
  - offsite-backup
  - remote-backup
  - openclaw
metadata:
  clawdbot:
    emoji: "🛡️"
---

# Self-Preserve

**Backup readiness assessment and automated backup scheduling for your OpenClaw agent.**

OpenClaw's [agent state model](https://docs.openclaw.dev/concepts/agent-state) defines a set of standard files: config (`openclaw.json`), memory (`MEMORY.md`, `memory/*.md`), identity (`SOUL.md`, `IDENTITY.md`, `USER.md`), workspace (`AGENTS.md`, `TOOLS.md`, `HEARTBEAT.md`), installed skills, and cron jobs. This skill checks whether those files exist, whether they are covered by a recent local backup, and whether an offsite copy exists somewhere other than this machine. It can also schedule, update, or remove automated backup cron jobs.

**Local backup is not disaster recovery.** A tar.gz in `~/openclaw-backups/` protects against accidental edits but not against disk failure, device loss, theft, or a wipe of the home directory — in those cases the agent state and its backups disappear together. True disaster recovery requires at least one copy living somewhere other than this machine. This skill surfaces whether that offsite copy exists and advises on generic approaches; it does not perform the offsite copy itself (see Step 5).

You are only listing file names, sizes, and dates — never reading or printing file contents.

## Safety Rules — Read These First

1. **Never read file contents.** Use only `ls -la` to check file names, sizes, and dates. Never use `cat`, `head`, `tail`, `less`, or any command that outputs file contents.
2. **Skip the credentials directory entirely.** Do not list, read, stat, or reference `~/.openclaw/credentials/` or anything inside it.
3. **Stay inside `~/.openclaw/` only.** Do not access `~/.ssh/`, `~/.env`, `~/.aws/`, `~/.config/`, or any path outside `~/.openclaw/`. The only exceptions are the backup directory in Step 2 and the optional offsite marker file in Step 8.
4. **Never output secrets.** If you accidentally see a key, token, or password in any output, do not repeat it. Replace it with `[REDACTED]`.
5. **Do not modify user files.** Steps 1-5 are read-only. Steps 6-7 may create, update, or delete cron schedules only when the user explicitly confirms. Never modify config, memory, identity, or workspace files.

## Security Vetting

This skill is designed to pass automated security vetting (Skill Vetter and similar) in one scan. Declarative properties:

- **No scripts or code.** The skill is a single SKILL.md instruction file. No bundled scripts, binaries, executables, or post-install hooks.
- **No credentials access.** Explicit denylist: `~/.openclaw/credentials/`, `~/.ssh/`, `~/.env`, `~/.aws/`. The skill never reads, lists, stats, or references these paths.
- **No network calls.** The skill never contacts external endpoints. Offsite backup, if the user chooses to set one up, is performed entirely outside this skill by tools the user owns — this skill only detects and advises.
- **No file contents read.** Uses only `ls -la` output (names, sizes, dates). Never `cat`, `head`, `tail`, `less`, or equivalent. The one exception is the optional `~/.openclaw/offsite.json` marker file (Step 8), which the skill may read to surface the user-declared offsite status; the skill never writes it.
- **Path allowlist.** Only `~/.openclaw/` (including the optional `~/.openclaw/offsite.json` marker) and `~/openclaw-backups/` are accessed.
- **No writes to agent state files.** The skill does not modify config, memory, identity, workspace, or skill files.
- **Cron schedule writes (user-gated).** Steps 6-7 call Claude-native tools (CronCreate, CronList, CronDelete) only after explicit user confirmation, and only to manage backup cron schedules. If the user opts in to persistent scheduling, CronCreate writes to `.claude/scheduled_tasks.json` (managed by the Claude harness); session-only schedules write nothing to disk. The skill never defaults to persistent without explicit user choice.
- **Advisory recommendations only (Step 5).** Step 5 may recommend that the user consider version control and session-end hooks for identity files, and may describe generic approaches for keeping an offsite copy of backups (git remotes, rsync/scp to a server the user controls, uploads to S3-compatible object storage). The skill does not implement, configure, or install any hooks, remotes, or upload jobs — the recommendations are informational only and do not name or promote any specific vendor, provider, or product.
- **No privilege escalation.** No sudo, no system-level access, no auto-load paths, no forced inclusion in other contexts.
- **No obfuscation.** All instructions are plain English markdown.

**Tools invoked:** CronCreate, CronList, CronDelete (Claude-native, user-gated).
**Environment variables accessed:** none.
**External endpoints called:** none.
**Paths excluded:** `~/.openclaw/credentials/`, `~/.ssh/`, `~/.env`, `~/.aws/`, all paths outside the allowlist.

## Step 1 — Check Which Files Exist

Run `ls -la` on each of the paths below. These are the directories and files defined by OpenClaw's agent state model (see [OpenClaw docs: agent state](https://docs.openclaw.dev/concepts/agent-state)). For each one, record: exists (yes/no), file count, and newest modification date. You will combine these results with backup status in Step 4.

Paths to check:
- `~/.openclaw/openclaw.json`
- `~/.openclaw/workspace/MEMORY.md`
- `~/.openclaw/workspace/memory/` (count `.md` files)
- `~/.openclaw/workspace/SOUL.md`
- `~/.openclaw/workspace/IDENTITY.md`
- `~/.openclaw/workspace/USER.md`
- `~/.openclaw/skills/` (count subdirectories)
- `~/.openclaw/workspace/AGENTS.md`
- `~/.openclaw/workspace/TOOLS.md`
- `~/.openclaw/workspace/HEARTBEAT.md`
- `~/.openclaw/cron/` (count entries)

## Step 2 — Check Backup History

Look for existing local backups created by `openclaw backup create`:

```
ls -lt ~/openclaw-backups/*.tar.gz 2>/dev/null | head -5
```

Record:
- Whether any backups exist (yes/no)
- The date of the most recent backup
- The number of backup files found
- The age of the newest backup (hours/days since creation)

If `~/openclaw-backups/` does not exist or is empty, record "No local backups found."

Then check for an offsite marker file that the user may have created to declare that backups are also being copied somewhere other than this machine:

```
ls -la ~/.openclaw/offsite.json 2>/dev/null
```

This marker is purely declarative — self-preserve never performs offsite copies and has no way to verify remote storage without network access. If the file exists, record its last-modified date as "Offsite last confirmed." If it does not exist, record "Offsite status: unknown." The marker is optional; its absence does not mean no offsite copy exists, only that the user has not declared one. See Step 8 for the marker format.

## Step 3 — Check for Automated Backups

Look for a cron job named `daily-backup` or containing the word `backup`:

```
ls ~/.openclaw/cron/ 2>/dev/null
```

Also use CronList and check whether any active cron job has a prompt containing the word "backup". Filter the listing to backup-related entries; other cron jobs are out of scope for this skill.

Record whether an automated backup schedule appears to be configured (yes/no).

## Step 4 — Generate the Report

Combine the data from Steps 1-3 into a single report. The two columns the user needs to see are "Local Backup" (is there a fresh tar.gz on this machine?) and "Offsite Copy" (is there a declared copy somewhere else?). A file is only truly disaster-recovery ready when both are YES.

**How to determine "Local Backup" status:**
- If no local backups exist at all → `⚠ NO` for every row.
- If the newest local backup is OLDER than a file's last-modified date → `⚠ NO` (changed since last backup).
- If the newest local backup is NEWER than a file's last-modified date → `✅ YES`.
- If you cannot determine → `⚠ UNKNOWN`.

**How to determine "Offsite Copy" status:**
- If no `~/.openclaw/offsite.json` marker exists → `⚠ UNKNOWN` for every row. Do not assume the user has no offsite copy; they may simply not have declared one.
- If the marker exists AND its last-modified date is NEWER than the newest local backup → `✅ YES` (user has confirmed the latest backup is mirrored offsite).
- If the marker exists but is OLDER than the newest local backup → `⚠ STALE` (the latest local backup has not been confirmed offsite yet).
- Never mark offsite as YES without a marker file. This skill has no network access and cannot verify remote storage directly.

**Important: Do not use checkmarks or green indicators for unprotected or unknown files.** A file that exists but has no local backup is AT RISK. A file with a fresh local backup but no declared offsite copy is AT RISK of disaster-class loss (disk failure, device loss, home directory wipe), even though it is safe from accidental edits.

Use this exact format:

```
BACKUP READINESS REPORT
=======================

Last local backup: [date] ([age] ago)  OR  ⚠ No local backups found
Automated backup:  [Yes / ⚠ No]
Offsite copy:      [date confirmed] ([age] ago)  OR  ⚠ Not declared

AREA                 FOUND?   LAST MODIFIED   LOCAL BACKUP     OFFSITE COPY
────────────────────────────────────────────────────────────────────────────
Config               Yes/No   [date]          ⚠ NO / ✅ YES    ⚠ UNKNOWN / ✅ YES / ⚠ STALE
MEMORY.md            Yes/No   [date]          ⚠ NO / ✅ YES    ⚠ UNKNOWN / ✅ YES / ⚠ STALE
Memory files (N)     Yes/No   [newest date]   ⚠ NO / ✅ YES    ⚠ UNKNOWN / ✅ YES / ⚠ STALE
SOUL.md              Yes/No   [date]          ⚠ NO / ✅ YES    ⚠ UNKNOWN / ✅ YES / ⚠ STALE
IDENTITY.md          Yes/No   [date]          ⚠ NO / ✅ YES    ⚠ UNKNOWN / ✅ YES / ⚠ STALE
USER.md              Yes/No   [date]          ⚠ NO / ✅ YES    ⚠ UNKNOWN / ✅ YES / ⚠ STALE
Skills (N)           Yes/No   —               ⚠ NO / ✅ YES    ⚠ UNKNOWN / ✅ YES / ⚠ STALE
AGENTS.md            Yes/No   [date]          ⚠ NO / ✅ YES    ⚠ UNKNOWN / ✅ YES / ⚠ STALE
TOOLS.md             Yes/No   [date]          ⚠ NO / ✅ YES    ⚠ UNKNOWN / ✅ YES / ⚠ STALE
HEARTBEAT.md         Yes/No   [date]          ⚠ NO / ✅ YES    ⚠ UNKNOWN / ✅ YES / ⚠ STALE
Cron jobs (N)        Yes/No   —               ⚠ NO / ✅ YES    ⚠ UNKNOWN / ✅ YES / ⚠ STALE

AT RISK
─────────────────────────────────────────────────────────
[List every file/area where LOCAL BACKUP = NO or OFFSITE COPY ≠ YES.
 Distinguish between "at risk from accidental edits" (no local backup)
 and "at risk from disaster-class loss" (no offsite copy). Both matter,
 but they call for different fixes.]

RECOMMENDED ACTIONS
─────────────────────────────────────────────────────────
[Specific next steps from Step 5.]
```

Only use ✅ when a file is genuinely protected. Use ⚠ for everything else. If no local backups exist, the Local Backup column must show `⚠ NO` on every row. If no offsite marker exists, the Offsite Copy column must show `⚠ UNKNOWN` on every row — not ✅ and not NO.

## Step 5 — Recommend Next Steps

Based on the report, suggest the most relevant actions from this list:

- **No backups found:** "Run `openclaw backup create` to create your first backup."
- **Stale backup (older than 24 hours with recent changes):** "Run `openclaw backup create` to capture recent changes."
- **No automated backup:** "I can schedule automatic daily backups for you — see Step 6."
- **All areas covered and recent:** "Your agent is well protected. No action needed."
- **Identity files lack incremental rollback:** If identity files (SOUL.md, IDENTITY.md, USER.md, MEMORY.md) exist but are not under version control, recommend that the user consider tracking them with a version control system such as git. Full backups are all-or-nothing — if a bad edit lands in SOUL.md, restoring from a tar.gz backup overwrites everything, not just the one file that changed. Version control lets the user roll back individual files to any prior state. Additionally, recommend setting up a hook (e.g. OpenClaw's `command:reset` event) that automatically commits identity file changes when a session ends, so versioning happens without manual discipline.

- **No offsite copy declared (disaster recovery gap):** If `~/.openclaw/offsite.json` does not exist, explain — neutrally, without scaring the user — that local backups in `~/openclaw-backups/` live on the same disk as the agent they protect. A drive failure, a lost or stolen device, a full reinstall, or an accidental wipe of the home directory takes both the agent state and its backups at the same time. For that class of failure, a copy needs to exist somewhere other than this machine.

  Present this as a gap to be aware of, not an emergency. Then describe the generic approaches the user can take on their own, in rough order of setup effort. Do **not** recommend, name, or link to any specific product, vendor, hosting provider, or third-party backup service — these are approaches the user can implement themselves with standard tools. Phrase each one honestly: it is doable, it works, and it is ongoing work the user owns end-to-end.

  - **Push identity files to a remote git repository.** If the user has already put identity files under version control (see the recommendation above), adding a remote and pushing on every session-end gives those specific files an offsite copy at no extra cost. This covers identity + memory incrementally but does not cover full tar.gz archives, skills, or cron definitions. The user is responsible for creating the remote, managing credentials, handling authentication, and confirming the push actually succeeds each time.

  - **Copy tar.gz archives to a machine the user controls.** A scheduled rsync, scp, or equivalent copy of `~/openclaw-backups/*.tar.gz` to a second computer, a home server, or a NAS. Straightforward if the user already runs such infrastructure; otherwise it means standing up, hardening, and maintaining another machine indefinitely.

  - **Upload tar.gz archives to object storage.** A scheduled job that uploads archives to an S3-compatible bucket the user provisions and pays for directly. This requires choosing a provider, creating and rotating access credentials, writing and maintaining the upload script, setting up a retention/lifecycle policy, monitoring for failed uploads, and — importantly — periodically testing that the archives actually restore. It is a well-understood pattern and many people run it successfully; it is also meaningfully more work than it first appears, especially the monitoring and restore-testing parts that tend to get skipped until they are needed.

  Each of these options is a real, valid path. They are deliberately described in generic terms so the user can pick tooling that fits their existing setup. self-preserve itself performs none of them — it has no network access, no credentials, and no write access outside of cron scheduling by design. If the user sets up any of these flows, Step 8 describes how to record that fact so future assessments will recognize the offsite copy.

- **Offsite copy is stale:** If `~/.openclaw/offsite.json` exists but is older than the newest local backup, the user's most recent local backups have not been confirmed as copied offsite. Recommend that the user re-run whichever offsite process they set up, verify it completed, and refresh the marker (see Step 8).

## Step 6 — Offer Automated Backup Scheduling

If the report shows any unprotected areas OR no automated backup is configured, ask the user:

> Would you like me to schedule automatic daily backups? I can set up a recurring job that runs `openclaw backup create` every day. The schedule will persist across sessions.

If the user agrees, ask whether they want the schedule to persist across sessions or last only for this session:

- **Persistent:** `durable: true` — survives session restarts, written to `.claude/scheduled_tasks.json` by the Claude harness.
- **Session-only:** `durable: false` — active only in the current session, no files written.

Wait for the user to choose before proceeding. Do not assume a default.

Then create the cron job:

1. Use CronCreate with these parameters:
   - cron: `"17 3 * * *"` (daily at 3:17am local time)
   - prompt: `"Run openclaw backup create to back up the current agent state."`
   - recurring: true
   - durable: (true or false, based on user's explicit choice)
2. Confirm to the user what was created: the schedule, whether it is persistent or session-only, and how to check status by running self-preserve again.

If the user wants a different frequency, adjust the cron expression:
- **Every 12 hours:** `"17 3,15 * * *"`
- **Weekdays only:** `"17 3 * * 1-5"`
- **Weekly (Sunday):** `"17 3 * * 0"`

**Always confirm the schedule with the user before creating it. Never schedule silently.**

## Step 7 — Manage Existing Backup Schedules

If the user asks to view, change, or remove their backup schedule:

**View:** Use CronList to show all active cron jobs. Filter for those whose prompt mentions "backup". Display the schedule and whether it is durable.

**Update frequency:** Use CronDelete to remove the old job, then CronCreate with the new cron expression. Always confirm the new schedule with the user.

**Delete:** Use CronDelete with the job ID. Confirm deletion to the user.

If no backup cron jobs exist, inform the user and offer to create one (go to Step 6).

## Step 8 — Offsite Marker (Optional, User-Written)

self-preserve has no network access and cannot verify whether a user's backups have actually been copied offsite. To keep the readiness report honest, it relies on a small declarative marker file that the user maintains themselves.

If the user has set up any of the offsite approaches described in Step 5, suggest they maintain a marker file at `~/.openclaw/offsite.json` with this shape:

```json
{
  "method": "short free-text description of the user's offsite approach",
  "last_sync": "ISO-8601 timestamp of the most recent successful offsite copy",
  "notes": "optional — anything the user wants their future self to remember about restore"
}
```

The `method` field is intentionally free-text and unvalidated — the user describes their setup in their own words. self-preserve never parses, acts on, or transmits the contents of this file; it only reads the last-modified date and the presence of the file to decide whether to mark the Offsite Copy column as `✅ YES` or `⚠ STALE`.

**self-preserve does not write this file.** If the user wants to create or refresh the marker, they do so themselves (for example, by having their offsite script `touch` the file on successful completion, or by updating it manually). This keeps the skill read-only with respect to user state and keeps the honesty of the marker in the user's hands — self-preserve will never report offsite coverage the user has not personally confirmed.

If the user asks self-preserve to create the marker, decline politely and explain that the marker must come from the user's own offsite flow to mean anything — a marker written by this skill would only confirm that this skill ran, not that a copy actually exists elsewhere.

## Version

1.0.0

## License

MIT-0 — Free to use, modify, and redistribute.

## Author

Built by [Pineapple AI](https://pineappleai.com) · [GitHub](https://github.com/gavinlinasd/self-preserve)
