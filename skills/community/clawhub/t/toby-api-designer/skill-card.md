## Description:

Use when designing REST or GraphQL APIs, creating OpenAPI specifications, or planning API architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API architects use this skill to design REST or GraphQL APIs, model resources, plan versioning and pagination, define error handling, and produce OpenAPI specifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API specifications may include unsafe or unintended resource-modifying operations when requirements are incomplete.

Mitigation: Review generated specifications before implementation, especially endpoints that delete or modify resources, and confirm authorization behavior.

Risk: API design guidance may omit organization-specific security, privacy, compliance, or rate-limiting requirements.

Mitigation: Run security and privacy review before production use and verify authentication, authorization, data exposure, and operational limits.

## Reference(s):

- [REST Design Patterns](references/rest-patterns.md)
- [API Versioning Strategies](references/versioning.md)
- [Pagination Patterns](references/pagination.md)
- [API Error Handling](references/error-handling.md)
- [OpenAPI 3.1 Specification](references/openapi.md)
- [Complete setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with OpenAPI YAML or JSON examples and structured API design guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include resource models, endpoint specifications, authentication and authorization flows, error catalogs, pagination patterns, and versioning strategies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
