## Description:

Query and answer questions about Volcengine API specifications, including parameters, error codes, request methods, enum values, required fields, response structures, pagination, parameter dependencies, service capability lists, API availability, and API comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to look up Volcengine API specifications and answer implementation questions about API actions, parameters, responses, errors, pagination, and service capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User questions may include sensitive API names, error codes, or internal incident details that could be sent to Volcengine during lookup.

Mitigation: Avoid including secrets or sensitive internal details in lookup queries unless sharing that text with Volcengine is acceptable.

## Reference(s):

- [Volcengine API Explorer Services](https://api.volcengine.com/api/common/explorer/services)
- [Volcengine API Explorer Versions](https://api.volcengine.com/api/common/explorer/versions?ServiceCode={ServiceCode})
- [Volcengine API Explorer APIs](https://api.volcengine.com/api/common/explorer/apis?ServiceCode={ServiceCode}&Version={Version}&APIVersion={Version})
- [Volcengine API Explorer Swagger](https://api.volcengine.com/api/common/explorer/api-swagger?ServiceCode={ServiceCode}&Version={Version}&APIVersion={Version}&ActionName={ActionName})
- [Volcengine API Search](https://api.volcengine.com/api/common/search/all?Query={keyword}&Channel=api)
- [Volcengine Error Code Search](https://api.volcengine.com/api/common/search/all?Query={error_code}&Channel=error_code)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Code]

**Output Format:** [Markdown answers with structured lists and inline code blocks when examples are useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, response structures, enum values, dependency notes, pagination guidance, and troubleshooting steps.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
