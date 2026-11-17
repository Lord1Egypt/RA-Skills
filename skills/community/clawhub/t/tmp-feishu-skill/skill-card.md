## Description:

Guides users through creating a Feishu bot, connecting it to OpenClaw, and binding it to a dedicated Agent in a Windows environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[song123-wq](https://clawhub.ai/user/song123-wq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Feishu bot integrations for OpenClaw, split bots by role, and validate message routing to dedicated Agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes unrelated agent-identity and user-addressing instructions.

Mitigation: Review and remove persona lines before installing or adapting the skill.

Risk: The setup flow handles Feishu App Secret values and local configuration paths.

Mitigation: Store secrets only in secure configuration locations, avoid pasting them into chats or committed files, and validate Agent IDs with a strict lowercase letters, digits, and hyphen pattern.

Risk: Restarting the OpenClaw gateway can briefly interrupt service.

Mitigation: Restart the gateway only during an acceptable maintenance window or when a brief interruption is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/song123-wq/skills/tmp-feishu-skill)
- [Feishu Open Platform OpenClaw app creation](https://open.feishu.cn/page/openclaw?form=multiAgent)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with PowerShell command blocks and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Windows-specific OpenClaw paths and credential-handling guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
