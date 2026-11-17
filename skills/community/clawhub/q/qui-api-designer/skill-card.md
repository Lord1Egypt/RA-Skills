## Description:

Use when designing REST or GraphQL APIs, creating OpenAPI specifications, or planning API architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design REST or GraphQL APIs, model resources, define endpoint contracts, and produce OpenAPI 3.1 specifications with supporting guidance for versioning, pagination, authentication, and error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API designs may include weak pagination cursor handling if implemented without additional safeguards.

Mitigation: Review pagination designs before implementation and require signed or otherwise integrity-protected cursors, strict validation, and authorization checks.

## Reference(s):

- [REST Design Patterns](references/rest-patterns.md)
- [API Versioning Strategies](references/versioning.md)
- [Pagination Patterns](references/pagination.md)
- [API Error Handling](references/error-handling.md)
- [OpenAPI 3.1 Specification](references/openapi.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with OpenAPI YAML or JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include resource models, endpoint specifications, authentication flows, error catalogs, pagination patterns, and versioning plans.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
