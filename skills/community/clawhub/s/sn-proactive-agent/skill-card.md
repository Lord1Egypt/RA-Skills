## Description:

安装、启动和使用 Proactive Agent，记录项目进展并在合适时机提醒下一步。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

开发者可按操作系统和对话平台安装、配置 Proactive Agent，以整理项目进展、查看提醒建议，并在确认后从原会话继续工作。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected conversation records are stored locally, processed by the configured model service, and remain after uninstall.

Mitigation: Enable only if this storage and processing are acceptable; explicitly request deletion when records should be removed.

Risk: Suggested follow-ups may lead to actions when accepted.

Mitigation: Review each suggested action before accepting it.

Risk: The runtime and plugin code are downloaded separately and are not included with this skill artifact.

Mitigation: Verify release checksums before installing downloaded files.

## Reference(s):

- [安装与运行](references/install/overview.md)
- [macOS 安装说明](references/install/macos.md)
- [Windows 安装说明](references/install/windows.md)
- [Hermes 接入](references/connectors/hermes.md)
- [OpenClaw 接入](references/connectors/openclaw.md)
- [Hermes 官方安装说明](https://hermes-agent.nousresearch.com/docs/getting-started/installation/)
- [pipx 安装说明](https://pipx.pypa.io/stable/how-to/install-pipx.html)
- [pipx 路径配置说明](https://pipx.pypa.io/latest/how-to/configure-paths.html)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OS- and conversation-platform-specific instructions]

## Skill Version(s):

2026.10.29 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
