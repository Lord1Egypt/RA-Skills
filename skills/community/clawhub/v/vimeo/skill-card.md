## Description:

Helps agents access Vimeo through a managed connection to upload and organize videos, manage showcases and folders, and interact with the Vimeo community.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams managing Vimeo videos use this skill to work with their connected account and, with explicit approval, configure related automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted functions can run unattended under the connected account.

Mitigation: Require user-reviewed code and explicit approval; limit the function to the intended connection and deny outbound network access unless specific hosts are approved.

Risk: Trigger destinations can continuously forward event data to an external host.

Mitigation: Confirm the exact account, source, destination host, data fields, and persistence with the user before enabling a destination; remove it when no longer needed.

## Reference(s):

- [Vimeo skill on ClawHub](https://clawhub.ai/byungkyu/skills/vimeo)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Vimeo API reference](https://developer.vimeo.com/api/reference)
- [Time trigger reference](artifact/references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses depend on the connected account and requested operation.]

## Skill Version(s):

1.2.5 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
