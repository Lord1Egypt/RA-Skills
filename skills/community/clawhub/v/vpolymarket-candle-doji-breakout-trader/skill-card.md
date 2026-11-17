## Description:

Detects doji patterns in crypto 5-minute interval markets on Polymarket and trades the post-doji breakout in the direction of the pre-doji trend for BTC, ETH, SOL, and XRP Up or Down bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to identify doji-after-trend patterns in Polymarket crypto interval markets and submit paper or explicitly enabled live trades with conviction-based sizing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real Polymarket trades when run with --live.

Mitigation: Use paper mode first and enable --live only after reviewing the strategy, position limits, and acceptable USDC exposure.

Risk: Security evidence says advertised risk controls are weak or not fully enforced.

Mitigation: Review or fix the risk-control gaps before live use, including spread, position, and execution safeguards.

Risk: The skill requires SIMMER_API_KEY, a high-value trading credential.

Mitigation: Use a narrowly scoped API key with only the trading authority the operator is willing to expose.

Risk: The skill depends on simmer-sdk for market discovery and trade execution.

Mitigation: Pin and verify the simmer-sdk package before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/vpolymarket-candle-doji-breakout-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls]

**Output Format:** [Console log text and trade API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless run with --live.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
