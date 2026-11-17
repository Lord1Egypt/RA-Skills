## Description:

Telegram新设备登录 — 绕过PHONE_CODE_EXPIRED错误，用QR码扫描代替验证码，附脚本和完整流程

This skill is ready for commercial/non-commercial use.

## Publisher:

[polityang](https://clawhub.ai/user/polityang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to troubleshoot Telegram new-device login failures and generate a local QR-based Telethon login flow when phone-code authentication reports PHONE_CODE_EXPIRED.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram QR login URLs, QR images, and session files can expose account access if shared or stored insecurely.

Mitigation: Generate and display QR codes locally, keep session files private, delete temporary QR artifacts, and do not send QR login material to an assistant or chat.

Risk: Publishing instructions mention sharing GitHub PATs, ClawHub tokens, and other credentials.

Mitigation: Do not share access tokens with an assistant or chat; use local authentication flows and avoid unrelated publishing instructions when applying the Telegram workaround.

Risk: The server security verdict is suspicious because the workflow can expose account or platform credentials.

Mitigation: Audit and correct the workflow before installation or use, following the server-provided security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/polityang/skills/telegram-qr-login-workaround)
- [Telegram API credentials](https://my.telegram.org)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes procedural troubleshooting guidance and examples for generating and handling Telegram QR login artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
