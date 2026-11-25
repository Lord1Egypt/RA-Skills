## Description:

Use when holding idle USDC on Hyperliquid and looking for yield, when already holding a BTC perp and wanting extra income on it (covered-call style), or when building a market-making bot for options. TLP is the default way to earn (one deposit, the venue quotes and manages for you); Custom is the port a maker's existing pricing, limits and margin systems plug into.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gnostrich](https://clawhub.ai/user/gnostrich)

### License/Terms of Use:

MIT-0

## Use Case:

External options makers and developers use this skill to understand and operate Temporal's Hyperliquid options market-making modes, either through venue-managed quoting or a custom pricing bot. It describes maker account actions, quote setup, and relevant margin and position risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Option positions can lose money, and displayed return excludes option P/L; sold options can be liquidated if margin falls below maintenance plus the stated penalty.

Mitigation: Review position exposure, margin, and liquidation distance before depositing or enabling quotes, and treat displayed return as incomplete.

Risk: Custom quoting can create loss exposure; the venue has no breaker for crossed quotes, and caps limit size rather than loss.

Mitigation: Use deterministic pricing with explicit exposure limits and stop rules, and monitor account state and margin rather than relying on venue limits as loss bounds.

Risk: The skill describes the venue as an unaudited open beta.

Mitigation: Confirm the venue's current beta status and deposit limits before funding an account.

## Reference(s):

- [Temporal Earn documentation](https://protect.temporal.exchange/docs/earn)
- [Temporal](https://temporal.exchange)
- [ClawHub skill release](https://clawhub.ai/gnostrich/skills/temporal-earn)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Configuration instructions]

**Output Format:** [Markdown instructions with tool-call examples, API parameters, and custom maker client guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers venue-managed and custom quoting workflows, wallet signing, and maker position and margin operations.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
