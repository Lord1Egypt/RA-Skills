## Description: <br>
小红书 MCP 登录流程，当用户需要登录小红书、登录过期或需要获取小红书登录二维码时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fe-room](https://clawhub.ai/user/fe-room) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check Xiaohongshu login status, retrieve and display a login QR code, and reset cookies when re-login is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Xiaohongshu login QR codes, which can grant account access if exposed or sent to an unintended recipient. <br>
Mitigation: Prefer local display of the QR code and allow external messaging delivery only when the user explicitly requests the destination. <br>
Risk: Cookie deletion resets the Xiaohongshu session and requires a fresh login. <br>
Mitigation: Treat cookie deletion as an explicit logout or reset action and confirm intent before running it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fe-room/xiaohongshu-login) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown with bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent through MCP calls, QR-code extraction, local image display, optional message delivery, and cookie deletion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
