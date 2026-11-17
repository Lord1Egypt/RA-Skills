## Description:

Use when two Polymarket markets imply different probabilities for a linked outcome.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-strategy analysts use this skill to evaluate relative-value spreads between linked Polymarket markets and frame NautilusTrader strategy parameters before custom implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The spread may reflect different market outcome mappings or resolution rules rather than a tradable inefficiency.

Mitigation: Confirm both markets have comparable resolution logic before using the strategy guidance.

Risk: Filled TradeTick backtests cannot prove simultaneous fills or full cross-book liquidity for both legs.

Mitigation: Review liquidity, order sizing, and entry/exit feasibility separately before any live Polymarket or NautilusTrader deployment.

Risk: The skill is trading-analysis guidance and not a finished live-trading system.

Mitigation: Adapt the archetype into reviewed custom code with user-confirmed live trading controls before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides strategy-analysis guidance only; live trading controls, order sizing, liquidity, and credentials require separate review.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
