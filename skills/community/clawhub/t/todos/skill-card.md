## Description:

Todos is a local to-do management skill for adding, completing, viewing, and deleting tasks stored in a local JSON file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[radiantbk](https://clawhub.ai/user/radiantbk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to manage personal to-do items through concise natural-language commands and a bundled Python command-line helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and modifies a local todo data file under ~/.openclaw/workspace/memory/todos.json.

Mitigation: Confirm this local storage location is acceptable before installation and review the file if todo data needs to be audited or removed.

Risk: Completion and deletion commands change task state in the local todo file.

Mitigation: Use explicit task IDs for completion and deletion, and inspect the list output before making irreversible todo edits.

Risk: The user-facing skill documentation and script output are written primarily in Chinese.

Mitigation: Deploy it for users who can operate the Chinese interface or provide localized wrapper guidance before use.

## Reference(s):

- [ClawHub Todos Skill Page](https://clawhub.ai/radiantbk/skills/todos)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Text responses and command-line invocations; task data is persisted as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and modifies ~/.openclaw/workspace/memory/todos.json when used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
