## Description:

Proactive spending alerts via Plaid. Track credit card spending against a monthly budget with pace-based alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbornhorst1524](https://clawhub.ai/user/jbornhorst1524)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to set up Spend Pulse, sync Plaid transaction data, check monthly budget pace, and compose concise spending alerts with optional chart attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle real financial credentials and transaction data through an external CLI.

Mitigation: Review the CLI package and source before installing, prefer a pinned or verified release, and avoid exposing Plaid credentials or stored transaction data.

Risk: Generated spending messages and charts may contain sensitive merchant, account, or transaction details.

Mitigation: Confirm the recipient and channel before sending, and include only the transaction details the user explicitly wants shared.

## Reference(s):

- [Spend Pulse ClawHub listing](https://clawhub.ai/jbornhorst1524/skills/spend-pulse)
- [Plaid developer keys](https://dashboard.plaid.com/developers/keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated spending chart image paths when the underlying CLI returns them.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
