## Description:

Provides Tiger Brokers US stock trading support for account balance queries, positions, buy and sell order placement, and order management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjpwc](https://clawhub.ai/user/wjpwc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an agent to Tiger Brokers account, position, balance, order placement, and order cancellation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive Tiger credentials and private keys.

Mitigation: Use a protected key file or secret manager, and do not paste private keys into chats or command lines.

Risk: The skill can submit buy, sell, and cancellation actions against brokerage accounts.

Mitigation: Require manual review before any order or cancellation action, and use a simulated or paper-trading Tiger environment unless live trading is intentional.

Risk: A real brokerage workflow can cause financial loss if parameters are wrong or misunderstood.

Mitigation: Confirm symbol, side, quantity, order type, account, and environment before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjpwc/skills/tiger-trading)
- [Publisher profile](https://clawhub.ai/user/wjpwc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples plus JSON response structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include account, balance, position, order, and error fields returned by Tiger Brokers APIs.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
