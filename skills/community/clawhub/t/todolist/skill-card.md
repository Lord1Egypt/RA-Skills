## Description:

Manage macOS Reminders through AppleScript-backed commands for adding, listing, completing, deleting, searching, and organizing reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manifoldor](https://clawhub.ai/user/manifoldor)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage macOS Reminders from an agent workflow on macOS, including creating, listing, completing, deleting, searching, and organizing reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fuzzy no-confirmation complete, uncomplete, and delete actions can affect the wrong reminder.

Mitigation: Use specific reminder titles, avoid vague fragments, and confirm important reminders in the Reminders app before destructive changes.

Risk: Reminder changes may sync to other Apple devices.

Mitigation: Treat completion and deletion as user-visible synced changes and manually verify high-value reminders after running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manifoldor/skills/todolist)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS with Reminders app permission; recurring reminders may need manual configuration in Reminders.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
