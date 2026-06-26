## Description: <br>
Helps agents install and troubleshoot the Weixin personal-account login flow for OpenClaw, including QR authorization links, scan-status polling, and local token-state checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aqHi](https://clawhub.ai/user/aqHi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect a Weixin personal account to OpenClaw, retrieve a browser-friendly QR authorization URL, poll login status, and diagnose cases where OpenClaw still reports SETUP or no token after the Weixin side confirms login. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles login URLs, qrcode values, bot tokens, ilink_user_id values, terminal output from polling, and files under ~/.openclaw/openclaw-weixin/ that may expose account access or identity data. <br>
Mitigation: Treat those values and files as secrets; redact them from chats, tickets, logs, screenshots, and repositories. <br>
Risk: The server security verdict is suspicious because the artifact does not clearly warn users that these login and account values are sensitive. <br>
Mitigation: Review the skill before installing and use it only when the Tencent Weixin OpenClaw package and this login workflow are trusted. <br>


## Reference(s): <br>
- [Implementation notes](references/implementation-notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/aqHi/weixin-openclaw-login) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell, JavaScript, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce QR login URLs, qrcode values, scan-status JSON, bot tokens, account identifiers, and local OpenClaw state-file paths that should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
