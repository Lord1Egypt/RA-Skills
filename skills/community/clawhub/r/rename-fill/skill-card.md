## Description:

Rename files in a specified directory with a given prefix, including a preview and confirmation step before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[git-xyz](https://clawhub.ai/user/git-xyz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other external users can use this skill to batch-prefix filenames in a selected directory while reviewing the planned changes before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A path-like prefix could move files outside the selected folder.

Mitigation: Allow only simple prefixes such as letters, numbers, underscores, or hyphens, and verify resolved destination paths stay inside the selected folder.

Risk: Batch renaming can be disruptive on important directories.

Mitigation: Review the preview carefully and use backups or disposable test folders before running on important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/git-xyz/skills/rename-fill)
- [Publisher profile](https://clawhub.ai/user/git-xyz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command snippets and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs preview mappings, rename counts, skipped files, and error summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
