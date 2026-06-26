## Description: <br>
西之月登录 uses a QR-code login flow to obtain, validate, and save Westmoon access and refresh tokens for reuse by related automation skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jader](https://clawhub.ai/user/jader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a Westmoon workflow needs a valid user login state. It shows a QR code, polls for scan confirmation, validates the session, and stores reusable tokens locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable Westmoon account tokens locally for other Westmoon skills to read. <br>
Mitigation: Keep QR output and session logs private, do not sync or share ~/.westmoon-user-login, and use the logout command to remove saved tokens when reuse is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jader/westmoon-qrcode-login) <br>
- [西之月扫码登录 API 速查](references/api_reference.md) <br>
- [西之月扫码登录集成指南](references/integration_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown or terminal text with QR-code file paths, data URI output, status JSON, and saved local token files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates QR images, pending-login state, and reusable token JSON under ~/.westmoon-user-login.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
