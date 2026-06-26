## Description: <br>
SmartSaaS lets an agent manage SmartSaaS datasets, projects, tasks, team members, integrations, knowledge, campaigns, templates, events, and cron workflows through authenticated shell scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smartsaas](https://clawhub.ai/user/smartsaas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SmartSaaS users and operators use this skill to automate administrative workflows in SmartSaaS, including dataset management, project and task operations, integrations, knowledge and research content, campaigns, templates, webhooks, and scheduled events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad SmartSaaS administrative powers beyond dataset-only workflows. <br>
Mitigation: Install it only when that broad access is intended, and use a least-privilege API key scoped to the actions the agent should perform. <br>
Risk: Write, integration, campaign, team, webhook, and cron actions can change SmartSaaS state. <br>
Mitigation: Require explicit user confirmation before executing these actions, especially in production environments. <br>
Risk: The skill relies on SmartSaaS API credentials from the execution environment. <br>
Mitigation: Keep SMARTSAAS_BASE_URL and SMARTSAAS_API_KEY in configuration or environment variables, and do not paste or log the API key in chat. <br>
Risk: Incorrect request shapes can create bad records or fail against SmartSaaS schemas. <br>
Mitigation: Run the schema lookup flow before create or post operations, then build request bodies that match the returned schema. <br>


## Reference(s): <br>
- [SmartSaaS ClawHub release page](https://clawhub.ai/smartsaas/smartsaas-ai) <br>
- [SMARTSAAS.md](artifact/SMARTSAAS.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell command invocations, and JSON responses from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SMARTSAAS_BASE_URL and SMARTSAAS_API_KEY in the environment; write actions should be explicitly requested by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
