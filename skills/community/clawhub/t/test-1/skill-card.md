## Description:

Provides QQ group administration guidance and shell commands for calling the napcat OneBot 11 API to change group names, post announcements, mute or unmute members, remove members, manage admins, toggle whole-group mute, update cards or titles, recall messages, and query group information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to perform QQ group administration through a local or approved OneBot-compatible service. It is intended for tasks such as announcements, moderation actions, group configuration updates, message recall, and group/member information lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled dispatcher can invoke broad OneBot administration actions, including sensitive moderation and group configuration changes.

Mitigation: Use the skill only with a dedicated low-privilege OneBot instance and require explicit human confirmation before sensitive actions such as kicking, muting, admin changes, group-wide mute, or message recall.

Risk: The release evidence reports a hardcoded fallback token.

Mitigation: Remove the bundled fallback token before deployment and supply a rotated token through the environment.

Risk: The release evidence reports a local-file-to-WebSocket data path through @/path inputs.

Mitigation: Do not allow untrusted prompts or users to choose action names, parameters, or @/path file inputs; restrict allowed file paths and parameters before execution.

Risk: The helper connects to a WebSocket endpoint for administrative actions.

Mitigation: Restrict the endpoint to a trusted local service or an approved wss:// server.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/test-1)
- [Publisher profile](https://clawhub.ai/user/yinwuzhe)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute OneBot API actions through a Node.js WebSocket helper when used by an agent with shell access.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
