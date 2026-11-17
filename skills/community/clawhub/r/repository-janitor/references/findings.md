# Findings and reports

Classify evidence, not presumed intent:
- Active work: an observed process uses the checkout.
- Recent WIP: latest available dirty-path mtime is less than 24 hours old, without an observed process.
- Older WIP with no identified owner: older than 24 hours; investigate ownership or handoff, never infer disposal permission.
- Unknown age: deletions or unavailable metadata.
- Known automation or deliberate quarantine: only with documentation; the executor does not infer these owners automatically.

The state lifecycle is `new`, `persistent`, `worsened`, or `resolved`. A failed scope does not resolve previous findings. Condensed reports may omit details while retaining findings in private state. Changed-file contents and raw subprocess errors are not stored. Private state can contain approved worktree paths, commit IDs, counts, and timestamps; do not publish it.

Remote protection checks require a successful current fetch. An absent upstream does not by itself mean data loss. Test incorporation in the configured base and containment in known fetched remote refs. Those observations do not guarantee a permanent remote backup.

A draft PR, missing approval, many comments, cache size, or a free persistent lock is not a defect. Unknown GitHub state stays unknown. A present empty SQLite placeholder is not the operational database unless the effective configuration selects it.

Report:
1. Time, mode, inspected repositories, open findings, incomplete checks.
2. New, worsened, persistent, and confirmed resolved findings with evidence.
3. Coverage failures and where to resume.
4. Exact targets and requested human actions when needed.
5. Explicit statement that no cleanup, commit, push, or deployment was performed.

Say “No decision needed today.” only when there are no open findings and no incomplete checks. Do not describe execution success as proof that every repository is clean.
