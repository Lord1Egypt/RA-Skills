## Description:

Install and configure the security-related plugins required by OpenClaw, including the `ai-assistant-security-openclaw` plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinjianfenghzau-wq](https://clawhub.ai/user/qinjianfenghzau-wq)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to install ClawSentry and the `ai-assistant-security-openclaw` plugin, complete login authorization, and configure local OpenClaw plugin settings for security monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer stores login state and may log credential-bearing authorization responses locally.

Mitigation: Review before installing, use restricted file permissions, and prefer a release that redacts logs before writing authorization responses.

Risk: The skill installs a remote plugin, writes service credentials into OpenClaw configuration, and restarts the OpenClaw gateway.

Mitigation: Confirm the plugin package, expected configuration changes, and post-authorization gateway restart before running it on a machine.

Risk: Credential values may be exposed through shell-interpolated configuration commands or local process/audit tooling.

Mitigation: Prefer a version-pinned installer that avoids shell-interpolated configuration updates and clearly reports the changes it made.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qinjianfenghzau-wq/skills/testdhdb)
- [Volcengine product site](https://www.volcengine.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and login URL text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a login URL and post-authorization verification guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
