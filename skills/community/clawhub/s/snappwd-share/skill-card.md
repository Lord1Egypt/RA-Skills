## Description:

Securely share secrets, API keys, files, and credentials with OpenClaw agents and team members via self-destructing links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fantaclaw-ai](https://clawhub.ai/user/fantaclaw-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and OpenClaw users use this skill to create one-time links for sharing secrets, credentials, and sensitive files without pasting raw values into chat or email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed for secret sharing and may encourage users to share durable credentials such as SSH private keys, whole .env files, credential bundles, or long-lived production tokens.

Mitigation: Prefer scoped temporary credentials, verify recipients out of band, avoid placing secrets directly on command lines, and rotate or revoke any credential that is shared.

Risk: Anyone with a generated link can retrieve the secret once, and compromised client devices or phishing pages remain outside the protection provided by encrypted storage.

Mitigation: Confirm the SnapPwd domain or approved self-hosted endpoint before entering secrets, share links only through intended channels, and avoid creating or opening secrets on untrusted devices.

Risk: The CLI path depends on an external npm package and may expose secrets through shell history when secrets are passed as command arguments.

Mitigation: Pin and verify the CLI package when used, prefer stdin or the web interface for sensitive values, and avoid command-line arguments for high-value secrets.

## Reference(s):

- [SnapPwd CLI Usage](references/cli-usage.md)
- [SnapPwd Security Model](references/security-model.md)
- [SnapPwd Web Interface](https://snappwd.io)
- [SnapPwd GitHub](https://github.com/SnapPwd/SnapPwd)
- [SnapPwd Service](https://github.com/SnapPwd/snappwd-service)
- [SnapPwd CLI](https://github.com/SnapPwd/snappwd-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct users to a web interface or CLI that outputs self-destructing secret-sharing links.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-03-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
