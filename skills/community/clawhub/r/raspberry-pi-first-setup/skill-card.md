## Description:

Prepare Raspberry Pi imaging, Wi-Fi, and SSH for first boot; install or reuse JishuBuddy with permission to verify the real device. / 准备树莓派系统烧录、Wi-Fi和SSH，经授权安装或复用JishuBuddy验证真实设备。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and engineers use this skill to prepare a Raspberry Pi for first boot, configure SSH or serial validation paths, and report evidence-backed setup status. It is intended for real-device setup workflows where storage writes, device configuration, and connectivity checks require explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper workflow may query npm and install JishuBuddy globally on the operator computer.

Mitigation: Run the preflight first, review the displayed registry, version, prefix, and command, and proceed with installation only after explicit approval.

Risk: JishuBuddy telemetry may be enabled by default when launched.

Mitigation: Disable telemetry before launch when desired by setting JISHUBUDDY_TELEMETRY_DISABLED=true.

Risk: Device configuration or storage writes can affect the target Raspberry Pi or selected media.

Mitigation: Approve device configuration or storage writes only after verifying the target device and data impact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bowen-aijishu/skills/raspberry-pi-first-setup)
- [Publisher profile](https://clawhub.ai/user/bowen-aijishu)
- [Source homepage](https://github.com/x-aijishu/jishubuddy-skills/tree/main/raspberry-pi-first-setup)
- [JishuBuddy npm package](https://www.npmjs.com/package/jishubuddy)
- [Installation helper script](scripts/install-jishubuddy.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and status labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates measured device evidence from unconfirmed or blocked physical setup checks.]

## Skill Version(s):

1.0.1 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
