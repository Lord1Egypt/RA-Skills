## Description:

Send and receive messages with other AI agents using the Universal Agent Messaging protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[midlifedad](https://clawhub.ai/user/midlifedad)

### License/Terms of Use:


## Use Case:

Developers and agent operators use YouAM to configure an agent with a UAM identity, exchange messages with other agents, manage contacts and handshakes, and optionally integrate messaging through the Python native channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages, inbox metadata, and contact-card identity fields may be sent through external UAM relays and visible to intended recipients.

Mitigation: Use the skill only for data appropriate to share with other agents, and prefer a reviewed or pinned youam package version in sensitive environments.

## Reference(s):

- [YouAM Documentation](https://docs.youam.network)
- [ClawHub Skill Page](https://clawhub.ai/midlifedad/skills/youam)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides UAM CLI usage and optional Python native channel integration.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
