## Description:

Queries A-share market data, filters stocks, and runs quantitative strategy backtests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zizhenghua](https://clawhub.ai/user/zizhenghua)

### License/Terms of Use:

MIT-0

## Use Case:

External users can query A-share realtime and historical prices, screen stocks by market metrics, and run strategy backtests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock queries, filters, strategy settings, and extra JSON fields are sent to zizhenghua.com.

Mitigation: Send only necessary, nonconfidential parameters and review the provider's privacy and retention practices before sharing proprietary strategies.

## Reference(s):

- [Source repository](https://github.com/Zizhenghua/quant-skill)
- [ClawHub skill page](https://clawhub.ai/zizhenghua/skills/quant-skill)
- [Quant data API](https://zizhenghua.com/api)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON data printed to standard output, with plain-text error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Backtests may return large daily arrays; the skill recommends presenting strategyReturn, maxDrawdown, winRate, summary, and trades.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
