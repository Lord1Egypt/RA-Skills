---
name: Release Guard
slug: release-guard
version: 1.0.1
description: Run narrow, local pre-publish checks for an OpenClaw skill folder without dynamic shell evaluation, network access, publishing, or destructive actions.
---

# Release Guard

Use this skill before publishing an OpenClaw skill. It performs a narrow, local readiness review of a selected skill folder and returns a checklist-style report.

This skill does **not** publish, upload, delete, modify, install dependencies, or contact external services. It only reads the chosen folder and reports common release risks.

## Checks covered

- `SKILL.md` exists.
- The file count is small enough for a reviewable ClawHub package.
- Obvious unrelated workspace folders are absent.
- Documentation is mostly English.
- Basic secret-like terms are reported for manual review.
- Shell scripts are checked for risky `eval` usage.

## Checks not covered

Release Guard is not a full security audit. It does not guarantee that a skill is safe, does not run dependency vulnerability scans, and does not replace human review.

## Safe usage

```bash
bash scripts/release-check.sh /path/to/skill-folder
```

The path is handled as data and is always quoted. The script avoids dynamic shell evaluation.

## Output

Return a compact report with:

- PASS/WARN/FAIL lines
- a final status
- specific files to review
- recommended next steps before publishing

## Human review rule

If the script reports secrets, unrelated folders, broad execution claims, or risky shell patterns, stop and review manually before publishing.
