# Rollback — When a Skill Breaks After an Update

Diagnose first when the cause is unclear; restore first when the user just wants the old behavior back. Both paths below.

## Symptom → Cause

Work top-down; each row is a check, not a guess.

| Symptom after update | Likely cause | Check |
|---|---|---|
| Skill stopped triggering at all | Description rewritten — the trigger surface changed | Diff the frontmatter `description` old vs new |
| Skill triggers but behaves differently | Instruction section rewritten or removed | Diff the section covering the changed behavior; search the new version for the old wording |
| Skill errors about a missing binary, env var, or account | New setup requirement introduced | New version's requirements vs what the machine has; a setup step, not a rollback, may be the fix |
| Skill can't read its saved data | Data format changed and migration didn't run (or ran wrong) | Open the data folder; compare its shape against what the new version expects (`migrate.md`) |
| Skill reads data but output lost personalization | Migration dropped or mis-mapped learned values | Compare data folder against the backup copy field by field |
| References inside the skill 404 (file not found) | Files renamed or moved by the update | List old vs new folder; a structural change slipped through preview |
| Only one agent shows the problem | That agent has a different copy or version | `multi-agent.md` — inventory every install location |
| Else | Unknown — treat as full breakage | Restore, then re-run the preview on the diff you missed |

A setup-requirement failure is the one row where rolling back is usually the wrong move: installing the requirement gets the user the new version they wanted.

## Restore Procedure

1. Locate the backup: `~/Clawic/data/skill-update/backups/<slug>-<version>-<timestamp>/` — the update log (`~/Clawic/data/skill-update/update-log.md`) maps dates to versions and paths when several backups exist.
2. Confirm with the user which version to restore (the log answers "what was I on when it worked?").
3. Copy the backed-up skill folder over the installed one — every install location, not just the first (`multi-agent.md`).
4. **If a migration ran during the update, restore the data folder from the same timestamp.** Old skill + migrated data is a second breakage, not a fix.
5. Verify: run the task that surfaced the problem. Broken → the update wasn't the cause; put the new version back and keep diagnosing.
6. Log the rollback in `update-log.md` (date · slug · restored version · reason).

## After a Successful Rollback

- Add the skill to `pinned_skills` if the user wants it held; otherwise note the failing version so the next sweep doesn't re-propose it blind.
- Report upstream in the user's name only if the user agrees: the skill's catalog page (`https://clawic.com/skills/<slug>`) is where feedback lands.
- When a fixed release appears, preview it against the version that worked, not against the one that broke.

## No Backup Exists

The update predates this skill's involvement, or retention expired:

1. Reinstall the last known-good version if the registry serves it; the catalog page lists version history.
2. If only latest is served: reconstruct what broke from the diff between the two published versions and patch the local copy as a stopgap — flag it as a local edit (`local-changes.md`) so the next update doesn't silently erase it.
3. Data loss with no backup and no export is unrecoverable — say so plainly rather than improvising a partial reconstruction that looks whole.

## Rolling Back a Migration Alone

Skill version is fine but the migrated data is wrong:

1. Restore only the data folder from the backup timestamp.
2. Re-run the migration with the mapping corrected (`migrate.md`, Handling Failures).
3. Verify with a task that exercises the migrated values — file counts don't catch semantic mapping errors.
