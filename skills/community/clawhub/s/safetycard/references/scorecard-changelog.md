# Scorecard changelog

Every rule change bumps `scorecard_version`. Entries carry the version they were scored under; the website flags entries older than the current catalog. When a change can move ratings, rerun every existing scorecard under the new version and log rating changes in each `reaudit_log`.

## 0.9
First public release. All published scores are labelled 0.9.

- **Safest setup (output only, 2026-10-10, skill 0.9.1).** Every review now carries a `safe_setup` section, rendered as "Safest setup" after the headline: how to run the agent most safely, written from the review's own findings (SKILL.md step 6). It changes no criterion, level, cap, weight or score, so `scorecard_version` stays 0.9 and published entries were backfilled without rescoring.
