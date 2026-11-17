## Description:

Polymarket Analysis fetches Polymarket market data, leaderboards, price movement, and sentiment indicators to produce structured market analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to inspect Polymarket trending markets, category activity, market-level prices, volume, liquidity, and sentiment signals. The generated reports support market research and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact a third-party billing service and attempt a 0.001 USDT charge during normal analysis startup.

Mitigation: Install only when the billing behavior is desired, clearly disclosed, and gated by explicit per-charge consent.

Risk: The security evidence reports a bundled billing API key that is not safely scoped for a market-analysis tool.

Mitigation: Require the publisher to remove or rotate the exposed key and move billing credentials to a user-controlled secret before deployment.

Risk: The analysis output may be mistaken for investment advice or may rely on incomplete live market data.

Mitigation: Present outputs as informational market research, verify live prices and liquidity from Polymarket before acting, and retain the skill's risk disclaimer.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shenmeng/skills/shenmeng-polymarket-analysis)
- [Polymarket Gamma API](https://gamma.polymarket.com)
- [Polymarket CLOB API](https://clob.polymarket.com)
- [Polymarket Predictions](https://polymarket.com/predictions)
- [Polymarket Leaderboard](https://polymarket.com/leaderboard)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis report with optional JSON market details and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes market overview, category highlights, deep-dive data, risk notes, and user-facing suggestions.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
