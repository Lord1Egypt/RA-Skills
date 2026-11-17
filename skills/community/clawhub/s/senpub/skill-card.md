## Description:

Install and configure the security-related plugins required by OpenClaw, including the `ai-assistant-security-openclaw` plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiger-xzp](https://clawhub.ai/user/tiger-xzp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install ClawSentry security plugins, start the login flow, and apply the resulting OpenClaw plugin configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Login and credential material may be stored in local state or exposed through local logs, configuration, process arguments, or audit tooling.

Mitigation: Install only on a machine where that exposure is acceptable, restrict access to the skill state and OpenClaw configuration files, and rotate credentials if local exposure is suspected.

Risk: The skill links the machine to a remote service and installs a remote plugin without pinned package integrity in the provided evidence.

Mitigation: Verify the publisher profile, login URL, service endpoint, and installed plugin identity before completing authorization or using the configured plugin.

Risk: The installer updates local OpenClaw plugin configuration and restarts the OpenClaw gateway, and evidence.security warns that unsafe cleanup or configuration paths could delete unintended files if inputs are compromised.

Mitigation: Back up important OpenClaw state before installation, review the planned configuration changes, and run from a least-privileged account or disposable environment when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tiger-xzp/skills/senpub)
- [Volcengine website](https://www.volcengine.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and a user-facing login URL after script execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may guide an agent to run a bundled Node.js installer that changes local OpenClaw plugin configuration.]

## Skill Version(s):

1.0.21 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
