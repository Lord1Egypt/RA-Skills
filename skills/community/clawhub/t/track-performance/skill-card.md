## Description:

Track the performance of Uniswap LP positions over time — check which positions need attention, are out of range, or have uncollected fees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External users with existing Uniswap LP positions use this skill to review position health, fee accumulation, range status, and action items across wallet, chain, and time-window filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation mentions configuring a private wallet key even though performance tracking should only need public wallet data.

Mitigation: Use a public wallet address for tracking and do not provide seed phrases, private keys, or signing credentials.

Risk: Mutable install sources can change after review.

Mitigation: Prefer a pinned install source or a reviewed ClawHub release instead of mutable latest or main references.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/track-performance)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown performance summary with position status, fee details, alerts, and action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegates analysis to the portfolio-analyst agent; performance data may be delayed due to RPC or subgraph synchronization.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
