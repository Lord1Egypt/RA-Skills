## Description:

Pre-trade readiness check for autonomous agents that returns wallet identity, venue status, spendable balance, open exposure, and an ok_to_trade verdict before live real-venue trades proceed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and autonomous-agent operators use this skill before automated trade submission to check account readiness, wallet identity, balance, exposure, and blocking conditions. It supports pre-trade audit logging and fail-closed handling when a real-venue trade is not ready to proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Simmer API key and reports trading-account readiness data, including wallet, balance, exposure, blockers, and warnings.

Mitigation: Install only from a trusted publisher, provide the API key through the SIMMER_API_KEY environment variable, and avoid exposing JSON or terminal output where account details should remain private.

Risk: Preflight checks depend on current account, venue, and position data, so stale or failed checks can affect trade readiness decisions.

Mitigation: Run the check once per trade intent, inspect blockers and warnings, and treat configuration or fetch failures as reasons to pause live trading until resolved.

## Reference(s):

- [Simmer API and wallet documentation](https://docs.simmer.markets)
- [ClawHub skill page](https://clawhub.ai/simmer/skills/simmer-preflight)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable terminal output or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses exit codes 0, 1, and 2 to indicate pass, blocked, or configuration error.]

## Skill Version(s):

0.3.6 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
