## Description:

Travel Tracker helps manage work and personal travel records, generate Excel reports, sync records to Obsidian, import travel plans from Apple Calendar, and set travel reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m646pxhjf4-dot](https://clawhub.ai/user/m646pxhjf4-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and personal users use this skill to query and summarize work/life travel records, generate weekly, monthly, and quarterly reports, sync travel notes to Obsidian, and manage travel reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates calendar, travel-record, report, reminder, and Obsidian actions to local scripts outside the package.

Mitigation: Review the referenced scripts under ~/.openclaw/workspace/scripts/ before installation or use, and confirm their handling of Apple Calendar data, travel history, reports, memory files, Obsidian copies, and reminders.

Risk: The skill may process and persist sensitive calendar and travel-history information.

Mitigation: Use it only when persistent copies in generated reports, memory files, Obsidian notes, and reminders are acceptable for the user or organization.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for local scripts that query records, generate Excel reports, sync Obsidian notes, import Apple Calendar travel plans, and set reminders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
