## Description:

Review code changes for security vulnerabilities, including OWASP Top 10 issues, secrets exposure, injection flaws, authentication issues, and insecure defaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to review PRs, commits, or code diffs for common security vulnerabilities and receive prioritized findings with concrete fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to inspect source files that contain secrets or sensitive code.

Mitigation: Use normal repository-sharing controls and avoid exposing repositories or files the reviewing agent should not read.

Risk: Security fix examples may need project-specific validation before they are applied.

Mitigation: Have a qualified reviewer confirm findings and proposed fixes against the application's authentication, authorization, and business-logic requirements.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown findings with severity, file location, problematic code, issue explanation, fix guidance, and OWASP category.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritizes high and critical findings, includes working fix examples, and calls out manual review areas when needed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
