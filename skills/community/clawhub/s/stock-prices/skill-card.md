## Description:

Query real-time stock prices and market data using the Stock Prices API, with responses returned in TOON format for decoding with @toon-format/toon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anthonylee1994](https://clawhub.ai/user/anthonylee1994)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to fetch current stock quotes, monitor prices, summarize portfolios, and analyze common market fields for ticker symbols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker and portfolio symbol lists are sent to stock-prices.on99.app.

Mitigation: Send only the ticker symbols required for the quote lookup and avoid placing unrelated sensitive information in the symbols parameter.

Risk: The skill depends on the third-party @toon-format/toon decoder to parse API responses.

Mitigation: Verify the package source and pin a specific reviewed package version before use.

## Reference(s):

- [Stock Prices API](https://stock-prices.on99.app)
- [Stock Prices ClawHub skill page](https://clawhub.ai/anthonylee1994/skills/stock-prices)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Markdown with inline bash and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses are TOON text and should be decoded with @toon-format/toon before use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
