## Description: <br>
Autonomous goal completion with checkpoint, resume, and no intermediary confirmation handoffs for complex or long-running tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[as76](https://clawhub.ai/user/as76) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep an agent working through scoped, multi-step tasks until completion, with checkpoints and resume behavior. It is intended for tasks where the agent should ask only when genuinely blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad autonomous execution authority and discourages intermediary confirmations. <br>
Mitigation: Define written task scope, stop conditions, and hard blockers before activation; require confirmation for deletes, risky commands, production changes, external actions, and real-world side effects. <br>
Risk: The artifact includes Telegram messaging behavior with a hard-coded recipient in its examples. <br>
Mitigation: Remove or replace the recipient before use and require confirmation before sending external messages. <br>
Risk: Checkpoint and memory logs may retain task details after completion. <br>
Mitigation: Review and clean checkpoint or memory logs after the task completes, especially when the task handles sensitive data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/as76/tenacity) <br>
- [Standing Orders Template](references/standing-orders-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and checkpoint state examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create checkpoint JSON files under the configured checkpoint directory when its helper script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
