## Description:

Tradebot Ops helps an agent monitor trading bot health, detect stale runtime state, verify data freshness, and summarize recovery actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[motivationationdaily](https://clawhub.ai/user/motivationationdaily)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check whether a live trading bot is healthy, explain why it may not be trading, and propose a restart or stale-state recovery action with verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to stop, restart, or clean stale state for a live trading bot without enough target confirmation.

Mitigation: Require manual confirmation of the target process, current positions, pending orders, and rollback steps before executing any stop, restart, or cleanup action.

Risk: Operational recovery guidance could affect a financial trading system.

Mitigation: Use the skill as an operations aid, verify bot status and market exposure independently, and keep the rule that risk percentage must not be raised automatically.

## Reference(s):

- [Tradebot Ops on ClawHub](https://clawhub.ai/motivationationdaily/skills/tradebot-ops)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise Markdown or plain-text health summary with a proposed action, verification step, and audit log entry.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stop, restart, or stale-state cleanup guidance; should not increase trading risk automatically.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
