## Description:

SSH remote connection and operation for servers (Linux/Unix cloud servers, etc.)

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingfalin](https://clawhub.ai/user/xingfalin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect to Linux/Unix servers over SSH, inspect system status and logs, and run common service or Docker administration commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using `StrictHostKeyChecking=no` can expose users to server impersonation and credential theft.

Mitigation: Verify and pin SSH host keys instead of using the documented unsafe connection option.

Risk: Privileged service, Docker, and log commands can disrupt servers or expose sensitive operational data.

Mitigation: Run these commands only on servers you control after confirming the target host, command, and expected impact.

Risk: Password-based SSH access and saved credentials increase credential exposure risk.

Mitigation: Prefer SSH key authentication, avoid direct root login where possible, and do not share passwords in chat.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xingfalin/skills/ssh-server)
- [ClawHub Publisher Profile](https://clawhub.ai/user/xingfalin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an SSH client binary and access to servers the user controls.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
