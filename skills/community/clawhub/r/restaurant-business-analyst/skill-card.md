## Description:

Generates restaurant-industry business model analysis reports for brands or formats, combining strategy, recent market moves, operating metrics, and confidence-labeled data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louiseliu](https://clawhub.ai/user/louiseliu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, operators, founders, executives, and investors use this skill to generate restaurant brand or category analysis covering business model canvas, strategic activity, unit economics, operating metrics, risks, and optional ESG or expansion modules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and opens a local HTML report from user-supplied restaurant brand or category names.

Mitigation: Use normal restaurant names rather than path-like input, and ask the agent to sanitize filenames before writing the report.

Risk: Dynamic report content may include public web-search results, links, and HTML-rendered text.

Mitigation: Escape dynamic HTML content, validate links, and review sourced claims before opening or sharing the report.

Risk: Restaurant operating metrics and strategic analysis may be incomplete or misleading when public data is unavailable.

Mitigation: Keep confidence labels on core figures, mark unknown data as not publicly disclosed, use benchmarks only as estimates, and retain the non-investment-advice disclaimer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/louiseliu/skills/restaurant-business-analyst)
- [Project homepage](https://github.com/louiseliu/restaurant-business-analyst)
- [Restaurant industry data analysis methodology](references/analytics_methodology.md)
- [Restaurant business model framework library](references/business_model_frameworks.md)
- [Restaurant metrics framework](references/metrics_framework.md)
- [Strategy, tactics, and metrics report template](references/report_template.md)

## Skill Output:

**Output Type(s):** [Analysis, Files, Code, Guidance]

**Output Format:** [HTML report with a short text summary and optional browser-generated PDF export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Core figures are expected to include confidence labels, and reports include a public-information disclaimer that they are not investment advice.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
