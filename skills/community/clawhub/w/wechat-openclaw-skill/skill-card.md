## Description:

Provides guidance and scripts for installing, binding, and operating a WeChat channel that connects users to an OpenClaw assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ynxiyan](https://clawhub.ai/user/ynxiyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to set up a WeChat integration, scan-bind an account, configure the OpenClaw WeChat channel, and troubleshoot message, file, and gateway connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation path uses an unpinned remote package version through `@latest`.

Mitigation: Use a pinned, reviewed package version and inspect the package before running installation commands.

Risk: WeChat messages and attachments can be routed into OpenClaw.

Mitigation: Use the integration only with trusted accounts, avoid secrets or regulated data, and disable `autoReply` and `autoAccept` unless a trusted sender allowlist is in place.

Risk: Running installer commands with elevated privileges can increase local system impact.

Mitigation: Run the installer as a normal user and review generated configuration changes before enabling the channel.

Risk: Gateway and network failures can interrupt installation or message routing.

Mitigation: Run the environment check, confirm the OpenClaw gateway is active, and verify access to WeChat and npm endpoints before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ynxiyan/skills/wechat-openclaw-skill)
- [OpenClaw WeChat channel documentation](https://docs.openclaw.ai/channels/weixin)
- [OpenClaw integration guide](https://docs.openclaw.ai/integration)
- [OpenClaw plugin documentation](https://docs.openclaw.ai/plugins)
- [Bilibili tutorial referenced by the skill](https://www.bilibili.com/video/BV1mdAgziEkh)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell, JSON, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, environment-check, binding, troubleshooting, and maintenance steps for OpenClaw and WeChat.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
