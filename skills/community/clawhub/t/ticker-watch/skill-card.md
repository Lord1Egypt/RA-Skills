## Description:

Helps users look up public stock prices, price history, dividends, splits, and tickers through ClawLink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can check public stock prices and trends, find tickers, and review dividends or splits for portfolio check-ins and market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the ClawLink plugin requires account and device pairing.

Mitigation: Explain the plugin and pairing requirement before installation and let the user approve device pairing.

Risk: Market-data calls spend ClawLink credit, especially across many tickers or expensive calls.

Mitigation: Check the current per-call price and ask the user before large batches or calls costing more than a few cents.

## Reference(s):

- [Ticker Watch on ClawHub](https://clawhub.ai/hith3sh/skills/ticker-watch)
- [ClawLink OpenClaw documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=ticker-watch)
- [Verify the ClawLink plugin](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language responses with stock market data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public market data; end-of-day prices by default, with delayed US intraday prices when requested.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
