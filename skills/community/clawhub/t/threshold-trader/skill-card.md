## Description:

Automatically trades prediction markets when prices deviate beyond a configured probability threshold, using Kelly Criterion sizing and safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skybinjf](https://clawhub.ai/user/skybinjf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-automation users use this skill as a configurable template for scanning prediction markets and submitting trades when market prices diverge from their probability estimates. It can run in simulated venues for testing or against supported real-money venues when explicitly configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated trading can affect authenticated trading-account state, including against real-money venues when live mode and venue settings are enabled.

Mitigation: Review the code and configuration before use, test on the sim venue first, and enable real-money trading only after explicitly accepting the trading risk.

Risk: Dry-run mode is not fully read-only because auto-redemption can still interact with account state.

Mitigation: Use credentials and accounts appropriate for testing, and review auto-redemption behavior before running the skill with production credentials.

Risk: Unpinned dependencies or publishing scripts run from a broader repository could expose private files or credentials.

Mitigation: Pin dependencies for operational use and avoid running bundled publish scripts from repositories that contain unrelated private material or secrets.

## Reference(s):

- [Threshold Trader on ClawHub](https://clawhub.ai/skybinjf/skills/threshold-trader)
- [Simmer Skill-Building Documentation](https://docs.simmer.markets/skills/building)
- [Simmer Dashboard](https://simmer.markets/dashboard)
- [Simmer Skills Registry](https://simmer.markets/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation, shell command examples, JSON configuration, and a Python trading script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and supports environment-variable configuration for venue, probability threshold, side, minimum edge, Kelly multiplier, and maximum position size.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
