---
name: Skill Update
slug: skill-update
version: 1.0.3
description: >-
  Updates installed agent skills safely: version check, diff preview, backup, approval,
  data migration, and rollback. Use when updating or upgrading a skill, checking for newer
  versions, previewing what changed before applying, when a skill breaks, misbehaves, or
  loses data right after an update, when saved data or config must migrate across a version
  bump, when local edits to an installed skill would collide with the new version, or when
  bringing every skill or every agent's copy current. Not for installing new skills
  (skill-finder) or publishing skills you own (skill-publish).
homepage: https://clawic.com/skills/skill-update
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🔄
    displayName: Skill Update
    configPaths:
    - ~/Clawic/data/skill-update/
---

Updates installed skills safely: preview every change, back up before applying, migrate data only on approval, roll back on failure. Mode: act-as — it executes the update directly, never advises from the sideline. Backups, the update log, and config live under `~/Clawic/data/skill-update/`. If you have data at an old location (`~/skill-update/` or `~/clawic/skill-update/`), move it to `~/Clawic/data/skill-update/`.

## When To Use

- User asks to update, upgrade, or version-check an installed skill.
- A skill misbehaves, stops triggering, or loses data right after an update — diagnose and roll back.
- A major bump is pending: preview breaking changes and migrate saved data before applying.
- The installed copy was hand-edited, so a straight update would overwrite the user's changes.
- Bringing everything current: `update --all`, or the same skill installed across several agents.
- User mentions a skill that has a newer published version — flag it once, proactively.
- Not for: publishing or versioning a skill you own (owner-side act → `skill-publish`); discovering or installing skills you don't have yet (→ `skill-finder`).

How updates break things (each maps to a preview check):
- Renamed/moved files → user data and references orphaned.
- Removed or rewritten instruction sections → the agent silently stops doing something the user relies on.
- New setup requirements (binary, env var, account) → skill half-works until configured.
- Changed data formats → previously saved state unreadable.
- Overwritten local edits → the user's customizations vanish without an error anywhere.

## Quick Reference

| Situation | Play |
|---|---|
| Single skill, patch or minor pending | Diff, classified summary, apply on explicit yes (→ Update Flow) |
| Major pending | Full preview + migration check → `preview.md`; never propose-and-apply in the same turn |
| Skill broke right after an update | Symptom→cause chains and restore procedure → `rollback.md` |
| Installed copy was hand-edited | Detect and merge before updating → `local-changes.md` |
| Same skill in more than one agent | Inventory every copy before touching any → `multi-agent.md` |
| "Update everything" | Patches/minors batched, majors one by one → `batch.md` |
| Data format changed between versions | Read the real data, map, apply on approval → `migrate.md` |
| Diff looks suspicious (new network calls, broadened file access) | Security screen → `preview.md`; do not apply, report to the user |
| No version history, or delta unclear | Treat as major |
| Anything else | Get the text diff first — it is the ground truth every other call rests on |

Depth on demand: `preview.md` diff procedure, impact classes, security screen, recommend/defer call · `migrate.md` data migration patterns, script template, failure handling · `rollback.md` post-update breakage diagnosis and restore · `local-changes.md` detecting and preserving user edits · `batch.md` multi-skill updates and mid-batch failure · `multi-agent.md` version skew across agent installs.

Check installed against published:
```bash
npx clawic list              # installed skills + versions
npx clawic show <slug>       # latest published version
```
Catalog page mirrors the same version info: `https://clawic.com/skills/<slug>`.

Version delta sets the default stance (semver semantics):

| Delta | Assume | Action |
|---|---|---|
| Patch (1.2.3 → 1.2.4) | Fixes only | Quick diff, apply on approval |
| Minor (1.2 → 1.3) | Additions | Diff; check modified sections, not just added ones |
| Major (1.x → 2.0) | Breaking | Full preview + migration check; never propose-and-apply in the same turn |
| Any delta, user mid-project on this skill | Risky timing | Mention once, defer until the work ships |
| Else (delta unclear, or no version history) | Unknown risk | Treat as major |

