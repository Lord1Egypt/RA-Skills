## Description:

Creates recurring OpenClaw analysis and report tasks by recording completed analysis steps from the current conversation, packaging them into a self-contained replay prompt, confirming the schedule, and adding an OpenClaw cron task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackyujun](https://clawhub.ai/user/jackyujun)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and operators use this skill after completing an analysis to convert the exact workflow into recurring daily inspections, weekly reports, monthly reports, or similar scheduled analysis tasks. It records executed analysis steps, confirms the recurring schedule and output with the user, and creates a scheduled replay task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled tasks may store analysis parameters or conclusions extracted from a conversation.

Mitigation: Use the skill only for analyses whose parameters and conclusions are safe to store, and require explicit confirmation of the exact stored prompt before scheduling.

Risk: Shell and temporary-file command patterns can be unsafe if task arguments are not handled safely.

Mitigation: Avoid executing the provided snippets unless OpenClaw supports safe argument-array or structured task creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackyujun/skills/scheduled-report)
- [Publisher profile](https://clawhub.ai/user/jackyujun)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with cron commands and a self-contained scheduled task prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent OpenClaw cron tasks after explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
