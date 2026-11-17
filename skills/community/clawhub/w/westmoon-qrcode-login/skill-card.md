## Description:

Starts a Westmoon QR-code login flow, displays the QR code, polls for confirmation, and saves access and refresh tokens plus user information for reuse by related Westmoon skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jader](https://clawhub.ai/user/jader)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to authenticate a Westmoon account by QR code before calling Westmoon APIs that require a valid bearer token. It is useful when a token is missing, expired, or needs to be refreshed for downstream Westmoon automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists reusable Westmoon access and refresh tokens for broad reuse by other skills.

Mitigation: Install only if the publisher and Westmoon API endpoint are trusted, treat ~/.westmoon-user-login/tokens.json as a sensitive credential file, and prevent untrusted skills from reading it.

Risk: The QR-code flow can automatically open remote-supplied image files with weak PNG validation.

Mitigation: Prefer manual review before implicit login flows, avoid automatic OS-handler opening by default, and validate PNG data strictly before displaying or opening it.

## Reference(s):

- [西之月扫码登录 API 速查](artifact/references/api_reference.md)
- [西之月扫码登录集成指南](artifact/references/integration_guide.md)
- [ClawHub skill page](https://clawhub.ai/jader/skills/westmoon-qrcode-login)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, API Calls, Guidance]

**Output Format:** [Markdown or terminal text with QR image file markers, data URIs, JSON token files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates QR image files and token or pending-login JSON under ~/.westmoon-user-login/.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact _meta.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
