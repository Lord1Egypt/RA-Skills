## Description: <br>
Call the JustAI openapi async chat endpoints and return structured JSON results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanchaowen84](https://clawhub.ai/user/tanchaowen84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to call a deployed JustAI agent for marketing plans, Xiaohongshu notes, image generation, information collection, confirmation-card workflows, and follow-up chat turns. The skill lists available projects and skills, submits asynchronous chat requests, and polls structured JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, project references, and chat context are sent to a configured remote JustAI OpenAPI service. <br>
Mitigation: Use only a trusted JUSTAI_OPENAPI_BASE_URL, avoid regulated data or secrets in prompts, and review returned content before relying on it. <br>
Risk: The configured API key can reveal account metadata when listing projects or skills. <br>
Mitigation: Use a scoped, revocable API key where possible and rotate it if exposure is suspected. <br>
Risk: Asynchronous chat tasks may fail or time out. <br>
Mitigation: Surface failed-task messages directly, preserve conversation_id values for follow-up turns, and tune polling timeout for slower tasks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tanchaowen84/xiaojia-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUSTAI_OPENAPI_BASE_URL and JUSTAI_OPENAPI_API_KEY; supports optional timeout, project IDs, skill IDs, and conversation IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
