## Description:

小红书 MCP 登录流程。当用户需要登录小红书、小红书登录过期、或需要获取小红书登录二维码时使用此 skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fe-room](https://clawhub.ai/user/fe-room)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check Xiaohongshu MCP login status, fetch a login QR code, display it to the user, and reset stored cookies when re-login is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The login QR code can grant access to the user's Xiaohongshu account.

Mitigation: Use the skill only with a trusted MCP service and trusted messaging destination, and require explicit confirmation before sending the QR code outside the local session.

Risk: The QR code is saved to a predictable local file path.

Mitigation: Prefer a temporary private file location and automatically delete the QR image after login is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fe-room/skills/xiaohongshu-login)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local PNG login QR code and optionally send it through Feishu.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
