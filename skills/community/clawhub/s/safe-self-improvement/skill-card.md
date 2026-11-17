## Description:

Safe Self-Improvement logs agent learnings, errors, and corrections for OpenClaw with human approval gates, sanitization, audit tooling, and promotion rate limiting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gateswell](https://clawhub.ai/user/gateswell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to capture sanitized local learning, error, and feature-request records so future sessions can review recurring issues and propose approved improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically stores conversation and error learnings for future sessions.

Mitigation: Use it only in low-sensitivity personal workspaces, review .learnings regularly, and avoid logging raw user text or command output.

Risk: The promotion gate includes a force command that can bypass the normal approval model.

Mitigation: Remove or disable the force command before relying on the promotion approval model.

Risk: Shared or high-sensitivity environments may require stronger controls than local learning files provide.

Mitigation: Do not use it for financial, medical, critical infrastructure, or shared environments without stronger human-controlled storage and review.

## Reference(s):

- [Safe Self-Improvement on ClawHub](https://clawhub.ai/gateswell/skills/safe-self-improvement)
- [Safe Self-Improvement Agent Repository](https://github.com/gateswell/safe-self-improvement-agent)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Original Self-Improving Agent](https://github.com/peterskoett/self-improving-agent)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown log entries and concise guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local .learnings markdown files after sanitization; proposes promotions for human approval.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
