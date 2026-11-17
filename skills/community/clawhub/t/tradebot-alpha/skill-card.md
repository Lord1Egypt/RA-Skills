## Description:

Read-only signal fetcher for the TradeBot Alpha API; Pro-tier signal analysis requires a subscription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zalcmann](https://clawhub.ai/user/zalcmann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-tool users use this connector to check TradeBot Alpha API status and fetch read-only trading signals. Pro-tier signal analysis requires an API key and a separate TradeBot Alpha subscription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented command-line API key flow can expose credentials through local shell history or process listings.

Mitigation: Review before installation, prefer a safer credential channel when available, and rotate any key previously used on the command line.

Risk: Returned trading signals are third-party financial data and may influence trading decisions.

Mitigation: Treat all signals as external data, verify them independently, and keep responsibility for trading decisions outside the connector.

## Reference(s):

- [TradeBot Alpha ClawHub Skill Page](https://clawhub.ai/zalcmann/skills/tradebot-alpha)
- [TradeBot Alpha Homepage](https://tradebot-alpha.bluefeza.com)
- [TradeBot Alpha API Documentation](https://tradebot-alpha.bluefeza.com/docs)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [CLI text summarizing API status or trading signals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided API key for authenticated API calls.]

## Skill Version(s):

0.1.14 (source: ClawHub release metadata; artifact files list 0.1.13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
