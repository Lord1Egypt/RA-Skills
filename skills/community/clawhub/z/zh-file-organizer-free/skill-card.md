## Description:

A Chinese-language file organizer skill that helps agents classify and organize files by type for personal, team, and cross-platform automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent operators, and teams use this skill to have an agent organize local files, classify common file types, inspect file metadata, and report operation status. It is intended for file-management automation rather than complex judgment calls or encrypted-file bypass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and command authority over user-selected folders, which can affect local files if used on the wrong path.

Mitigation: Use the skill on a test folder first, limit the target directory, and ask the agent to preview planned moves or deletions before applying changes.

Risk: Duplicate cleanup and file organization can remove, overwrite, or relocate files in ways that are difficult to undo.

Mitigation: Keep backups of important folders, require explicit confirmation before destructive operations, and review the operation summary after each run.

Risk: Sensitive directories or API keys may be exposed if the agent is pointed at private data or asked to configure credentials unnecessarily.

Mitigation: Avoid sensitive directories unless required, do not provide API keys unless the workflow clearly needs them, and prefer environment-variable handling for any credential configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/zh-file-organizer-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON-style operation summaries with inline shell commands when configuration is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include success status, result data, error details, file paths, file metadata, and follow-up troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
