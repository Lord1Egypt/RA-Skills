## Description:

Store and retrieve website credentials for domain, username, password, and notes entries with Ravi password-manager commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raunaksingwi](https://clawhub.ai/user/raunaksingwi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, list, retrieve, update, delete, and generate website credentials through Ravi password-manager commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Password command outputs may expose plaintext credentials in transcripts, screenshots, logs, copied snippets, or shell history.

Mitigation: Avoid sharing command output and clear or suppress terminal history and logs that may contain returned passwords.

Risk: The skill is intended for website credentials, not API keys, secrets, or inbox messages.

Mitigation: Use ravi-secrets for API keys and environment secrets, and use ravi-inbox for message-reading workflows.

## Reference(s):

- [Passwords API Reference](https://ravi.id/docs/schema/passwords.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include plaintext passwords and should be treated as sensitive.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
