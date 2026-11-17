## Description:

Connects an agent to Sequence so it can read business banking data, report cash position, inspect transfers, cards, and rules, and propose money-moving automations that require human approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getsequence](https://clawhub.ai/user/getsequence)

### License/Terms of Use:

MIT-0

## Use Case:

Business users, finance operators, and developers use this skill to connect an agent to a Sequence account for business banking questions, cash visibility, transfer history, card activity, and controlled money-movement proposals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects an agent to business banking data.

Mitigation: Install only for users who intend to connect their Sequence business finance account, review plugin capabilities during setup, and prefer read-only list/get tools unless transfer proposals are needed.

Risk: Transfer actions can affect real funds if approved.

Mitigation: Treat money movement as a proposal, confirm amount, source, and destination, and require human approval in Sequence before funds move.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/getsequence/skills/sequence-finance)
- [Sequence publisher profile](https://clawhub.ai/user/getsequence)
- [Sequence website](https://getsequence.io)
- [Sequence agent setup](https://app.getsequence.io/agents)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with setup commands and operational instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to call Sequence MCP tools for account data, balances, transfers, cards, and transfer proposals.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
