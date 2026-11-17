## Description:

Accepts software requirements text or documents, breaks them into work items, estimates effort across analysis, design, frontend, backend, algorithm, and testing dimensions, and produces Excel evaluation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinqiu193](https://clawhub.ai/user/jinqiu193)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and project planners use this skill to turn software requirements into a structured effort estimate with work breakdowns, risk notes, dependencies, schedule views, and cost estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated spreadsheets may include inaccurate estimates, misleading assumptions, or content derived from untrusted requirements text.

Mitigation: Review and sanitize generated workbooks before sharing or opening them in a sensitive environment.

Risk: The report defaults include Chinese labels, China holiday assumptions, and RMB cost estimates that may not fit every team or region.

Mitigation: Adjust labels, calendars, rates, currency, and cost assumptions before using the report for planning or budgeting.

Risk: Very large or poorly scoped requirements can produce oversized or low-quality estimates.

Mitigation: Keep inputs reasonably sized and split large projects into smaller estimation runs.

## Reference(s):

- [Software Development Work Estimation Guide](references/evaluation-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/jinqiu193/skills/work-estimation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance and generated Excel workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Excel reports include overview, dimension details, Gantt chart, key risks, coordination, and cost-estimation sheets.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
