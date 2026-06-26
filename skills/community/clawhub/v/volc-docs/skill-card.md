## Description: <br>
Volc Docs searches and fetches official Volcengine documentation for product, API, SDK, pricing, deployment, troubleshooting, and service-support questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinsun-fiver](https://clawhub.ai/user/jinsun-fiver) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support teams use this skill to answer Volcengine product and implementation questions by searching official documentation or fetching the full content of a provided documentation link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Volcengine-related questions and documentation URLs may be sent to the external Volcengine docs API. <br>
Mitigation: Avoid including confidential information in queries or URLs, and use the skill only for Volcengine documentation lookups. <br>
Risk: Responses depend on external documentation API availability and returned content quality. <br>
Mitigation: Review the linked official documentation before relying on answers for operational or customer-facing decisions. <br>


## Reference(s): <br>
- [Volc Docs on ClawHub](https://clawhub.ai/jinsun-fiver/volc-docs) <br>
- [Volcengine documentation search API](https://docs-api.cn-beijing.volces.com/api/v1/doc/search) <br>
- [Volcengine documentation fetch API](https://docs-api.cn-beijing.volces.com/api/v1/doc/fetch) <br>
- [Volcengine documentation example](https://www.volcengine.com/docs/6349/162514) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown answers with official documentation links; script calls return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers should cite clean official Volcengine documentation URLs and show at most the most relevant results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
