## Description:

Manage calendar, draft communications, and track preferences with explicit confirmation before actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Individuals and teams use this skill as an administrative assistant for calendar planning, communication drafting, reminders, travel coordination, and preference tracking. It is intended to operate through the user's configured tools with explicit confirmation before external actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Support files describe sending messages, changing calendars, and booking travel without clear user approval.

Mitigation: Require explicit confirmation for every send, archive, RSVP, calendar edit, booking, and rebooking before granting tool access.

Risk: The skill may store or update personal preferences and relationship context in local memory files.

Mitigation: Require user approval for each memory write and review the contents of ~/secretary/ periodically.

Risk: Broad email, calendar, travel, or document permissions could let the skill take high-impact actions.

Mitigation: Use host-level approval controls and grant only the narrow permissions needed for the current task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/secretary)
- [Calendar Management](artifact/calendar.md)
- [Memory System Guide](artifact/memory-guide.md)
- [Daily Operations](artifact/operations.md)
- [Writing On Your Behalf](artifact/writing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with occasional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local files under ~/secretary/ when the user allows memory storage.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
