## Description:

Manages user schedules and task planning by adding, listing, updating, deleting, and setting reminders for local schedule entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h3avysword](https://clawhub.ai/user/h3avysword)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal productivity agents use this skill to maintain a local task schedule, view time-bounded task lists, update priorities and deadlines, delete completed tasks, and optionally set reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bash command templates can turn untrusted task names or notes into local command execution.

Mitigation: Review task names, notes, and generated commands before execution; prefer structured argument passing for deployments that accept untrusted input.

Risk: Reminder setup can pass stored task text into a future agent action through another skill.

Mitigation: Review reminder message content and the permissions of cron-mastery before enabling reminders.

## Reference(s):

- [Schedule Manager ClawHub listing](https://clawhub.ai/h3avysword/skills/schedules-manager)
- [Reply templates](artifact/references/templates.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text responses and Bash command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates a local schedules/schedule.csv file; reminder setup may hand task text to a separate reminder skill.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
