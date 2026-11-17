## Description:

Helps Chinese-speaking teams manage a local task ledger, generate workday-aware reminders, and optionally mirror tasks to macOS Reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djoldwang](https://clawhub.ai/user/djoldwang)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking teams and their integration operators use this skill to track shared tasks, review progress and deadlines, and prepare reminders. Optional macOS Reminders mirroring requires explicit setup; identity checks, team notifications, and reminder delivery require a trusted external integration.

### Deployment Geography for Use:

Global (Chinese-language interface; built-in workday calendars cover mainland China)

## Known Risks and Mitigations:

Risk: Optional Reminders mirroring and scheduled sync can change a dedicated local list and create user-level background scheduling.

Mitigation: Use explicit initialization and enablement only for a user-selected dedicated list; review the planned changes first and disable scheduling when no longer needed.

Risk: Local task records and synchronization state may contain sensitive team information.

Mitigation: Keep task and state directories private to the user and restrict access to trusted integrations.

Risk: The skill does not itself authenticate users or authorize team notifications and calendar web access.

Mitigation: Use a trusted integration layer to enforce identity, permissions, notification authorization, and government-calendar web access.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/djoldwang/skills/team-tasks)
- [Storage and integration guidance](references/storage.md)
- [macOS Reminders setup](references/macos-reminders.md)
- [Annual calendar maintenance](references/calendar-maintenance.md)
- [Reminder adapter contract](references/reminder-adapters.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Guidance]

**Output Format:** [Chinese-language responses and reminders; task data and exports in JSON, CSV, or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local task data and optional macOS Reminders synchronization]

## Skill Version(s):

1.6.6 (source: SKILL.md metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
