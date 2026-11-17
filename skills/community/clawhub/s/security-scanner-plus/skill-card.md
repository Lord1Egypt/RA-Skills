## Description:

Scans AI agent skills for security vulnerabilities, dangerous code patterns, and undeclared permissions using dependency, static code, and permission checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kennyzir](https://clawhub.ai/user/kennyzir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and marketplace operators use this skill to check agent skills before installation, publication, CI release, or ongoing monitoring. It returns a structured report covering dependency vulnerabilities, risky code patterns, undeclared permissions, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the selected repository URL, skill slug, or direct source-code payload to Claw0x for analysis.

Mitigation: Avoid direct-code mode for proprietary code or secrets unless external scanning is permitted by the organization.

Risk: The skill requires a CLAW0X_API_KEY environment variable.

Mitigation: Store the API key in environment or secret-management tooling, never embed it in prompts or source files, and rotate it if exposed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/kennyzir/skills/security-scanner-plus)
- [Publisher profile](https://clawhub.ai/user/kennyzir)
- [Claw0x](https://claw0x.com)
- [OSV vulnerability database](https://osv.dev)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Structured JSON security report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes risk level, risk score, dependency findings, static code findings, permission audit results, recommendations, scan timestamp, and scan duration.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
