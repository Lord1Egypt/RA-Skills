---
name: "trace-configuration-file-migrations"
description: "Trace removed or relocated config files across source, releases, migration code, and local state without mistaking relocation for deletion."
---

# Trace configuration-file migrations

Use when a config, workspace, or instruction file disappears after an upgrade and the task is to explain what changed, when, why, and whether local data survived.

## Procedure

1. Inspect current local state first.
   - Test whether the old file exists.
   - Locate the replacement section or file.
   - Record modification times for the replacement and any migration backup.
   - Hash the backup when integrity matters.

2. Establish upstream intent.
   - Find the introducing PR or commit.
   - Inspect its changed-file list before opening large diffs.
   - Read the PR description and only the relevant source, template, and documentation files.

3. Establish release timing.
   - Read tag name and publication time from release metadata.
   - Do not rely on a truncated release body as proof.
   - Distinguish merge date, first packaged prerelease, and later migration refinements.

4. Read migration code, not only release notes.
   - Identify the source file, destination, backup/archive path, deletion point, and failure ordering.
   - Check how empty or stock templates differ from customized content.
   - Check whether runtime retains a fallback reader for the legacy file.
   - Check migration scope: workspace root, multiple agents, or nested directories.

5. Compare docs and templates with implementation.
   - Confirm the new canonical location and whether it controls behavior or merely supplies model guidance.
   - Treat source as decisive for edge cases; use docs for the supported contract.

6. Audit stale custom guidance.
   - Search active instruction files for references to the legacy path.
   - Inspect rewrite tables when migration updates known wording.
   - Expect exact-match rewrites to miss custom paraphrases; report those separately from data migration.

7. Report in this order:
   - conclusion: deleted, relocated, merged, or unsupported;
   - timeline: merge, release, later refinements;
   - rationale;
   - migration behavior and recovery path;
   - verified local outcome;
   - remaining stale references or out-of-scope nested files.

## Pitfalls

- File absence alone does not prove data loss.
- Release notes alone do not establish migration ordering or rollback behavior.
- A backup alone does not prove destination content was written.
- Successful root migration does not prove nested files were migrated.
- Automated wording rewrites may cover stock text but leave customized guidance contradictory.
- Large API responses can truncate the only relevant evidence; narrow by changed path or metadata.

## Verification

Verify all applicable invariants:

- the legacy root file is absent or intentionally retained;
- migrated content appears at the documented destination;
- the backup exists and its hash is stable;
- timestamps align with the migration event;
- current docs name the destination;
- migration source confirms archive/write/delete ordering;
- active instructions contain no unreported legacy references.

If any invariant cannot be checked, label it unknown rather than inferring success.
