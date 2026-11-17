## Description:

Provides real-time mainland China A-share quotes, stock and index analysis, sector monitoring, trading strategy suggestions, and price-alert support using market data sources such as Eastmoney and Sina Finance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to ask an agent for mainland China A-share quotes, market sentiment, technical and fundamental stock analysis, sector trends, and risk-aware trading strategy suggestions.

### Deployment Geography for Use:

Global, for analysis of mainland China A-share markets.

## Known Risks and Mitigations:

Risk: Trading guidance may be based on unauthenticated HTTP market data.

Mitigation: Use the skill for educational analysis and verify prices with a trusted HTTPS broker or data provider before making trades.

Risk: The skill can provide trading suggestions that may be incorrect or misleading.

Mitigation: Require human review of recommendations, keep risk notes attached to price advice, and avoid treating outputs as guaranteed financial advice.

Risk: Local watchlist entries may record user alert targets or trading interests.

Mitigation: Avoid storing sensitive information in watchlists and periodically review or delete local alert entries.

Risk: Some referenced data sources may require session cookies.

Mitigation: Avoid providing session cookies unless they can be stored and handled securely.

## Reference(s):

- [A Stock Trading Assistant on ClawHub](https://clawhub.ai/tobeyrebecca/skills/toby-stock-trading)
- [Stock Analysis Methods](references/analysis.md)
- [Market Data Source APIs](references/data-sources.md)
- [Complete Setup Guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose and tables, with optional JSON emitted by the market-data helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market outputs should include data source and fetch time; price suggestions should include risk notes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
