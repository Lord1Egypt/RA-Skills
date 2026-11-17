## Description:

Helps agents use WATI to find contacts and templates, send WhatsApp messages, and set up approved automations through Maton.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to access WATI contacts and message templates, send user-approved WhatsApp messages, and configure related automations through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sending messages or changing contacts can affect real recipients and personal data.

Mitigation: Confirm the recipient or contact, content, and intended change with the user before each write.

Risk: Connections, functions, triggers, and destinations can enable ongoing account access or automatic actions.

Mitigation: Get explicit approval for each connection or automation and confirm its event scope and destination.

Risk: Credentials and WATI responses may expose account access or personal information.

Mitigation: Prefer Maton login over raw API keys and handle only the response fields needed for the task.

## Reference(s):

- [WATI API documentation](https://docs.wati.io/reference/introduction)
- [Maton homepage](https://maton.ai)
- [Maton API reference](https://docs.maton.ai/api-reference/overview)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with commands, code, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account access and write actions require user authorization.]

## Skill Version(s):

1.2.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
