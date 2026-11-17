## Description:

Runs a backend-backed live safety check for instructions that may trigger tool execution, external calls, file edits, permission changes, destructive or irreversible actions, prompt injection, or compliance-sensitive operations before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modeioai](https://clawhub.ai/user/modeioai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to request a live safety decision before executing instructions that may change state or trigger external effects. It is intended for pre-execution operation checks, not repository auditing, read-only chat, or content masking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instruction text, context, and target identifiers are sent to a configured safety backend.

Mitigation: Use the skill only when that backend is approved to receive those details, and avoid sending secrets unless organizational policy permits it.

Risk: The CLI returns a safety decision but does not enforce the caller's policy.

Mitigation: Have the calling agent enforce the returned approved and risk_level fields, and do not proceed silently after dependency, network, or API errors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modeioai/skills/security-2)
- [Project homepage](https://github.com/mode-io/mode-io-skills/tree/main/security)
- [Architecture](artifact/ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [JSON, guidance]

**Output Format:** [JSON success or error envelope, or pretty-printed JSON with a status line in non-JSON mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes backend-provided approval and risk details when available; caller must enforce the returned decision.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
