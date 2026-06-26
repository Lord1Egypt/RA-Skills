## Description: <br>
Connects a personal WeChat account through OpenClaw with a QR-code login flow, credential setup, and gateway restart; it is not for enterprise WeChat or WeCom. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EaseLearnAI](https://clawhub.ai/user/EaseLearnAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to bind a personal WeChat account to OpenClaw via QR-code login and save returned account credentials for the Weixin extension. It should not be used for enterprise WeChat or WeCom connections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A short-lived personal WeChat login QR image may be uploaded to an unspecified CDN. <br>
Mitigation: Use only with clear user consent, prefer a local-only QR display path when possible, and delete any uploaded or backup QR image after login completes or expires. <br>
Risk: The flow persists account tokens under the user's home directory with limited user control described in the artifact. <br>
Mitigation: Review the credential path and file permissions before use, keep the token out of logs and shared workspaces, and provide cleanup or revocation steps after testing or account changes. <br>
Risk: The skill installs and runs npm-based tooling before connecting the account. <br>
Mitigation: Install only in an environment where the npm installer and Weixin extension are trusted, and review package provenance before using the connected account. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/EaseLearnAI/weixin-connect) <br>
- [Weixin iLink QR Code API](https://ilinkai.weixin.qq.com/ilink/bot/get_bot_qrcode?bot_type=3) <br>
- [Weixin iLink QR Status API](https://ilinkai.weixin.qq.com/ilink/bot/get_qrcode_status?qrcode=<qrcode>) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate a QR image file and write local account credential JSON files during execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
