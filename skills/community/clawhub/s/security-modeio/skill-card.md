## Description:

Runs a backend-backed live safety check for instructions that may trigger tool execution, external calls, file edits, permission changes, destructive or irreversible actions, prompt injection, or compliance-sensitive operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modeioai](https://clawhub.ai/user/modeioai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before executing side-effecting instructions to get a safety decision for destructive actions, permission changes, external calls, file edits, prompt injection risk, and compliance-sensitive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operation details are sent to an external safety backend and may include sensitive instruction, context, or target data.

Mitigation: Avoid sending secrets in instruction, context, or target fields, and review use before applying the skill to regulated or production workflows.

Risk: The backend URL is configurable, so a process environment change could redirect safety decisions to an untrusted endpoint.

Mitigation: Keep SAFETY_API_URL unset or locked to a trusted HTTPS endpoint and control the process environment.

Risk: The returned safety decision is advisory unless the caller enforces it.

Mitigation: Use a fail-closed caller policy for dependency, network, and API errors, and require explicit confirmation or acknowledgement for higher-risk denials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modeioai/skills/security-modeio)
- [Project homepage](https://github.com/mode-io/mode-io-skills/tree/main/security)
- [Architecture](ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON safety decision envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns approval, risk level, concerns, recommendations, or normalized error information.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
