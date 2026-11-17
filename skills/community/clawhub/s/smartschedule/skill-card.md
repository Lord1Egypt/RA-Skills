## Description:

SmartSchedule is a local team scheduling skill that manages shared SQLite schedules, detects conflicts, sends email summaries, and triggers DingTalk reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renhao12356578](https://clawhub.ai/user/renhao12356578)

### License/Terms of Use:

MIT-0

## Use Case:

Team members use this skill through an OpenClaw agent to add, update, search, delete, and receive reminders for a shared schedule. Administrators use it to configure SMTP email summaries and recurring DingTalk reminder jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared team calendar entries can be emailed and sent through DingTalk by recurring background jobs.

Mitigation: Restrict who can add, update, and delete schedules, and confirm reminder recipients before production use.

Risk: SMTP credentials are configured in the project config file.

Mitigation: Store SMTP credentials outside tracked project config, such as in a secrets store or environment-specific configuration.

Risk: Schedule title, location, and description fields are rendered into HTML email summaries.

Mitigation: Escape schedule fields before generating HTML email.

Risk: Recurring reminder agents may encounter schedule text during autonomous runs.

Mitigation: Treat schedule content as data only and prevent reminder jobs from following instructions embedded in event text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renhao12356578/skills/smartschedule)
- [README.md](artifact/README.md)
- [TECHNICAL.md](artifact/TECHNICAL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown/plain text guidance with inline shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local SQLite state and can configure recurring email and DingTalk reminder jobs.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
