## Description:

Tradedaily helps stock traders manage daily trading schedules, generate opening, closing, and end-of-day report templates, monitor portfolio risk alerts, record trading logs, and support performance review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horizoncove](https://clawhub.ai/user/horizoncove)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and trading teams use this skill to organize a daily stock-trading workflow, produce markdown briefings, and check portfolio risk thresholds. It is intended as workflow and reporting support, not as a source of financial advice or trade execution authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled portfolio data may contain sensitive holdings and account information.

Mitigation: Replace bundled portfolio data with a private local file or synthetic example and redact generated reports before sharing.

Risk: The risk monitor uses an unauthenticated HTTP quote service, so market data can be unavailable, stale, or tampered with in transit.

Mitigation: Use an authenticated HTTPS market data source and validate returned prices before relying on risk alerts.

Risk: Trading thresholds and generated reports can be mistaken for investment advice.

Mitigation: Treat thresholds as examples and require qualified human review before making trading decisions.

## Reference(s):

- [Daily Schedule](artifact/references_files/daily-schedule.md)
- [Report Templates](artifact/references_files/report-templates.md)
- [Risk Management](artifact/references_files/risk-management.md)
- [ClawHub Skill Page](https://clawhub.ai/horizoncove/skills/trader-daily)
- [Publisher Profile](https://clawhub.ai/user/horizoncove)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and command-line guidance backed by JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes portfolio and risk configuration examples; generated reports should be reviewed and redacted before sharing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
