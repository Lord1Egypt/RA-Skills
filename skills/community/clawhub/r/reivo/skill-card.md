## Description: <br>
Track AI agent costs in real-time, set budget limits, and auto-detect runaway loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tazsat0512](https://clawhub.ai/user/tazsat0512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Reivo to monitor AI API spend, enforce budgets, detect runaway loops, and configure cost-saving model routing for OpenAI, Anthropic, and Google traffic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes AI API traffic through the Reivo proxy and uses Reivo account credentials. <br>
Mitigation: Install only when that traffic routing is acceptable; use dedicated or scoped provider keys where possible and keep REIVO_API_KEY private. <br>
Risk: The skill can change Reivo account settings such as budget limits, routing mode, and Slack webhook notifications when requested. <br>
Mitigation: Review budget, routing-mode, and Slack webhook changes before applying them. <br>
Risk: Cost and defense reports depend on the Reivo service and the configured account state. <br>
Mitigation: Treat reports as account-specific operational data and verify important decisions in the Reivo dashboard. <br>


## Reference(s): <br>
- [Reivo homepage](https://reivo.dev) <br>
- [Reivo dashboard](https://app.reivo.dev) <br>
- [ClawHub skill page](https://clawhub.ai/tazsat0512/reivo) <br>
- [Publisher profile](https://clawhub.ai/user/tazsat0512) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live account cost, budget, routing, defense, optimization, and Slack notification status returned from Reivo APIs.] <br>

## Skill Version(s): <br>
0.4.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
