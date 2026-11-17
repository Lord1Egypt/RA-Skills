## Description:

Provides real-time quote lookup for A-shares, Hong Kong stocks, and futures, plus A-share sector leaderboards and symbol search using a configured Qutedance quote service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoocky](https://clawhub.ai/user/yoocky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve market quotes, search tradable symbols, and summarize A-share sector movement in chat as Markdown tables and lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls a configured Qutedance service for market data.

Mitigation: Install only if that external service is acceptable for the intended environment and data-handling policy.

Risk: The skill encourages storing an API key in config.json.

Mitigation: Use QUTEDANCE_API_KEY or another secret mechanism instead, and rotate any key that may have been saved or shared in the skill directory.

Risk: Market data returned by the skill may be time-sensitive or unsuitable as financial advice.

Mitigation: Treat outputs as informational quotes and verify important trading or investment decisions against authoritative financial sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yoocky/skills/qutedance-quotes)
- [Publisher profile](https://clawhub.ai/user/yoocky)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown tables and lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns market data retrieved from the configured Qutedance service; output is informational and not investment advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
