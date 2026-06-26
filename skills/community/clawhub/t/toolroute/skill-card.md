## Description: <br>
Route every task to the best MCP server and cheapest LLM. Scores on real execution data across quality, reliability, speed, cost, and trust. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grossiweb](https://clawhub.ai/user/grossiweb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use ToolRoute to ask an external routing service for recommended MCP servers, LLM models, and fallback chains before executing tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task descriptions are sent to an external routing service before use, which may expose sensitive task context if prompts are not generalized. <br>
Mitigation: Require explicit approval for sensitive work and redact names, credentials, contract details, personal data, and other confidential specifics before routing. <br>
Risk: Routing recommendations can influence tool and model selection for downstream agent work. <br>
Mitigation: Review recommendations before execution and verify that selected tools, models, and fallback chains match the task's data-handling and reliability requirements. <br>
Risk: Separate SDK or hook packages are mentioned but not included in the submitted artifact. <br>
Mitigation: Review and scan those packages independently before installing or enabling them. <br>


## Reference(s): <br>
- [ToolRoute ClawHub listing](https://clawhub.ai/grossiweb/toolroute) <br>
- [ToolRoute API docs](https://toolroute.io/api-docs) <br>
- [ToolRoute server catalog](https://toolroute.io/servers) <br>
- [ToolRoute models](https://toolroute.io/models) <br>
- [ToolRoute privacy policy](https://toolroute.io/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend MCP servers, LLM models, fallback chains, and optional reporting or registration steps.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
