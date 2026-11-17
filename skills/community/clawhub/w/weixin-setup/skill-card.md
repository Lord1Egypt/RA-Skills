## Description:

Install and connect the WeChat ClawBot channel plugin for OpenClaw, including a qrcode-terminal patch that emits scannable QR image URLs for chat surfaces where ASCII QR codes are unreliable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaojiankui](https://clawhub.ai/user/shaojiankui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install, connect, verify, and troubleshoot the WeChat ClawBot channel in OpenClaw. It is intended for workflows where WeChat login, QR-code scanning, accountId repair, and optional per-account session isolation need step-by-step command guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow exposes WeChat login QR contents to a third-party QR service.

Mitigation: Prefer local QR rendering that keeps QR contents inside the controlled OpenClaw environment.

Risk: The patch persistently rewrites the installed qrcode-terminal dependency.

Mitigation: Review the patch before use, keep the generated backup, and be prepared to restore the backup or reinstall the plugin after testing.

Risk: The install command uses the latest plugin release instead of a pinned version.

Mitigation: Prefer a version-pinned installer when reproducibility or change control matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaojiankui/skills/weixin-setup)
- [Third-party QR image service used by the patch](https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational setup, verification, troubleshooting, and patch guidance for an existing OpenClaw installation.]

## Skill Version(s):

5.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
