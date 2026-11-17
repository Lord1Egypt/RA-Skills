## Description:

A Chinese-language virtual stock-trading skill for learning investing, recording simulated trades, viewing returns, and using A-share, Hong Kong, and U.S. market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingdevatil](https://clawhub.ai/user/kingdevatil)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to practice stock-investing workflows with simulated capital, track virtual holdings and transactions, and inspect educational market recommendations across A-share, Hong Kong, and U.S. equities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat simulated stock recommendations as financial advice.

Mitigation: Present recommendations as educational simulation output and encourage independent review before any real trading.

Risk: Proxy settings can route market-data requests through a user-specified intermediary.

Mitigation: Review proxy settings before enabling them and leave proxy access disabled when direct API access works.

Risk: The skill creates local simulated portfolio records.

Mitigation: Store only simulated portfolio data and review or remove workspace stock_data records when they are no longer needed.

## Reference(s):

- [Stock API Reference](references/stock_api.md)
- [ClawHub Skill Page](https://clawhub.ai/kingdevatil/skills/stock-simulator)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown responses with optional Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON files for simulated account configuration, holdings, transactions, and profits.]

## Skill Version(s):

1.0.2 (source: server release metadata and target metadata; artifact footer says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
