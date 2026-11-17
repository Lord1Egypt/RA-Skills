## Description:

Sendflare lets an agent send email through a configured Sendflare account and exposes experimental contact-management commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keepchen](https://clawhub.ai/user/keepchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to send email from a Sendflare account with natural-language commands. Contact list actions are exposed but should be treated as experimental or incomplete in this version.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send email immediately after parsing a command.

Mitigation: Review recipients, subject lines, and message bodies carefully before asking the agent to send.

Risk: Messages may contain secrets, personal data, or regulated information that would be processed by Sendflare.

Mitigation: Avoid placing sensitive or regulated data in messages unless that processing is acceptable for the account and use case.

Risk: Contact-management commands are unreliable or incomplete in this version.

Mitigation: Treat contact actions as experimental and verify contact state in Sendflare before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keepchen/skills/sendflare-skill)
- [Sendflare](https://Sendflare.com)
- [Sendflare Node.js SDK documentation](https://docs.Sendflare.com/docs/sdk/nodejs/)
- [Sendflare API documentation](https://docs.Sendflare.com/)

## Skill Output:

**Output Type(s):** [text, guidance, API calls]

**Output Format:** [Plain text status messages with optional suggested actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send email through the configured Sendflare account; contact-management commands may return setup or limitation guidance.]

## Skill Version(s):

1.0.7 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
