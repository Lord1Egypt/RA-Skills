## Description:

StockBuddy helps agents analyze CN, HK, and US equities, review portfolios, manage watchlists and accounts, and produce execution-aware trading guidance with risk disclaimers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tacitlab](https://clawhub.ai/user/tacitlab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use StockBuddy to analyze individual stocks, review portfolios, track durable account and position facts, and generate practical order suggestions for CN, HK, and US equities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores portfolio and account facts locally, and the security summary warns that migration can erase legacy positions.

Mitigation: Back up any existing ~/.stockbuddy/stockbuddy.db before use and test migrations on a copy when preserving prior portfolio data matters.

Risk: The dependency installer can modify the Python environment, including a fallback that uses --break-system-packages.

Mitigation: Install dependencies in an isolated virtual environment or user environment, and avoid running the installer against system Python unless that package-management risk is acceptable.

Risk: The skill calls external market, news, and filing services and can produce action-oriented trading guidance.

Mitigation: Treat outputs as reference material, verify market data independently, require missing execution constraints before order-size guidance, and retain the investment-risk disclaimer.

## Reference(s):

- [Technical Indicators Reference](references/technical_indicators.md)
- [Output Templates](references/output_templates.md)
- [Data Source Roadmap](references/data-source-roadmap.md)
- [ClawHub Skill Page](https://clawhub.ai/tacitlab/skills/stockbuddy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands; analysis scripts return JSON for agent interpretation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes action labels, scores, confidence, event-adjusted suggestions, portfolio summaries, execution constraints, and investment-risk disclaimers.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
