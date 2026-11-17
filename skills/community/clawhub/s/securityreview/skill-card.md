## Description:

Security code review guides agents through read-only source-code security audits focused on direct, actionable evidence of vulnerabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylehuan](https://clawhub.ai/user/kylehuan)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to direct an agent through structured SAST-style code review and produce clear vulnerability reports with severity, evidence, impact, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to inspect repository files during security reviews.

Mitigation: Use it only in workspaces where read-only repository inspection is authorized.

Risk: Some workflows may create security report artifacts under .shield_security/.

Mitigation: Confirm that report artifact creation is acceptable before invoking artifact-producing workflows.

Risk: The artifact contains vulnerable code snippets and risky-looking strings as examples.

Mitigation: Treat examples as review guidance only; do not execute sample vulnerable snippets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kylehuan/skills/securityreview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with vulnerability findings, evidence, severity, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read-only inspection commands and, when explicitly requested by the user, report artifacts under .shield_security/.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
