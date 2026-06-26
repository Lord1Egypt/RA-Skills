## Description: <br>
Helps agents guide users through one-time sharing of secrets, credentials, and sensitive files with SnapPwd secure links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fantaclaw-ai](https://clawhub.ai/user/fantaclaw-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill when they need to share passwords, API keys, tokens, configuration files, or private key material without pasting the raw secret into chat or email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages sharing high-value credentials through a third-party service. <br>
Mitigation: Use it only for explicit one-time sharing with verified recipients, prefer temporary or scoped credentials, and rotate or revoke sensitive credentials after sharing. <br>
Risk: Anyone with a generated secure link can access the secret once. <br>
Mitigation: Share links only through intended channels and verify the recipient before sending. <br>
Risk: Sharing raw long-lived private keys or credentials can create lasting exposure if the recipient or client device is compromised. <br>
Mitigation: Avoid raw long-lived private keys where possible and prefer short-lived, scoped, or revocable credentials. <br>


## Reference(s): <br>
- [SnapPwd CLI Usage](references/cli-usage.md) <br>
- [SnapPwd Security Model](references/security-model.md) <br>
- [SnapPwd Web Interface](https://snappwd.io) <br>
- [SnapPwd GitHub](https://github.com/SnapPwd/SnapPwd) <br>
- [SnapPwd Service](https://github.com/SnapPwd/snappwd-service) <br>
- [SnapPwd CLI](https://github.com/SnapPwd/snappwd-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and secure-sharing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct users to the SnapPwd web interface or CLI and may produce one-time sharing commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
