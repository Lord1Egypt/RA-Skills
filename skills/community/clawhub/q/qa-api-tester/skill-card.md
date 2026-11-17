## Description:

API interface testing and automation for sending HTTP requests, validating responses, chaining API calls, and generating Python requests/pytest, curl, and Postman collection outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanghengyi1986-afk](https://clawhub.ai/user/zhanghengyi1986-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and API testers use this skill to test REST or GraphQL endpoints, validate status codes, headers, response bodies, schemas, and generate reusable API automation assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated write or delete requests could modify or remove data.

Mitigation: Use scoped test tokens, approved non-production endpoints, disposable data, and explicit confirmation before POST, PUT, PATCH, or DELETE requests.

Risk: Concurrent request checks could create unwanted traffic against target services.

Mitigation: Run concurrency checks only against approved test endpoints with conservative limits and explicit confirmation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhanghengyi1986-afk/skills/qa-api-tester)
- [Publisher Profile](https://clawhub.ai/user/zhanghengyi1986-afk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline bash, Python, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce curl commands, pytest/requests scripts, JSON schema validation examples, Postman collection JSON, and environment configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
