## Description:

Generates SQL query result and chart reports with tables, matrices, slicers, multi-format exports, and statistics-driven insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moniq888](https://clawhub.ai/user/moniq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and business teams use this skill to turn SQL outputs, DataFrame-style data, and chart assets into structured business reports and dashboards. It supports reusable templates, statistical insight generation, and HTML, JSON, and PDF-oriented report workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may include user- or data-controlled values without escaping.

Mitigation: Review reports before distribution; do not host generated HTML on authenticated or trusted origins until text escaping, base64/image validation, CSS/class restrictions, and an appropriate CSP are in place.

Risk: Reports generated from uploaded, third-party, database, or customer-controlled data may expose privacy, legal, or content risks.

Mitigation: Review inputs and outputs, add privacy and legal guardrails for templates that profile users or recommend outreach, and limit use to approved datasets.

Risk: Unpinned or incomplete dependencies can make installs non-reproducible.

Mitigation: Pin and verify Python dependencies before production installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moniq888/skills/sql-report-generator)
- [Templates index](artifact/references/templates-index.md)
- [Chart guidelines](artifact/references/chart-guidelines.md)
- [Chart planning](artifact/references/chart-planning.md)
- [Insight patterns](artifact/references/insight-patterns.md)
- [Dashboard templates](artifact/DASHBOARD_TEMPLATES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and Python code examples, with generated report artifacts in HTML, JSON, and PDF-oriented formats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python dependencies; full report generation depends on pandas, numpy, matplotlib, jinja2, and scipy.]

## Skill Version(s):

1.0.1 (source: server release metadata and user changelog, released 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
