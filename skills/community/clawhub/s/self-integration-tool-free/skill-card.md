## Description: <br>
自集成工具 helps agents connect to external applications such as Slack, HubSpot, and Notion through a unified integration gateway, then create OAuth connections, search available actions, and execute single actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect supported SaaS applications, establish OAuth connections, search actions, and execute simple cross-app operations such as sending Slack messages or creating CRM records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger live create, update, delete, send, or webhook-driven actions in connected external services. <br>
Mitigation: Use a limited gateway token, test with non-production accounts first, and require explicit approval before any action that changes data or sends messages. <br>
Risk: An integration token could expose connected application access if it is logged, shared, or hardcoded. <br>
Mitigation: Store INTEGRATION_TOKEN only in the environment or a secrets manager, avoid embedding credentials in prompts or files, and rotate the token immediately if exposed. <br>
Risk: Incorrect connection IDs, action IDs, or inputs could run an action against the wrong service or with invalid data. <br>
Mitigation: List existing connections first, verify the selected connection and action schema, and review input fields before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/self-integration-tool-free) <br>
- [Integration gateway API base](https://api.integration-gateway.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown instructions with curl command examples and API request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an integration gateway token and external service accounts; the free edition is limited to prebuilt connectors and single-action execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
