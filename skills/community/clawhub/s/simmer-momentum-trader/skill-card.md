## Description:

Momentum-based trading skill for Simmer prediction markets. Detects probability momentum and divergence to generate YES/NO trades on Polymarket. Remixable -- swap in your own signal source or combine with other indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrjoeteam](https://clawhub.ai/user/mrjoeteam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-automation users use this skill to monitor Simmer watchlist markets and generate or execute YES/NO Polymarket trades from a configurable momentum and divergence strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place automated financial trades when live mode is enabled, and the authoritative security summary flags safety and accuracy gaps.

Mitigation: Review the strategy before installation, keep dry-run mode until validated, use conservative account limits, and only enable --live with a narrowly scoped Simmer API key.

Risk: Unpinned dependencies, numeric configuration, and fail-open behavior can change trading behavior or allow orders under weak validation.

Mitigation: Pin and review dependencies, validate threshold and trade amount settings, and consider fail-closed safeguards before scheduled or live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrjoeteam/skills/simmer-momentum-trader)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls]

**Output Format:** [Console text with optional Python execution and Simmer API trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; live trading requires the --live flag and a SIMMER_API_KEY environment variable.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
