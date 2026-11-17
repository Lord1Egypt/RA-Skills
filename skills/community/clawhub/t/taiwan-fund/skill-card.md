## Description:

Query Taiwan mutual fund NAV, performance, holdings via cnyes/MoneyDJ, compare funds, and auto-convert foreign currency values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ichendong](https://clawhub.ai/user/ichendong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Taiwan mutual fund NAV, compare fund performance against other funds or benchmarks, view watchlist entries, and convert foreign-currency fund values to TWD.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries third-party public finance endpoints for NAV, benchmark, and exchange-rate data.

Mitigation: Review data-source availability and terms before deployment, and verify financial outputs against authoritative sources before using them for decisions.

Risk: The skill stores a local TDCC cache for offshore fund data.

Mitigation: Install only where local cache writes are acceptable and clear the cache according to the user's data-handling policy.

Risk: Server security guidance says the holdings claim is incomplete.

Mitigation: Present holdings-related output as limited and rely on the skill primarily for NAV, performance, benchmark comparison, exchange rates, watchlist output, and links or prompts for further detail.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ichendong/skills/taiwan-fund)
- [cnyes fund overview](https://invest.cnyes.com/funds/detail/{name}/{code}/overview)
- [TDCC offshore fund OpenAPI](https://openapi-t.tdcc.com.tw/v1/opendata/3-4)
- [Yahoo Finance chart API](https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=5y&interval=1d)
- [ExchangeRate API](https://open.er-api.com/v6/latest/USD)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query third-party public finance endpoints and may write a local TDCC cache under the user's home directory.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
