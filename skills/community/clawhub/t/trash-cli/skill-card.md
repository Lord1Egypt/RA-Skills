## Description:

Use trash-cli to move files to the system trash for recoverable deletion instead of permanently removing them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xlionjuan](https://clawhub.ai/user/xlionjuan)

### License/Terms of Use:


## Use Case:

Developers, engineers, and command-line users use this skill to install and use trash-cli for recoverable file deletion, listing trashed items, restoring files, and managing trash contents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permanent removal commands such as trash-empty and trash-rm can irreversibly delete items from the trash.

Mitigation: Prefer trash-put and trash-restore for normal use, and confirm listed matches before running permanent removal commands.

Risk: The top-level /.Trash setup example uses sudo and changes a system-wide filesystem directory.

Mitigation: Run the sudo setup only when the user understands the filesystem impact and actually needs trash support on that partition.

Risk: Installing command-line tools from untrusted package sources can introduce supply-chain risk.

Mitigation: Install trash-cli only from package sources the user trusts, such as their operating system package manager, Homebrew, or a vetted Python package source.

## Reference(s):

- [Trash Cli on ClawHub](https://clawhub.ai/xlionjuan/skills/trash-cli)
- [Official trash-cli GitHub](https://github.com/andreafrancia/trash-cli)
- [FreeDesktop.org Trash Specification](https://specifications.freedesktop.org/trash/latest/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance for trash-cli operations; no API calls or credentials required.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
