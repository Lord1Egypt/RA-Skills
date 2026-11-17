---
name: ci-tools-digest
description: Produce an English CI Tools digest for a complete calendar month, with release evidence, migration notes and clearly separated open work. Use for monthly reporting or an explicitly requested month.
metadata: { "openclaw": { "requires": { "bins": ["glab", "python3"] }, "primaryEnv": "GITLAB_TOKEN" } }
---

# CI Tools monthly digest

1. Run `python3 {baseDir}/scripts/collect.py`. The default is the previous
   complete **UTC calendar month**, not the previous 28 days. For a rerun, pass
   `--month YYYY-MM`. Stop on API, pagination or timestamp errors; incomplete
   collection must never be presented as complete.
2. Use the returned `month`, `window_start_utc`, `window_end_utc` and counts.
   The start is inclusive and the next month's start is exclusive. Date releases
   by `released_at` and merged MRs by `merged_at`, not commit dates or the time
   the digest runs. Inspect representative MR descriptions and GitLab sources
   before making behavior or migration claims. A tag name alone proves no
   functionality. Explicit `--allow-incomplete` previews must say **Month to
   date**, include `collected_through_utc`, and never claim a complete month.
3. Write the entire digest in **English**, including headings and **Not yet
   released**. Include the calendar period and timezone, release/MR counts,
   3–5 substantive themes, concrete migration points and direct source links.
   Open MRs are a separately dated current snapshot, not shipped changes or
   part of the monthly merged count. If published release and merge evidence
   differ, describe that distinction instead of calling every merge released.
4. Publish through an assigned MR in `xrow-public/ci-tools` at the collector's
   `output_path`: `docs/digest/digest-yyyy-mm.md`. Follow the GitLab Agent access,
   assignment, source and review gates. Search for an existing open MR for that
   month's path/branch before creating one. Reruns replace that month's report
   in the existing MR or update the existing file in a new MR after merge;
   never append overlapping rolling windows or create a duplicate monthly MR.
   Preserve other months. The checked diff must contain one calendar report.
5. Verify the rendered page, period, counts, English text and all source links.
   Return the MR link and whether CI/review is pending. Do not push to the
   protected default branch or merge merely because a digest was generated.
   Scheduled delivery handles the final reply; do not send a separate message
   from inside the run.

The skill is maintained in `xrow-public/ci-tools/skills/ci-tools-digest` and is
included in the OpenClaw image from that source, not a profile-local duplicate.
The default monthly schedule is in `{baseDir}/AUTOMATIONS.json`. Before changing
an installed job, list all automations including disabled ones and reuse either
`profile:ci-tools-digest` or the legacy `profile:ci-tools`/`ci-tools` skill prompt.
Do not create a second job, enable a disabled job, or overwrite a user-edited
schedule during installation or rename migration.
