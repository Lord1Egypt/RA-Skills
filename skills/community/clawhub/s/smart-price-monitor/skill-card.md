## Description:

Monitors product prices, stock levels, and market data across websites and APIs, with alerts and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure price monitors, compare retailer prices, record price history, generate alerts, and create reports or local dashboards for products, competitor pricing, and market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious because broad price monitoring and bundled scripts create local-file and dashboard-script risks.

Mitigation: Review before installing; use only for user-approved price or stock monitoring, avoid sensitive or authenticated pages, and keep dashboards local unless escaping issues are fixed.

Risk: Dashboard content can include monitor names or source data that may be untrusted.

Mitigation: Do not generate dashboards from untrusted monitor data until HTML and script escaping are added.

Risk: Monitor IDs are used to locate local history files.

Mitigation: Use only trusted monitor IDs and add path validation before accepting monitor IDs from untrusted input.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell command examples, generated JSON data, Markdown reports, and HTML dashboards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local price-monitor-data files for monitor configuration, price history, reports, dashboards, and alert logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
