## Description: <br>
Inspect, query, summarize, and debug WeryAI task IDs and batch IDs through the official task query endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weryai-developer](https://clawhub.ai/user/weryai-developer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect existing WeryAI task or batch IDs, summarize current status, surface generated artifact URLs, and debug task lifecycle issues without submitting new work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WeryAI API key to query task and batch status. <br>
Mitigation: Keep WERYAI_API_KEY private and configure it only in trusted runtime environments. <br>
Risk: Overriding the default WeryAI base URL could send task identifiers or authorization headers to an unintended endpoint. <br>
Mitigation: Use only a trusted WERYAI_BASE_URL when overriding the default API host. <br>
Risk: Raw task payloads and artifact URLs can expose generated content or other sensitive task details to the agent context. <br>
Mitigation: Inspect only task or batch IDs whose raw outputs and artifact URLs are appropriate to reveal in the current session. <br>


## Reference(s): <br>
- [WeryAI Task Query APIs](references/tasks-api.md) <br>
- [Query Task Details](https://docs.weryai.com/api-reference/tasks/query-task-details) <br>
- [Query Batch Task Status](https://docs.weryai.com/api-reference/tasks/query-batch-task-status) <br>
- [ClawHub Skill Listing](https://clawhub.ai/weryai-developer/weryai-task-inspector) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the inspector script, typically summarized by the agent as text or Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only task and batch inspection; includes normalized phase, status fields, artifacts, and raw API payload when available.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
