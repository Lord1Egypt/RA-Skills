## Description: <br>
Pulse TODO provides unified task management and scheduling guidance for AI agents by keeping commitments, reminders, recurring checks, and task selection in one TODO.md workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kagura-agent](https://clawhub.ai/user/kagura-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Pulse TODO to maintain a persistent TODO.md, track commitments, create reminders, and choose the next task by strategic alignment. It is useful when an agent needs a single source of truth for pending work and cron-backed scheduled tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration can overwrite or lose existing TODO.md or HEARTBEAT.md content. <br>
Mitigation: Back up existing TODO.md and HEARTBEAT.md, then merge current tasks into the Pulse TODO format before relying on the new workflow. <br>
Risk: Incorrect cron changes can create missed, duplicated, or unexpected reminders. <br>
Mitigation: Review proposed cron changes and keep each repeat or timed TODO entry synchronized with its corresponding OpenClaw cron job. <br>
Risk: Ambiguous reminder requests can be stored with the wrong timing or recurrence. <br>
Mitigation: Confirm unclear date, time, timezone, and recurrence details before writing scheduled TODO entries or creating cron jobs. <br>


## Reference(s): <br>
- [Pulse TODO setup guide](setup.md) <br>
- [TODO template](TODO-TEMPLATE.md) <br>
- [Pulse TODO on ClawHub](https://clawhub.ai/kagura-agent/pulse-todo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TODO entries, setup commands, and configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update TODO.md, HEARTBEAT.md, and OpenClaw cron jobs when the agent acts on reminders or recurring tasks.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata; artifact package.json lists 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
