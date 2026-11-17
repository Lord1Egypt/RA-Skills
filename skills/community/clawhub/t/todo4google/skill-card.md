## Description:

Manages local todo items and work logs, syncs selected tasks with Google Tasks, and archives todo files to Google Drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liliangjie91](https://clawhub.ai/user/liliangjie91)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain weekly markdown todo files, summarize daily work, sync day-specific tasks with Google Tasks through gog, and archive todo files to Google Drive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Todo content, notes, task titles, and file paths may be interpolated into shell commands.

Mitigation: Review commands before execution, use trusted todo content and paths, and prefer structured gog arguments over assembled shell strings.

Risk: Sync and archive operations send selected todo and work-log data to Google services.

Mitigation: Confirm the user intends to sync or archive the specific day's tasks or target file before invoking Google Tasks or Google Drive operations.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/liliangjie91/skills/todo4google)
- [Publisher profile](https://clawhub.ai/user/liliangjie91)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown task files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog command-line tool and access to Google Tasks or Google Drive for sync and archive operations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
