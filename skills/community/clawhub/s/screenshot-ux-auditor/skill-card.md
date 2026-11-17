## Description:

Turn app screenshots into structured UX, copywriting, and conversion audits with issue severity and recommended fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, product teams, and developers use this skill to audit app screenshots for UX, copywriting, conversion, and accessibility issues, then produce prioritized fixes and issue logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV issue logs generated from untrusted issue text may be unsafe to open in spreadsheet software if formula-prefixed cells are not sanitized.

Mitigation: Treat issue JSON as untrusted and sanitize formula-prefixed cells before spreadsheet use, or review the CSV in a plain-text editor.

Risk: Screenshot audits can produce incomplete or misleading recommendations when product goals, target users, platform, or benchmark context is missing.

Mitigation: State assumptions clearly and ask only for the minimum missing context before finalizing recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/screenshot-ux-auditor)
- [UX Heuristics Checklist](resources/heuristics-checklist.md)
- [Example Prompt](examples/example-prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, CSV, guidance]

**Output Format:** [Markdown audit summaries with optional CSV issue logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include prioritized issue lists and before/after prompt suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and user changelog mention 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
