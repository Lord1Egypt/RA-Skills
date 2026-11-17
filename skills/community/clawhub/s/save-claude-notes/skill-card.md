## Description:

Save the latest/current Claude Code Q&A to a local Markdown note.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiao2769433](https://clawhub.ai/user/xiao2769433)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to manually save recent Q&A exchanges into Markdown notes, either in a daily note, a specified Markdown file, or a selected notes directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic transcript discovery can select the wrong Claude Code conversation or include private content.

Mitigation: Prefer explicit transcript or file-based input for sensitive work, and avoid the default --latest mode when multiple projects or private conversations may be present.

Risk: Selected Q&A content may contain sensitive context before it is saved to a Markdown note.

Mitigation: Redact sensitive content before saving, and only allow suspected secrets after explicit user confirmation.

Risk: A mistaken destination path can append notes to an unintended file or directory.

Mitigation: Verify the destination path before writing, especially when using one-off output files or notes directories.

## Reference(s):

- [Source repository](https://github.com/xiao2769433/save-claude-notes)
- [ClawHub skill page](https://clawhub.ai/xiao2769433/skills/save-claude-notes)
- [Publisher profile](https://clawhub.ai/user/xiao2769433)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration]

**Output Format:** [Markdown notes, shell commands, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manual note capture; selected Q&A content may be appended to daily or target Markdown files.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
