## Description:

Aggregates monthly content, calendar, channel, product-line, and knowledge-base data into a performance report and next-cycle recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Brand-side content and marketing teams use this skill to review monthly publishing output, compare the content calendar with actual results, and prepare evidence-based adjustments for the next cycle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because three local references in SKILL.md could not be matched to bundled files.

Mitigation: Check those referenced paths and review their contents before installing or relying on them.

Risk: Incomplete or platform-reported performance data could lead to misleading conclusions.

Mitigation: Mark gaps as DATA_MISSING, preserve the required source caveat for platform metrics, and have a person review recommendations before acting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/haiyangchenbj/skills/tcms-performance-analyst)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown monthly report with tables, findings, and next-cycle recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves to reports/YYYY-MM-monthly-report.md; marks unavailable performance data as DATA_MISSING and requires human confirmation before acting on recommendations.]

## Skill Version(s):

1.1.9 (source: frontmatter; server release: 1.1.9)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
