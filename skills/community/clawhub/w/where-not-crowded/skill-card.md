## Description:

去哪不挤 helps users decide where to travel during Chinese holidays by comparing crowded default destinations with less crowded, higher-value alternatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyikoi](https://clawhub.ai/user/keyikoi)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill before holiday travel to get a direct decision report that challenges a default popular route and recommends a main alternative plus near and far backups with crowd, cost, timing, and budget context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may replace previous latest Markdown or HTML outputs in the selected output directory.

Mitigation: Run the skill in a dedicated output directory or move earlier reports before generating a new latest report.

Risk: Travel recommendations and price ranges may be incomplete or stale for a specific holiday, route, or budget.

Mitigation: Treat the report as decision support and verify current transport, lodging, visa, and booking details before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keyikoi/skills/where-not-crowded)
- [Report template](artifact/references/report_template.md)
- [Example report](artifact/references/example_report.md)
- [Widget data spec](artifact/references/widget_data_spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Code, Guidance]

**Output Format:** [Markdown report plus local Markdown and HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generation script can also emit a JSON report payload when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
