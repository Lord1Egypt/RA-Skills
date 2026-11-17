## Description:

Provides structured financial market data through the WeStock CLI for stocks, ETFs, indexes, sectors, futures, forex, convertible bonds, company filings, research reports, risk events, fund flows, ETF holdings, investment calendars, and macroeconomic indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[westock-skills](https://clawhub.ai/user/westock-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and agent developers use this skill to answer financial-data questions by selecting the correct westock command and interpreting returned market, fundamentals, event, and macroeconomic data. It is for informational analysis and not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup scripts install a remote westock executable from the Tencent/stockbuddy.qq.com release source.

Mitigation: Install only when the publisher and release source are trusted; review the setup script first and use dry-run or a custom install directory where practical.

Risk: The bash and PowerShell installers can persist PATH changes in the user environment.

Mitigation: Review the intended install location before execution and confirm PATH changes match local policy.

Risk: The skill returns financial market data that may be delayed or incomplete for investment decisions.

Mitigation: Present results as informational data, preserve disclosed data dates, and avoid treating the output as investment advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/westock-skills/skills/westock-data)
- [Publisher Profile](https://clawhub.ai/user/westock-skills)
- [WeStock CLI Release Source](https://stockbuddy.qq.com/release/clawhub/cli)
- [routing-guide.md](references/routing-guide.md)
- [commands.md](references/commands.md)
- [scenarios-guide.md](references/scenarios-guide.md)
- [ai_usage_guide.md](references/ai_usage_guide.md)
- [macro-fields.md](references/macro-fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables and explanatory text with westock CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and a locally installed westock executable; market data may be delayed and should be treated as informational.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