## Core Rules

1. A skill is behavior-as-text: every text diff is a behavior diff. Never apply one the user hasn't seen and approved.
2. The update order is load-bearing — check → detect local edits → preview → explain → confirm → backup → update → verify (→ Update Flow). Back up before applying; verify before deleting anything.
3. Explicit "yes" only. Silence, "hmm", or a topic change is not consent. Approval for skill A is never approval for `update --all`.
4. Diff even patch bumps. Semver is the publisher's claim, not a guarantee: a "patch" that rewrites an instruction section is a behavior change wearing a small number.
5. Verify with one real task run against the updated skill, not a file listing. Files present ≠ skill works.
6. Back up before ANY update. Retention: keep ≥`backup_retention_days` AND until the user confirms the new version works — whichever is later. Breakage surfaces on next real use, not at install.
7. A migration that fails mid-way stops, reports, and restores — never leave partial state.
8. Any breaking-change signal leads the summary and requires explicit approval (signals → Preview Before Update).
9. The diff is ground truth; the changelog is the publisher's summary. Read the changelog to set expectations, never to skip the diff.

## Update Flow

Order is load-bearing: backup before apply, verify before deleting anything.

1. **Check** — compare installed vs published version; inventory every install location (`multi-agent.md` if more than one).
2. **Detect local edits** — installed copy vs its published original; edits found → `local-changes.md` before anything else.
3. **Preview** — full diff, classified by impact, security-screened (`preview.md`).
4. **Explain** — breaking changes first, in the user's workflow terms.
5. **Confirm** — explicit yes (Core Rule 3).
6. **Backup** — copy current state before touching anything (→ Backup & Update Log).
7. **Update** — apply the new version to every inventoried copy.
8. **Verify** — run one real task with the updated skill.

## Preview Before Update

Never apply without showing impact. For each changed file answer: what changed, does the user's workflow touch it, is migration needed. Procedure, impact classes, and the security screen of the diff: `preview.md`.

Breaking-change signals — any one present means it leads the summary and requires explicit approval:
- File or folder renamed, moved, or deleted.
- Instruction section removed or rewritten (breaking even with zero structural change).
- New required setup step.
- Format change in anything the skill saves.
- Local edits on the installed copy that the update would overwrite.

Present changes in a digestible summary, breaking items first:

> "Skill X has v2.0.0 available. Changes:
>
> **⚠️ Breaking:** Config now in `config.md` (was in SKILL.md)
> **Added:** New `templates/` folder with examples
> **Removed:** Old `legacy.md` no longer needed
>
> **Migration needed:** Your saved preferences need to move. I can help migrate. Proceed?"

Each skill with a pending major gets its own preview.

## Applying the Update

```bash
npx clawic update <slug>   # update one skill
npx clawic update --all    # update every installed skill with a newer version
```

`update` is the consumer-side pull — it fetches what the owner already published; publishing a new version is the owner's act, a different operation entirely (→ `skill-publish`). Reach for `--all` only when the user asked for all AND no pending update is a major (majors go one by one; sequencing and mid-batch failure → `batch.md`).

**Proactive notification:** when the user mentions a skill that has a newer version, say so once (unless `proactive_notify` is off or the skill is in `pinned_skills`). Don't re-raise it in the same session.

## Backup & Update Log

Before ANY update:
1. Copy the current skill folder to `~/Clawic/data/skill-update/backups/<slug>-<version>-<timestamp>/`.
2. If the skill being updated declares a data folder (`~/Clawic/data/<slug>/`), back that up under the same timestamped folder — the update itself never touches it, but a migration might.
3. State the backup path in your response.
4. Append one line to `~/Clawic/data/skill-update/update-log.md`: date · slug · old→new version · backup path · agents updated. The log is what lets you answer "what version was I on last week?" after the session that updated it is long gone.
5. If the update fails → offer restore immediately.

