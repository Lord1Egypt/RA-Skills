## Description:

Reads local WorkBuddy session data to summarize token and credit usage and create an offline dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[circleruler](https://clawhub.ai/user/circleruler)

### License/Terms of Use:

MIT

## Use Case:

WorkBuddy users use this skill to review local token and credit consumption by day, model, and session, and generate terminal, JSON, or offline HTML reports. Figures are local estimates, not official billing records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Specially crafted session titles could run web scripts when the generated HTML dashboard is opened.

Mitigation: Use --json until database-derived text is safely escaped in the HTML dashboard.

Risk: Reports contain private session titles and usage figures that are local estimates, not official billing records.

Mitigation: Share reports carefully and treat their figures as estimates rather than official billing data.

## Reference(s):

- [Server-resolved source repository](https://github.com/CircleRuler/wb-usage-dashboard)
- [ClawHub skill release](https://clawhub.ai/circleruler/skills/wb-usage-dashboard)
- [Publisher profile](https://clawhub.ai/user/circleruler)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML file]

**Output Format:** [Terminal summary, machine-readable JSON, or standalone HTML dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports contain local usage estimates and may include private session titles; figures may differ from official billing.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
