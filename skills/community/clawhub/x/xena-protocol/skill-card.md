## Description: <br>
Xena Protocol scans a user's Gmail inbox for phishing, crypto scams, impersonation, and business email compromise, with an optional Reporter mode that submits hashed detections to an Ethereum Sepolia registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickvanzo](https://clawhub.ai/user/nickvanzo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor Gmail for suspicious messages, triage phishing signals, and optionally publish hashed threat reports to a shared Sepolia registry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Gmail inbox state during background scans. <br>
Mitigation: Grant Gmail OAuth access only for accounts where background phishing scans and unread-state changes are acceptable. <br>
Risk: Reporter mode can automatically publish Sepolia blockchain reports. <br>
Mitigation: Use Watcher mode unless automatic blockchain reporting is explicitly desired, and review setup choices before enabling Reporter mode. <br>
Risk: The generated reporting wallet key is stored locally and should not protect other assets. <br>
Mitigation: Do not reuse the generated wallet or fund it beyond the Sepolia test ETH needed for reporting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickvanzo/xena-protocol) <br>
- [Publisher profile](https://clawhub.ai/user/nickvanzo) <br>
- [Project homepage](https://github.com/NickVanzo/royal-hackathon-itu) <br>
- [OpenClaw package](https://www.npmjs.com/package/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-derived alert details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide OAuth setup, local wallet setup, inbox scanning, and optional Sepolia registry reporting.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
