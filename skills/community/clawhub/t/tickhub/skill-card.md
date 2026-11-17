## Description:

TickHub helps agents answer real-time stock quote questions for A-share, Hong Kong, and U.S. equities with current price, price movement, percentage change, and volume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oct16](https://clawhub.ai/user/oct16)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to quickly answer current stock price and movement questions from a stock code or name. It is for informational quote lookup, not historical chart analysis, technical indicator calculation, or investment recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock symbols or company names from user requests may be sent to external market-data services.

Mitigation: Use the skill only when that disclosure is acceptable for the request and avoid sending sensitive portfolio or account context.

Risk: Returned quote data may be delayed, unavailable, or unsuitable as financial advice.

Mitigation: Present results as informational market data and avoid using the skill for investment recommendations.

## Reference(s):

- [TickHub ClawHub skill page](https://clawhub.ai/oct16/skills/tickhub)
- [TickHub stock quote endpoint example](https://tickhub.net/stock/600519)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Concise human-readable stock quote summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned quotes should be treated as informational market data, not investment advice.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
