## Description:

Check balances and transfer Quack tokens through the Quack Network API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpaulgrayson](https://clawhub.ai/user/jpaulgrayson)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent check a Quack token balance and initiate token transfers or payments on the Quack Network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The transfer script can move tokens using stored credentials without a built-in confirmation step.

Mitigation: Require an explicit confirmation process before execution and verify the recipient and amount immediately before running a transfer.

Risk: The skill depends on an agent-accessible Quack API credential.

Mitigation: Install and run it only in trusted environments, protect the credential file, and limit credential access to agents authorized to view balances or initiate transfers.

Risk: Transfers may be sensitive and potentially irreversible.

Mitigation: Start with low-value transfers, keep an audit trail of recipient, amount, and memo, and use operational controls appropriate for token movement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpaulgrayson/skills/quack-wallet)
- [Quack Network API](https://quack.us.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code]

**Output Format:** [Markdown guidance with bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local Quack API credential; transfer commands accept recipient, amount, memo, and optional agent ID.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
