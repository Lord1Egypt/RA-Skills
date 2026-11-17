## Description:

Performs structured security audits of codebases, infrastructure configuration, API designs, and architecture documents, producing prioritized findings with severity ratings and remediation recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leewest0](https://clawhub.ai/user/leewest0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and security reviewers use this skill to assess source code, infrastructure-as-code, cloud configuration, API design, dependencies, and architecture for security risks. It helps produce full audit reports, quick assessments, or executive summaries with severity, evidence, impact, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases such as "audit this" may route a general review request into a security-focused assessment.

Mitigation: Confirm the intended review scope when the user's request is ambiguous, especially when they may want general code quality feedback rather than a security audit.

Risk: Security-audit findings and remediation guidance can be incomplete or incorrect without project-specific deployment, threat-model, and compliance context.

Mitigation: Have qualified reviewers validate high-impact findings and remediation steps before applying changes in production.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown security audit report with findings, severity ratings, evidence, impact, and remediation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include code examples, authoritative security references, compliance mappings, and executive-summary prose when requested.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
