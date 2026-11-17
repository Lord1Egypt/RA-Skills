## Description:

Use this skill when a security engineer, AppSec reviewer, or architect needs to threat-model a system, feature, or architecture change using STRIDE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers, AppSec reviewers, architects, and product security teams use this skill to turn a system or feature design into a STRIDE threat model for design review, security-architecture review, or pre-launch assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may disclose live secrets or sensitive architecture details while describing a system.

Mitigation: Describe secret types and storage locations instead of secret values, and limit system details to authorized review contexts.

Risk: The threat model may be incomplete or misleading when components, data flows, trust boundaries, assets, actors, tech stack, or topology are missing.

Mitigation: Require confirmed scoping inputs, record unresolved design details as open questions, and route the DRAFT report to security-architect review.

Risk: Mitigation recommendations are advisory and may not match implementation constraints or residual-risk decisions.

Mitigation: Have engineering owners and security reviewers validate recommended controls before sign-off.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown STRIDE threat-model report with tables, prioritized threats, mitigation backlog, and open questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is labeled DRAFT and is intended for security-architect review before sign-off.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
