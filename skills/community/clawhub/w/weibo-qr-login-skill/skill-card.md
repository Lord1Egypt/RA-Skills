## Description: <br>
Fetches a Weibo login QR code through OpenClaw browser integration and guides the agent through cookie restore, QR login, and session persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fmls](https://clawhub.ai/user/fmls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs to log in to Weibo by restoring saved cookies or presenting a fresh QR code for scanning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes global OpenClaw browser and tool configuration and may restart the gateway. <br>
Mitigation: Run it only in an isolated OpenClaw environment where those configuration changes and a gateway restart are acceptable. <br>
Risk: The skill stores reusable Weibo session cookies locally. <br>
Mitigation: Review the scripts before use and delete ~/.openclaw/data/weibo/cookies.json and meta.json when the session should no longer be preserved. <br>
Risk: The cookie export path can expose cookie values as shell commands. <br>
Mitigation: Avoid the export command unless explicitly needed and handle any exported cookie values as sensitive credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fmls/weibo-qr-login-skill) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>
- [Weibo sign-in page](https://passport.weibo.com/sso/signin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and an optional local QR image path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit a MEDIA line for the QR image path and stores Weibo session cookies locally after successful login.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
