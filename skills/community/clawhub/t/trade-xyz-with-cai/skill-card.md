## Description:

Trade HIP-3 markets on trade.xyz via CAI using Hyperliquid Route B tools for xyz:SYMBOL assets, orders, positions, and cancellations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernardtai](https://clawhub.ai/user/bernardtai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to guide agents through CAI-mediated trade.xyz HIP-3 market workflows, including placing, checking, and cancelling Hyperliquid builder-market orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides live trading and may require broad CAI platform or full API authority, creating financial-loss risk if credentials, balances, or permissions are misused.

Mitigation: Use the narrowest available CAI key scope and only fund balances the user is comfortable risking.

Risk: The security summary notes that the artifact does not clearly require explicit confirmation before live orders.

Mitigation: Require explicit user confirmation for every live order, including asset, side, size, price, venue, and order action before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bernardtai/skills/trade-xyz-with-cai)
- [CAI Canonical Skill Reference](https://cai.com/skill.md)
- [trade.xyz HIP-3 Documentation](https://docs.trade.xyz/about-trade-xyz/hyperliquid-xyz-and-hip-3)
- [CAI Developer Documentation](https://cai.com/developers.html)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline shell commands and structured parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference live-trading parameters including asset, side, size, price, order id, platform_slug, and dex.]

## Skill Version(s):

1.0.15 (source: evidence.release.version and artifact frontmatter metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
