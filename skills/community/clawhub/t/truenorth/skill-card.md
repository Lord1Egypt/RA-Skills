## Description:

TrueNorth crypto market intelligence: technical analysis (RSI, MACD, Bollinger Bands), derivatives (funding rates, open interest), DeFi (TVL, fees), token performance, events, liquidation risk, token unlock, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[truenorth-lj](https://clawhub.ai/user/truenorth-lj)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent for read-only crypto market intelligence, including technical indicators, derivatives data, DeFi metrics, token performance, events, liquidation risk, and token unlock information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a mutable global third-party npm CLI using the latest package tag.

Mitigation: Review the package before installation and prefer a pinned version or isolated environment when available.

Risk: Token-related prompts may be sent to TrueNorth's external public API for entity recognition and market data lookups.

Mitigation: Do not include private keys, credentials, wallet details, account information, or sensitive trading context in requests.

Risk: Market intelligence may be incomplete, stale, or unsuitable for trading decisions.

Mitigation: Treat outputs as informational analysis and independently verify data before acting on financial decisions.

## Reference(s):

- [TrueNorth web app](https://app.true-north.xyz)
- [TrueNorth CLI package](https://www.npmjs.com/package/@truenorth-ai/cli)
- [ClawHub skill page](https://clawhub.ai/truenorth-lj/skills/truenorth)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with natural language analysis and JSON-producing CLI command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses summarize read-only API results and include a TrueNorth web app call to action.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
