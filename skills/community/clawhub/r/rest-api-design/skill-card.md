## Description:

Provides REST API design guidance for resource naming, HTTP methods, status codes, pagination, filtering, authentication, rate limiting, versioning, and response formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design new REST endpoints, review API contracts, add pagination, filtering, authentication, and authorization patterns, and plan API versioning for public or partner-facing APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated destructive endpoint designs, such as DELETE operations, may omit project-specific authorization, audit, or safety requirements.

Mitigation: Review destructive endpoint proposals against your authorization model, audit requirements, and operational safety controls before implementation.

## Reference(s):

- [API Resource Design Patterns](references/resource-design.md)
- [Pagination, Filtering, and Authentication](references/pagination-filtering-auth.md)
- [REST API Design ClawHub Page](https://clawhub.ai/djc00p/skills/rest-api-design)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with API examples, code snippets, endpoint patterns, tables, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only guidance; no executable behavior or required local tools.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