## Handling Migrations

When a data format changes:
1. Read the user's actual current data first — never map from an assumed format.
2. Explain what moves and what defaults get added.
3. Execute only with approval.
4. Verify migrated data works.

Patterns (rename, structure change, folder move, learned data), script template, and failure handling: `migrate.md`.

## Rollback

Restore = copy the backup folder back over the installed skill — and its data folder from the same timestamp if a migration ran. Offer it unprompted the moment the user reports the skill misbehaving after an update:

```
"Something's not working? I have a backup from before the update.
Want me to restore skill X to v1.2.3?"
```

Diagnosis first when the cause is unclear (symptom→cause chains, restore verification, what to do when no backup exists): `rollback.md`.

## Output Gates

Before applying any update, verify:

- Explicit yes from the user for THIS skill, in this session?
- Diff actually read — not just the changelog or the version number?
- Local edits checked (installed copy vs its published original)?
- Backup of the skill folder AND its data folder exists, path stated to the user?
- Every install location inventoried, not just the first one found?

Before reporting success: one real task run against the updated skill?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/skill-update/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| backup_retention_days | number (days, ≥1) | 7 | Floor for deleting backups (Core Rule 6); "until the user confirms it works" still applies on top |
| proactive_notify | bool | true | Whether to flag a newer version once when the user mentions an installed skill |
| pinned_skills | list (slugs) | none | Excluded from proactive flags and `update --all`; updated only when the user names the skill explicitly |
| preview_detail | summary \| full-diff | summary | Previews show the classified summary, or the raw diff inline for users who want to read every hunk |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:
- **Tooling**: where skills live (project vs global installs, which agents) — affects the Check step's inventory and `multi-agent.md`
- **Safety posture**: how majors are sequenced and how much confirmation ceremony — never below Core Rule 3's explicit-yes floor; affects Update Flow and `batch.md`
- **Cadence**: when version sweeps happen (only on request vs at session start) — affects Check and proactive notification
- **Conventions**: how previews and batch reports are worded (terse vs annotated) — affects Preview Before Update and `batch.md` reporting

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Trusting a patch bump | For text skills any edit changes behavior | Diff every update regardless of number |
| Verifying by file listing | Files present ≠ skill works | Run one real task with the updated skill |
| `update --all` after one yes | Consent covered one skill | Per-skill preview for every pending major (`batch.md`) |
| Deleting backup right after update | Breakage shows on next use, not at install | Hold ≥`backup_retention_days` and until user confirms |
| Flagging moved text as removed | Diff shows delete + add; content just relocated | Search the new version for "deleted" text before calling it breaking |
| Overwriting a hand-edited install | The user's customizations vanish with no error anywhere | Detect local edits before applying (`local-changes.md`) |
| Restoring the skill folder but not its data | A migration already rewrote the data; old skill + new data = both broken | Restore skill and data folder from the same backup timestamp (`rollback.md`) |
| Updating only the first copy found | The same skill installed in other agents keeps loading the stale version | Inventory all install locations first (`multi-agent.md`) |
| Reading the changelog as the diff | It is the publisher's summary, written to be short | Changelog sets expectations; the diff is ground truth (Core Rule 9) |

## Where Experts Disagree

- **Update promptly vs pin and batch.** Prompt updates minimize drift from published fixes; pinning batches the review cost into scheduled sweeps. The boundary is criticality, not taste: skills inside daily load-bearing workflows get pinned (`pinned_skills`) and reviewed deliberately; peripheral skills update as bumps appear.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/skill-update (install if the user confirms):
- `skill-finder` - Find, compare, and install skills you don't have yet, before there is anything to update.
- `skill-publish` - The owner-side act `update` pulls from: sanitize, version, and publish a skill you own.
- `skill-manager` - Broader install/remove/list lifecycle and unused-skill cleanup beyond one update.

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/skill-update.
