## Description:

Send messages to various webhook-based bots and notification services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[takedwind](https://clawhub.ai/user/takedwind)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation agents use this skill to send selected notification text to configured webhook-based chat bots and notification services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message content can be sent to external bot and notification services.

Mitigation: Use approved destinations only, verify recipients before sending, and avoid confidential or regulated content unless the destination is authorized.

Risk: Webhook keys, bot tokens, secrets, chat IDs, and full webhook URLs are sensitive credentials.

Mitigation: Store credentials in controlled secret storage, pass them only at execution time, and avoid logging or committing them.

Risk: Custom or user-provided URLs can direct messages to unintended endpoints.

Mitigation: Prefer tightly controlled destination URLs or allowlisted services when deploying the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/takedwind/skills/webhook-robot)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [shell commands, text, guidance]

**Output Format:** [Markdown with inline shell command examples and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and user-provided webhook keys, bot tokens, chat IDs, or destination URLs.]

## Skill Version(s):

1.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
