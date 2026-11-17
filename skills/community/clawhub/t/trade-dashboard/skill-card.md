## Description:

Trade Dashboard helps agents produce B2B foreign-trade analytics dashboards for conversion funnels, ROI tracking, outreach performance, model routing, and feedback analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External business and operations users can use this skill to ask an agent for a compact dashboard-style report on foreign-trade prospecting performance, including funnel movement, ROI, outreach results, and trend signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes automatic feedback that can alter trade-hunter search behavior or trade-qualifier scoring weights without clearly defining approval, scope, or rollback.

Mitigation: Require explicit human approval before feedback changes another trade skill, document the affected data and scoring changes, and keep a rollback path for search and scoring settings.

Risk: Dashboard outputs may influence business decisions using incomplete or stale prospecting, outreach, cost, or revenue data.

Mitigation: Review source data freshness and reconcile key metrics before using the dashboard for spend, targeting, or sales decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/skills/trade-dashboard)
- [Publisher Profile](https://clawhub.ai/user/wangm-a3)
- [Related Skill: trade-hunter](https://github.com/cloud-travel-skills/trade-hunter)
- [Related Skill: trade-qualifier](https://github.com/cloud-travel-skills/trade-qualifier)
- [Related Skill: trade-closer](https://github.com/cloud-travel-skills/trade-closer)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown or HTML-oriented dashboard guidance with chart and metric descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference ECharts, Leaflet, and curl where available; no credential variables were detected in the release evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
