## Description:

Helps agents manage Unbounce landing pages and leads through a connected account, with optional scheduled or event-driven automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and developers use this skill to retrieve leads and manage Unbounce landing pages through an authorized connection; they can also configure related automations with separate approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overbroad account access or unapproved changes to landing pages and leads.

Mitigation: Use the minimum needed OAuth scopes and confirm each write or new connection with the user.

Risk: Automations or third-party destinations could forward lead data continuously.

Mitigation: Review trigger destinations and ongoing data flow; approve each automation step separately.

Risk: Exposed Maton credentials could permit unauthorized access.

Mitigation: Keep API keys and stored credentials private; never embed them in destinations or output.

## Reference(s):

- [ClawHub Unbounce skill release](https://clawhub.ai/byungkyu/skills/unbounce)
- [Unbounce API documentation](https://developer.unbounce.com/api_reference/)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with commands and API response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authorized reads, writes, and automation setup for a connected account.]

## Skill Version(s):

1.2.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
