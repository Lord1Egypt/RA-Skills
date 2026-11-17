## Description:

Institutional-grade L2 Orderbook Imbalance (OBI) detector. Captures market maker footprints across OKX and Binance with millisecond precision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmstudio667-commits](https://clawhub.ai/user/tmstudio667-commits)

### License/Terms of Use:


## Use Case:

External users and trading-tool developers use this skill to request L2 orderbook imbalance analysis for crypto markets, including market-maker footprint and cross-exchange liquidity pattern detection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The usage example runs an unpinned npx command.

Mitigation: Use a pinned and trusted OpenClaw CLI version before installing or running the skill.

Risk: Trading-performance claims are not supported by bundled auditable scanner code.

Mitigation: Treat market-scan outputs and performance claims as unverified until independently reviewed against trusted data and execution logs.

Risk: The release describes a paid scan flow.

Mitigation: Confirm the payment and service provider details before authorizing any USDC transaction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tmstudio667-commits/skills/sovereign-liquidity-sniffer)
- [Publisher Profile](https://clawhub.ai/user/tmstudio667-commits)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner behavior and trading-performance claims are not backed by bundled auditable scanner code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
