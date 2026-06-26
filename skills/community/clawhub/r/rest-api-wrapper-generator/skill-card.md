## Description: <br>
Generate production-ready REST API endpoints to expose graph database operations, queries, and data management capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate REST API wrappers for graph databases, including CRUD endpoints, relationship endpoints, query endpoints, authentication patterns, validation, error handling, and API documentation scaffolding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated database APIs may expose sensitive graph data or mutation endpoints without adequate access control. <br>
Mitigation: Require authentication and authorization before deployment, apply role-based permissions, and add deletion safeguards for destructive operations. <br>
Risk: Arbitrary query endpoints can permit unsafe or overly broad database access. <br>
Mitigation: Avoid arbitrary query endpoints where possible, parameterize database queries, validate request schemas, and restrict allowed query patterns. <br>
Risk: Example server and webhook patterns can become unsafe if copied directly into production. <br>
Mitigation: Bind local development servers to localhost, restrict webhook targets, require HTTPS, and review generated scaffolding as a starting point rather than a deployable system. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fisa712/rest-api-wrapper-generator) <br>
- [REST API Design Patterns](references/rest-api-patterns.md) <br>
- [REST API Wrapper Examples](examples/rest-api-examples.md) <br>
- [REST API Best Practices](https://restfulapi.net/) <br>
- [FastAPI Documentation](https://fastapi.tiangolo.com/) <br>
- [Express.js Guide](https://expressjs.com/) <br>
- [MDN HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) <br>
- [Swagger RESTful API Design](https://swagger.io/resources/articles/best-practices-in-api-design/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code blocks, API endpoint examples, JSON configuration, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are scaffolding for graph database REST APIs and should be reviewed before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
