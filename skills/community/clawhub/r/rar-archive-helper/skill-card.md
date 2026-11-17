## Description:

Provides cross-platform RAR and WinRAR command-line guidance for detecting archive tools, repairing PATH issues, extracting or creating archives, handling passwords and multipart archives, and troubleshooting common failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkcloud](https://clawhub.ai/user/zkcloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation users, and shell-oriented agents use this skill to prepare reliable RAR or WinRAR commands for extracting, creating, and troubleshooting archives on Windows and Linux.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Archive passwords can be exposed if placed directly in command arguments or logs.

Mitigation: Prefer interactive password prompts or approved secret handling, and avoid recording real passwords in command history or shared output.

Risk: Persistent PATH changes can affect future shells or user environments.

Mitigation: Use a temporary PATH update or an absolute executable path unless the user explicitly approves a persistent PATH change and understands how to undo it.

Risk: Installer downloads can create supply-chain risk when the archive tool is missing.

Mitigation: Download only after detection and common-location checks fail, use the official WinRAR links, and verify the installer through trusted channels before running it.

Risk: Overwrite flags and archive commands can change or replace files.

Mitigation: Review the final command, target paths, and overwrite options before execution, then verify expected outputs after the command completes.

## Reference(s):

- [RAR / WinRAR Quick Reference](references/winrar-quick-reference.md)
- [Execution Template](references/execution-template.md)
- [Common Errors Quick Reference](references/common-errors.md)
- [WinRAR Windows Download](https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-720.exe)
- [RAR Linux Download](https://www.win-rar.com/fileadmin/winrar-versions/rarlinux-x64-720.tar.gz)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Goal, Detect, Fix PATH, Run, Verify, and Result reporting structure.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
