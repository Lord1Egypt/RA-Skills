## Description: <br>
Track your AI agent's token usage, API spend, and set soft budget thresholds with in-session warnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openauthority](https://clawhub.ai/user/openauthority) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to monitor estimated token usage, daily API spend, burn rate, recent budget history, and soft token thresholds during OpenClaw sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad questions about API costs or token usage. <br>
Mitigation: Review activation behavior in the target agent and use explicit commands when possible for budget-specific requests. <br>
Risk: Thresholds and history may be stored in the local OpenAuthority budget state file. <br>
Mitigation: Treat local budget history as usage data and manage file access according to the user's privacy and retention expectations. <br>
Risk: The skill provides soft warnings and cannot enforce a hard stop when a budget is exceeded. <br>
Mitigation: Use provider-side controls or the OpenAuthority plugin's budget rules for hard spending limits. <br>
Risk: Token usage and cost figures are estimated from session context and model pricing. <br>
Mitigation: Use the API provider billing dashboard as the source of truth for final costs. <br>


## Reference(s): <br>
- [Token Budget on ClawHub](https://clawhub.ai/openauthority/token-budget) <br>
- [OpenAuthority plugin](https://github.com/Firma-AI/openauthority) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown-style budget summaries, history tables, threshold confirmations, and warning messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Token counts and costs are estimates; threshold alerts are soft warnings rather than hard spending limits.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
