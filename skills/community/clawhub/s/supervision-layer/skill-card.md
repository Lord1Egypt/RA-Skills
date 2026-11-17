## Description:

Helps developers wrap async agent tool calls with timeouts, circuit breakers, audit logging, and crash-loop protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larios613-hub](https://clawhub.ai/user/larios613-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Supervision Layer to add local supervision around async agent tool calls, including timeouts, per-tool circuit breakers, audit logging, and crash-loop tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper is not a guaranteed non-bypassable security boundary.

Mitigation: Treat it as defense-in-depth and explicitly route every tool call through the supervision wrapper during integration review.

Risk: Audit and crash-loop records can persist sensitive data in local plaintext logs.

Mitigation: Avoid logging secrets or private prompts, and add redaction, retention, and file-permission controls before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/larios613-hub/skills/supervision-layer)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper can create local JSONL audit logs and crash-loop state files when integrated.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
