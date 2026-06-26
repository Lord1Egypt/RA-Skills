## Description: <br>
Helps agents discover RunAPI models, compare capabilities and pricing, inspect required fields, search by modality, and recommend a service/action/model triple. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query RunAPI catalog and pricing tools, compare available models, and choose a suitable service/action/model triple for generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model and pricing answers depend on configured RunAPI MCP tools and may change over time. <br>
Mitigation: Use current RunAPI tool responses for catalog and pricing details, and do not quote stale prices. <br>
Risk: Recommendations could be incomplete if the user supplies broad or ambiguous requirements. <br>
Mitigation: Filter by modality, service, or action when possible and present one service/action/model triple only when the user wants a generation recommendation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text, typically compact tables and concise recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference RunAPI model slugs, service/action/model triples, pricing summaries, and required parameter notes returned by configured RunAPI MCP tools.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
