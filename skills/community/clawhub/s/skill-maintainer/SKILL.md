---
name: clawhub-skill-maintainer
description: Maintain a large ClawHub skill portfolio with a quality-first and AI-assisted upgrade lens. Use when the user wants to audit published skills, find high-quality skills worth maintaining, analyze downloads/installs/stars/comments, detect stale or partial data, generate safe upgrade/maintenance queues, prepare AI maintainer prompts, handle bulk-publishing account risk, or build/update a ClawHub skill dashboard.
---

# Skill Maintainer

Use this skill to audit and maintain a ClawHub publisher portfolio, especially when the maintainer needs to identify which skills deserve ongoing public investment.

## Operating Principle

Preserve quality first, analyze cleanup second, ask for approval third, execute last.

The default output is an evidence-backed maintenance queue. Prefer skills with real user signal, clear public utility, complete metadata, source provenance, version history, recent updates, and growth momentum. Treat cleanup as secondary and only act on it when the data quality status is `ok`.

Do not run public visibility changes, merge commands, delete commands, or publish updates unless the user explicitly approves the specific batch or operation.

## Core Workflow

1. Refresh portfolio data:

   ```bash
   python3 scripts/update_all.py --handle <clawhub-handle>
   ```

   To restart the trend history from a clean baseline while preserving old snapshots in an archive:

   ```bash
   python3 scripts/update_all.py --handle <clawhub-handle> --baseline
   ```

2. Review generated artifacts:

   - Dashboard: `reports/index.html`
   - Scored analysis: `data/processed/<handle>_skill_analysis.csv`
   - Summary and quality queue: `data/processed/<handle>_summary.json`
   - Low-signal triage: `data/processed/<handle>_low_signal_triage.csv`
   - Data unavailable queue: `data/processed/<handle>_data_unavailable.csv`
   - Latest snapshot: `data/snapshots/<handle>/latest.json`
   - Growth deltas: `data/processed/<handle>_skill_growth.csv`
   - Trend summary: `data/processed/<handle>_trend_summary.json`
   - General approval board: `reports/approval_packets/<handle>_approval_board.md`
   - Bulk cleanup board: `reports/bulk_cleanup/<handle>_bulk_approval_board.md`
   - AI upgrade plan: `reports/auto_upgrade/latest/report.md`
   - AI maintainer prompts: `reports/auto_upgrade/latest/agent_prompts/`

3. Explain the recommendation to the user in business terms:

   - which skills are worth maintaining first
   - which quality signals explain that priority
   - what should stay public
   - what should be upgraded
   - what cleanup was suppressed because the data is partial
   - which skills had failed detail fetches and therefore get no decision today
   - what should be hidden or merged only after explicit cleanup review
   - what should be monitored

4. Ask the user to approve one batch at a time using the exact approval phrase shown in the generated approval board.

5. After approval, execute only the approved commands and report the outcome.

## AI Maintenance Candidate Plan

Use `scripts/auto_upgrade.py` when the portfolio is too large to maintain manually. The loop selects the next high-quality skills worth reviewing, inspects local source packages, writes an evidence report, and creates one prompt per candidate for an AI maintainer. It is a candidate-plan workflow, not an automatic publish workflow.

Plan-only mode:

```bash
python3 scripts/auto_upgrade.py --handle <clawhub-handle> --limit 5
```

Integrated refresh plus plan:

```bash
python3 scripts/update_all.py --handle <clawhub-handle> --auto-upgrade-plan --auto-upgrade-limit 5
```

Fetch missing sources before planning:

```bash
python3 scripts/auto_upgrade.py --handle <clawhub-handle> --limit 5 --fetch-source
```

Missing source lookup order is GitHub first, local roots second, and ClawHub install/download fallback last. If GitHub or ClawHub reports a rate limit, stop instead of retrying and run the source fetch later.

Conservative deterministic edits:

```bash
python3 scripts/auto_upgrade.py --handle <clawhub-handle> --limit 5 --apply-safe
```

`--apply-safe` is intentionally narrow and must not be used in the daily cron. It only appends missing example prompts or sensitive-domain safety boundaries to local `SKILL.md` files when the package has no forbidden files and a small file surface. It never publishes, hides, merges, deletes, renames, or changes ownership.

For each generated prompt in `reports/auto_upgrade/latest/agent_prompts/`, run an AI maintainer with these gates:

- preserve the original public contract and slug
- keep edits small and reviewable
- look for source on GitHub first; if unavailable, use ClawHub install/download as the fallback
- add trigger clarity, examples, workflow, validation checks, tags, bilingual search terms, and safety boundaries where useful
- run validation and dry-run publish before any real publish
- stop on rate limits, auth errors, data-quality warnings, or missing source
- require explicit user approval before publishing

