## Description:

Sanna governance makes AI agent tool calls governed transparently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicallen-exd](https://clawhub.ai/user/nicallen-exd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to apply constitution-based governance to tool calls, allowing, blocking, or escalating actions for human approval. It also records Ed25519-signed receipts for governed actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required third-party governance plugin can observe and control high-impact tool calls.

Mitigation: Review the plugin before installation and run it with least-privilege runtime limits.

Risk: The required plugin version is not pinned in the artifact metadata.

Mitigation: Pin and review a specific plugin version before deployment.

Risk: Governed actions automatically persist receipts, which may affect data retention expectations.

Mitigation: Document receipt storage, retention, deletion behavior, and any network endpoints before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicallen-exd/skills/sanna-governance)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Text decisions and receipt records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and the @sanna-ai/openclaw plugin.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
