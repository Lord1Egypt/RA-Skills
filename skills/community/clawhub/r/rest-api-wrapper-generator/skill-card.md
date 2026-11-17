## Description:

Generate production-ready REST API endpoints to expose graph database operations, queries, and data management capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate and review REST API wrappers for graph databases, including CRUD, relationship, query, traversal, authentication, pagination, and documentation patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents itself as production-ready, while security evidence says it should be treated as a scaffold/reference for powerful query and data-mutation APIs.

Mitigation: Review generated APIs before deployment and require real authentication, authorization, rate limiting, audit logging, and least-privilege database credentials.

Risk: Generated custom query endpoints and examples can expose graph queries or destructive data mutations if accepted without controls.

Mitigation: Use parameterized or allowlisted graph queries, validate all inputs, restrict destructive operations, and require role checks for sensitive endpoints.

Risk: Webhook and external callback patterns can introduce unsafe outbound requests.

Mitigation: Validate webhook URLs, restrict allowed destinations where appropriate, and log callback activity for review.

Risk: Install guidance includes unpinned framework dependencies.

Mitigation: Pin and scan dependencies before using generated services in a deployment pipeline.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/rest-api-wrapper-generator)
- [REST API Design Patterns](references/rest-api-patterns.md)
- [REST API Wrapper Examples](examples/rest-api-examples.md)
- [REST API Best Practices](https://restfulapi.net/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Express.js Guide](https://expressjs.com/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [RESTful API Design](https://swagger.io/resources/articles/best-practices-in-api-design/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code snippets, HTTP examples, JSON schemas, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce API endpoint scaffolds, OpenAPI-style documentation structures, request and response examples, and deployment-oriented configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
