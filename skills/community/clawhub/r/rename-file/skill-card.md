## Description:

Rename files in a specified directory with a given prefix. This skill prompts the user for a prefix and directory path, shows a preview of changes, and asks for confirmation before executing. Uses Node.js script for cross-platform compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[git-xyz](https://clawhub.ai/user/git-xyz)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to batch add a consistent prefix to files in a chosen directory after reviewing the proposed rename operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prefix handling can move files outside the chosen folder.

Mitigation: Use only backed-up folders, avoid untrusted prefixes, and reject prefixes containing slashes, backslashes, or traversal strings such as ../ before execution.

Risk: The skill performs batch file renames with under-enforced safeguards.

Mitigation: Review the preview carefully before confirming and prefer a dry-run or destination validation workflow before using it on important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/git-xyz/skills/rename-file)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and plain-text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and may rename files in the selected directory after user confirmation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
