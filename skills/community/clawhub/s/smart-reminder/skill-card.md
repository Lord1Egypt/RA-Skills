## Description:

Smart Reminder helps an agent create scheduled reminders with five reminder personalities, nickname personalization, multi-frequency progress tracking, and context-aware feedback using cron scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seulkilu](https://clawhub.ai/user/seulkilu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to set one-time or repeating reminders, deliver them in a selected personality style, and track progress on recurring tasks. It is suited for personal reminder workflows where local reminder history and delivery routing data are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local reminder history and delivery identifiers.

Mitigation: Avoid sensitive reminder text and install only where keeping local history and routing identifiers is acceptable.

Risk: Scheduled jobs may lack sufficient cleanup, consent, or scoping safeguards.

Mitigation: Confirm the target account before cross-channel reminders and periodically review or remove cron jobs.

## Reference(s):

- [Personalities Reference](references/personalities.md)
- [Smart Reminder ClawHub Page](https://clawhub.ai/seulkilu/skills/smart-reminder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reminder text, task-state configuration, cron scheduling guidance, and progress feedback.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
