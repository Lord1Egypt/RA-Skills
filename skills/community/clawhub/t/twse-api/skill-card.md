## Description:

Query official Taiwan Stock Exchange OpenAPI data for listed Taiwan securities, including quotes, valuation ratios, index history, company profiles, financial statements, revenue, margin trading, block trades, ESG disclosures, warrants, broker data, and the trading calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanookai](https://clawhub.ai/user/nanookai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to identify TWSE OpenAPI endpoints, fetch public Taiwan-listed securities data, and interpret endpoint-specific JSON fields, date formats, and data limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public market and financial data can be incomplete, stale, or misinterpreted when used for investment decisions.

Mitigation: Verify important investment decisions independently against authoritative sources and treat skill output as public-source information.

Risk: Example commands may fetch TWSE data and run local parsing logic over returned JSON.

Mitigation: Review commands before execution and avoid dumping large raw endpoint responses into an agent context.

## Reference(s):

- [TWSE OpenAPI docs](https://openapi.twse.com.tw/)
- [TWSE OpenAPI Swagger spec](https://openapi.twse.com.tw/v1/swagger.json)
- [ClawHub skill page](https://clawhub.ai/nanookai/skills/twse-api)
- [TWSE API - Securities Trading](references/securities-trading.md)
- [TWSE API - Corporate Governance](references/corporate-governance.md)
- [TWSE API - Financial Statements](references/financial-statements.md)
- [TWSE API - Indices](references/indices.md)
- [TWSE API - Warrants](references/warrants.md)
- [TWSE API - Broker Data](references/brokers.md)
- [TWSE API - Miscellaneous](references/misc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoint paths, JSON field names, and parsing guidance; does not create persistent files by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