## Quality Maintenance Lens

Start with `quality_maintenance_queue` in `data/processed/<handle>_summary.json` and `reports/action_plans/<handle>_quality_maintenance_plan.csv`.

Strong quality signals include:

- installs, stars, comments, or sustained downloads
- public-utility categories such as developer, data, knowledge, automation, or shopping
- rich summary, useful tags, changelog, source repo/path metadata
- multiple versions or recent updates
- positive growth in downloads or installs since the previous snapshot

When a skill has quality signal, recommend concrete upgrades before any visibility cleanup: improve `SKILL.md`, examples, bilingual search terms, tags, changelog, source metadata, tests, and release notes.

## Data Quality Guardrails

Treat the run as `partial` when profile totals and processed totals diverge, many detail requests fail, many rows are unexpectedly zero-download, the report falls back to cache, or deltas are negative. In partial mode:

- keep quality maintenance, upgrade, and monitor queues
- move failed skill-detail fetches into `data_unavailable`
- exclude `data_unavailable` skills from keep, upgrade, hide, merge, delete, monitor, bulk-cleanup, and AI maintenance candidate decisions for that day
- suppress hide, merge, delete, and bulk-cleanup approval batches
- tell the user which warning caused suppression
- refresh data later instead of retrying aggressively during rate limits

## Account-Risk Cleanup Lens

When the user says bulk publishing caused an account review, start with `scripts/plan_bulk_cleanup.py` outputs.

The strongest bulk-risk pattern is:

- low or plausible-low signal
- single version
- zero installs
- zero stars
- zero comments

Recommended default policy:

- Phase 1: hide low-download skills matching the strongest risk pattern only when data quality is `ok`.
- Phase 2: spot-check, then hide moderate-download skills matching the same pattern.
- Phase 3: upgrade within a short deadline or hide only after the upgrade decision is reviewed.
- Phase 4: merge or hide repeated families only after target review.
- Do not delete by default.

Prefer hide before delete because `clawhub hide` is reversible with `clawhub unhide <slug>`.

## Approval And Execution

Generated command files are intentionally commented out. Treat them as previews, not scripts to run blindly.

Safe command forms after explicit approval:

```bash
clawhub hide <slug> --yes
clawhub unhide <slug> --yes
clawhub inspect <slug> --files
clawhub publish <path>
clawhub skill rescan <slug>
```

Higher-risk command form:

```bash
clawhub skill merge <source-slug> <target-slug> --yes
```

Merge is higher risk because no obvious `unmerge` command is available. Review the canonical target before approving merge batches.

## Responding To Users

For skills with comments or reported issues:

1. Inspect the skill with `clawhub inspect <slug> --files`.
2. Find or reconstruct the local source.
3. Reproduce or understand the issue.
4. Patch the source skill.
5. Publish the update with `clawhub publish <path>`.
6. Rescan if needed with `clawhub skill rescan <slug>`.
7. Reply with what changed, the new version, and any remaining limitation.

If comment bodies are unavailable through the API or CLI, say that only comment counts are visible and ask for a browser workflow or comment export.

## Dashboard Maintenance

The dashboard is a local generated artifact:

```bash
python3 scripts/update_all.py --handle <clawhub-handle>
```

Open `reports/index.html` after refresh. It is safe to regenerate; it should not be packaged into the skill.

Each full refresh writes a timestamped snapshot under `data/snapshots/<handle>/`. When at least two snapshots exist, the dashboard shows the top 20 skills by new downloads and new installs since the previous snapshot. Use those growth charts to decide which skills are becoming popular and deserve priority maintenance.

Use `--baseline` when the account has materially changed and the next run should become the first active trend baseline. Existing active snapshots are archived under `data/snapshots/<handle>/archive/` instead of deleted.

## Safety Rules

- Never execute hide, merge, delete, or publish actions merely because a report recommends them.
- Never execute hide, merge, or delete actions when `data_quality.status` is `partial`.
- Never make maintenance, cleanup, or publish decisions from rows marked `data_unavailable`; retry collection later.
- Never batch-hide skills with installs, stars, comments, or strong usage without manual review.
- Do not treat zero downloads as evidence when detail fetches failed or profile totals disagree with processed totals.
- Use hide/private-style cleanup before deletion.
- Treat generated shell files as commented approval previews.
- Keep generated data, caches, logs, and reports out of the published skill package.
- If network or authentication fails, work from existing snapshots and clearly state the limitation.
