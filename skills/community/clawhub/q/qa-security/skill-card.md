## Description:

Code quality audit guidance, security review, vulnerability identification patterns, and dependency risk assessment with AI-delivered service access via clawtip verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinyu12166](https://clawhub.ai/user/jinyu12166)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use qa-security to request code quality audits, security review guidance, vulnerability pattern analysis, dependency risk assessment, and testing strategy suggestions after completing the clawtip payment workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid clawtip workflow with credential access, network permission, persistent local order files, and external payment tooling.

Mitigation: Install only when that payment and permission posture is acceptable for the environment, and review the payment flow before use.

Risk: The local payment verification is weak according to the security guidance.

Mitigation: Treat payment authorization as low-assurance until the publisher strengthens credential validation and dependency integrity.

Risk: The initial question may contain sensitive project details, source code, or secrets.

Mitigation: Avoid including secrets, source code, credentials, or sensitive project information in the initial consultation question.

## Reference(s):

- [qa-security ClawHub skill page](https://clawhub.ai/jinyu12166/skills/qa-security)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and payment status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid clawtip workflow; order metadata is written locally before service authorization.]

## Skill Version(s):

1.0.27 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
