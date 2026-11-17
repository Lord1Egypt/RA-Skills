## Description:

Biometric guardrail for OpenClaw that intercepts dangerous tool calls and requires Face ID authorization through the TruClaw iOS app before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanjaymk908](https://clawhub.ai/user/sanjaymk908)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw operators use this skill to require phone-based biometric authorization before high-risk agent tool calls such as write, delete, network, install, messaging, financial, process, and permission-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent privileged hook that can inspect tool-call arguments and affect execution.

Mitigation: Review and pin the exact plugin source before installing, and prefer testing in an isolated environment before using it in higher-impact workflows.

Risk: Tool names and arguments may be sent to external services while privacy and approval details are under-specified.

Mitigation: Be comfortable with data sent to Anthropic, consider self-hosting the relay, and avoid secrets, private file contents, or high-impact automation until authorization JWT claims and data minimization behavior are documented and verifiable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanjaymk908/skills/truclaw-biometric)
- [Project homepage](https://github.com/sanjaymk908/trukyc-openclaw)
- [Plugin source](https://github.com/sanjaymk908/trukyc-openclaw/tree/main/)
- [Relay source](https://github.com/sanjaymk908/trukyc-openclaw/tree/main/cloudflare-worker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide installation, pairing, self-hosting, and risk-review guidance for an OpenClaw plugin.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
