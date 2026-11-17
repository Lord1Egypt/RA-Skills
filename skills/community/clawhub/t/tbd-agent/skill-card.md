## Description:

TBD is a prediction market for crypto, sports, politics, and culture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coreyjoshuamiller](https://clawhub.ai/user/coreyjoshuamiller)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to browse TBD prediction-market campaigns, inspect account balance, configure bet size, and place USDC-backed bets through the tbd-vote CLI or HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable repeated real-money USDC bets without clear per-bet confirmation or strong spending controls.

Mitigation: Require explicit user confirmation for each bet, set strict spending limits, monitor balances, and keep API-key revocation or rotation available before use.

Risk: A global latest-version CLI install can make agent behavior depend on an unpinned package version.

Mitigation: Use an isolated, pinned CLI install when possible and review the installed package before granting access to a funded account.

## Reference(s):

- [TBD skill page](https://clawhub.ai/coreyjoshuamiller/skills/tbd-agent)
- [Publisher profile](https://clawhub.ai/user/coreyjoshuamiller)
- [TBD website](https://tbd.vote)
- [TBD API base URL](https://production-tbd-bets-api.tbd.vote)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash, JSON, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers API-key authentication, JSON CLI output, USDC bet sizing, rate limits, and raw HTTP fallback commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
