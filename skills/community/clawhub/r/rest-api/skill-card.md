## Description:

Build production-ready REST APIs with contract-first design, secure auth, robust testing, and deployment runbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design, implement, secure, test, and ship REST APIs from scratch or harden existing APIs for production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local REST API project memory may retain sensitive project context if users enter secrets, tokens, or personal data.

Mitigation: Decide whether to enable local memory before installation and avoid storing secrets, tokens, or personal data in ~/rest-api/.

Risk: Generated API guidance can miss application-specific security or reliability requirements.

Mitigation: Review auth, authorization, validation, rate limits, migration plans, tests, observability, and release gates before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/rest-api)
- [Skill Homepage](https://clawic.com/skills/rest-api)
- [API Contract Workflow](api-contract.md)
- [Endpoint Design Rules](endpoint-design.md)
- [Auth and Security Controls](auth-and-security.md)
- [Persistence and Migration Guide](persistence-and-migrations.md)
- [Testing and Observability](testing-and-observability.md)
- [Deployment Checklist - REST API](deployment-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code, command, checklist, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local project memory under ~/rest-api/ when the user opts in.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
