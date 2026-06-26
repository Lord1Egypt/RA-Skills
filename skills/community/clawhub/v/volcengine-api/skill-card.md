## Description: <br>
Query and answer questions about Volcengine API specifications, including parameters, error codes, request methods, enum values, required fields, response structures, pagination, service capabilities, API availability, and API comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to answer Volcengine API questions from API Explorer data, including how to find APIs, inspect request and response schemas, understand error codes, compare operations, and identify pagination or parameter constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup keywords, API names, and error codes may be sent to Volcengine documentation endpoints. <br>
Mitigation: Avoid including private business context or sensitive identifiers in lookup terms unless sharing them with Volcengine documentation services is acceptable. <br>
Risk: API Explorer data can be incomplete, unavailable, or temporarily unreachable during a user request. <br>
Mitigation: Tell the user when lookup fails or results are ambiguous, ask for API or service context when needed, and avoid relying on memory for current Volcengine API details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volc-sdk-team/skills/volcengine-api) <br>
- [Volcengine API Explorer services endpoint](https://api.volcengine.com/api/common/explorer/services) <br>
- [Volcengine API Explorer API details endpoint](https://api.volcengine.com/api/common/explorer/api-swagger?ServiceCode={ServiceCode}&Version={Version}&APIVersion={Version}&ActionName={ActionName}) <br>
- [Volcengine API Explorer search endpoint](https://api.volcengine.com/api/common/search/all?Query={keyword}&Channel=api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown or plain text answers with API details, constraints, and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers may be in Chinese or English and may include API parameters, error-code explanations, request and response structures, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
