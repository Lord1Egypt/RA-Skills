## Description: <br>
Manage Vapi voice assistants, calls, phone numbers, tools, and webhooks via Vapi REST API or CLI commands within OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colygon](https://clawhub.ai/user/colygon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Vapi voice agent resources, including assistants, calls, phone numbers, tools, and webhooks, through documented REST and CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through sensitive Vapi account-management actions, including changing assistants, phone numbers, tools, webhooks, and calls. <br>
Mitigation: Keep VAPI_API_KEY in a secret manager, prefer read-only checks first, and approve account-changing actions or outbound calls case by case. <br>
Risk: Incorrect phone numbers, webhook URLs, or call settings can cause calls or events to go to unintended destinations. <br>
Mitigation: Verify phone numbers, assistant IDs, webhook URLs, consent, and recording requirements before initiating or changing call workflows. <br>
Risk: The optional Vapi CLI installation path uses a remote installer. <br>
Mitigation: Inspect or replace the remote installer with an official installation method before running it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/colygon/vapi-skill) <br>
- [Vapi API Reference](https://api.vapi.ai/api) <br>
- [Vapi Quickstart](https://docs.vapi.ai/quickstart/introduction) <br>
- [Vapi CLI](https://github.com/VapiAI/cli) <br>
- [Vapi MCP Setup](https://docs.vapi.ai/cli/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include REST request shapes and CLI workflow steps; requires VAPI_API_KEY for account access.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
