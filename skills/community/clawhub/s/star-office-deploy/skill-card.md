## Description:

Star Office UI 一键部署技能 — 帮主人快速部署像素办公室看板，支持多 Agent 加入、状态可视化、移动端查看与公网访问

This skill is ready for commercial/non-commercial use.

## Publisher:

[iiustrator](https://clawhub.ai/user/iiustrator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to deploy and configure a Star Office UI pixel-office dashboard for multi-agent status visibility, mobile viewing, public access, and optional Gemini image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable third-party Star Office UI code.

Mitigation: Review or pin the external code before installation, and install dependencies only after confirming the source and requirements.

Risk: The dashboard can expose local agent data publicly through tunneling or weak default access controls.

Mitigation: Change the default password and join keys before sharing access, avoid public tunneling unless strong access controls are added, and confirm memory-note display is safe.

Risk: Optional Gemini image generation may send API keys or prompts to a third-party service.

Mitigation: Use dedicated credentials, avoid prompts containing secrets, and enable the feature only when third-party processing is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iiustrator/skills/star-office-deploy)
- [Star Office UI repository referenced by the artifact](https://github.com/ringhyacinth/Star-Office-UI.git)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment steps, access reminders, optional API-key setup guidance, and security configuration notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
