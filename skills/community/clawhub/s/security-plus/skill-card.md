## Description:

Enhanced security with OWASP Top 10, dependency scanning, SAST/DAST, secrets detection, compliance checks, and security hardening guides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill as a practical security reference for OWASP Top 10 mitigations, vulnerability scanning, secrets detection, compliance checks, and server, application, and database hardening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example scanner and audit commands may change dependencies or test live systems if run without review.

Mitigation: Pin tool versions where possible, review changes from npm audit fix, and run scanners only against systems you are authorized to test.

Risk: Running external security tools with production credentials present may expose sensitive data.

Mitigation: Run tools in a controlled environment and avoid using production credentials during scans.

## Reference(s):

- [detect-secrets](https://github.com/Yelp/detect-secrets)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes checklists, tool references, mitigation tables, and example commands; users should review commands before execution.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
