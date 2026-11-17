## Description:

Manage and secure local high-privilege storage serving workflows for creating, starting, stopping, or hardening a full-drive file server and related operational controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manlight87](https://clawhub.ai/user/manlight87)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run a local high-privilege storage manager with token authentication, loopback binding, directory listing, file reading, and binary download workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes a local high-privilege file server with broad default root access.

Mitigation: Use a narrow GOD_MODE_ROOT instead of a full drive, keep GOD_MODE_HOST on 127.0.0.1, and run only when this local file-serving workflow is intentionally required.

Risk: Authentication and UI handling weaknesses could expose sensitive files or tokens.

Mitigation: Use a strong unique token, keep token authentication enabled, avoid putting tokens in URLs, rotate tokens if shared in logs, and patch UI rendering and symlink containment issues before handling sensitive files.

## Reference(s):

- [Ops Runbook](references/ops.md)
- [ClawHub Skill Page](https://clawhub.ai/manlight87/skills/telegrambot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local server run commands, environment variable settings, operational checks, and risk guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
