## Description: <br>
Integrates n8n workflows with OpenClaw agents through authenticated webhooks, agent execution, result callbacks, and observability hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation teams use this skill to let n8n workflows trigger OpenClaw agent actions, receive execution results, and continue downstream workflow steps. It is suited to webhook-driven automation such as scheduled AI search, CRM enrichment, and social media monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook requests can trigger broad agent actions and callbacks. <br>
Mitigation: Run the service only on localhost or a protected network, require a strong unique N8N_AUTH_TOKEN, and restrict allowed workflows and actions. <br>
Risk: Example or default tokens could allow unintended access if reused. <br>
Mitigation: Replace the example workflow token before use and rotate authentication tokens regularly. <br>
Risk: Sensitive workflow parameters may be exposed through logs, traces, or callback payloads. <br>
Mitigation: Disable or sanitize telemetry for sensitive parameters and allow callbacks only to trusted n8n URLs. <br>
Risk: The n8n API key can grant broader workflow and credential API access. <br>
Mitigation: Avoid setting N8N_API_KEY unless those API methods are required, and scope operational access as tightly as the deployment allows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/yuyonghao-n8n-integration) <br>
- [n8n documentation](https://docs.n8n.io/) <br>
- [Research notes](artifact/RESEARCH.md) <br>
- [Example workflow](artifact/examples/workflow-example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON workflow configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces webhook setup guidance, n8n workflow examples, and Node.js integration patterns for agent execution and callbacks.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
