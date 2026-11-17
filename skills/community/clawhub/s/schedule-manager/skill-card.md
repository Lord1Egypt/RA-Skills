## Description:

Schedule Manager helps agents view, add, edit, pause, delete, and run local scheduled tasks and one-time reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cowboy231](https://clawhub.ai/user/cowboy231)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage recurring cron-backed reminders and temporary reminders in an OpenClaw workspace. It supports task listing, creation, editing, pausing, deletion, cleanup, and local text-to-speech reminder execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill rewrites the user's crontab when recurring tasks are changed.

Mitigation: Back up the current crontab before installation or use, and review generated cron entries before relying on them.

Risk: Persistent cron commands are built from weakly validated task fields.

Mitigation: Only add task names, weekdays, and times from trusted sources until field validation and safe quoting are confirmed.

Risk: Running the skill from a privileged account could expand the impact of cron or file-write mistakes.

Mitigation: Run it under a non-privileged user account with access limited to the intended OpenClaw workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cowboy231/skills/schedule-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Command-line text and Markdown-backed task configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, python3, and edge-tts; updates local workspace task files and the user's crontab.]

## Skill Version(s):

1.0.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
