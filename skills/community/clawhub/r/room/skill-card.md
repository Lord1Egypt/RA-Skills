## Description:

Organize room inventory and maintenance schedules. Use when adding furniture items, tracking appliances, scheduling deep cleans, setting repair reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Room to record room inventory, maintenance schedules, reminders, costs, and notes from a local CLI, then review, search, or export that data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Room and household notes are stored locally under ~/.local/share/room until the user removes them.

Mitigation: Avoid entering sensitive household details unless local storage is acceptable, and delete or back up ~/.local/share/room according to the user's retention needs.

Risk: CSV exports may preserve formula-like user-entered values that spreadsheet software could evaluate.

Mitigation: Review or sanitize exported CSV values before opening them in spreadsheet software, especially when entries may contain untrusted text.

## Reference(s):

- [Room ClawHub Listing](https://clawhub.ai/bytesagain-lab/skills/room)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text terminal output with optional JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local data under ~/.local/share/room and can export room records for backup or review.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
