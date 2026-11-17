## Description:

Uses the Futu paper trading API to query market data, holdings, orders, fills, and submit simulated trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxxwang](https://clawhub.ai/user/xxxwang)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent inspect Hong Kong stock market data, account funds, positions, orders, fills, and place or cancel paper-trading orders through a local FutuOpenD service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update Python packages in its own environment.

Mitigation: Use a prebuilt or reviewed Python environment and prefer pinned dependency versions before running the skill.

Risk: The skill can send trading credentials to a configurable FutuOpenD endpoint.

Mitigation: Keep FUTU_HOST pointed at a trusted local FutuOpenD service and avoid reusing account passwords through FUTU_PASSWORD.

Risk: The skill can place or cancel simulated trading orders without an additional confirmation step.

Mitigation: Review proposed order commands before execution and do not run automated trading loops unattended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xxxwang/skills/xtrade-futu-paper-trade)
- [FutuOpenD download and setup](https://www.futuhk.com/en/support/topic1_464)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command output with ok, data, error, and next-step fields where applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, a local FutuOpenD service, and futu-api and akshare Python dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
