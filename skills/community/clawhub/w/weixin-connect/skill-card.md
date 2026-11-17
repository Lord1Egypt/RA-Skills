## Description:

Connects an agent workflow to a personal WeChat account by guiding QR-code login, credential storage, and OpenClaw gateway restart; it is not intended for WeCom or enterprise WeChat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easelearnai](https://clawhub.ai/user/easelearnai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect a personal WeChat account to OpenClaw through a QR-code login workflow. It helps distinguish personal WeChat connection requests from enterprise WeChat or WeCom requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow installs remote packages during execution.

Mitigation: Review and pin dependencies before use in managed environments.

Risk: The workflow may temporarily host a live WeChat login QR code remotely.

Mitigation: Prefer local-only QR display or require explicit approval before remote upload.

Risk: The workflow persists WeChat connection tokens on local storage.

Mitigation: Require explicit approval before credential writes and protect stored credential files with restricted permissions.

Risk: The workflow restarts the OpenClaw gateway.

Mitigation: Confirm service restart timing and operational impact before running the restart step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/easelearnai/skills/weixin-connect)
- [EaseLearnAI publisher profile](https://clawhub.ai/user/easelearnai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files, API calls]

**Output Format:** [Markdown with inline shell commands and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a QR-code login workflow, local credential files, and gateway restart guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
