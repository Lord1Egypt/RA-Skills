## Description: <br>
Cross-platform rar and winrar command-line archive handling for Windows and Linux, including executable detection, PATH repair, official download fallback, password-protected archives, multipart archives, and troubleshooting command-line extraction or compression failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zkcloud](https://clawhub.ai/user/zkcloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and shell-oriented users use this skill to prepare reliable rar or winrar commands for extracting, creating, and troubleshooting archives across Windows and Linux environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can suggest persistent PATH changes. <br>
Mitigation: Prefer absolute executable paths or temporary PATH changes, and require explicit user approval before persistent PATH edits. <br>
Risk: The skill can suggest downloading external installer binaries. <br>
Mitigation: Use only the official download URLs from the skill evidence and verify installers before use. <br>
Risk: Archive passwords can be exposed in displayed commands. <br>
Mitigation: Redact passwords from logs and displayed commands whenever possible, while preserving enough detail for the user to execute safely. <br>
Risk: Overwrite flags can replace existing files during extraction. <br>
Mitigation: Extract into a new folder before using overwrite flags and confirm overwrite intent with the user. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zkcloud/rar-archive-helper) <br>
- [RAR / WinRAR Quick Reference](references/winrar-quick-reference.md) <br>
- [Common Errors Quick Reference](references/common-errors.md) <br>
- [Execution Template](references/execution-template.md) <br>
- [WinRAR Windows Download](https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-720.exe) <br>
- [RAR Linux Download](https://www.win-rar.com/fileadmin/winrar-versions/rarlinux-x64-720.tar.gz) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Goal, Detect, Fix PATH, Run, Verify, Result response structure and permits one evidence-based retry when the failure cause is clear.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
