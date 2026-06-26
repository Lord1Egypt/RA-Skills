## Description: <br>
Use trash-cli to safely delete files by moving them to the system trash instead of permanently removing them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xlionjuan](https://clawhub.ai/user/xlionjuan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and command-line users use this skill to manage recoverable file deletion, inspect trash contents, restore files, and remove selected trash entries with trash-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Permanent trash cleanup commands can irreversibly remove trashed files. <br>
Mitigation: Require explicit confirmation before running trash-empty or trash-rm. <br>
Risk: Restore and broad listing operations can overwrite files or expose trash entries beyond the current user's normal workflow. <br>
Mitigation: Confirm before using trash-restore --overwrite or trash-list --all-users, and review target paths before execution. <br>
Risk: Shell aliases and top-level trash directory setup can change user or system configuration. <br>
Mitigation: Review edits to shell startup files and sudo .Trash setup commands before applying them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xlionjuan/trash-cli) <br>
- [Official GitHub](https://github.com/andreafrancia/trash-cli) <br>
- [FreeDesktop.org Trash Specification](https://specifications.freedesktop.org/trash/latest/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires trash-cli command-line tools: trash-put, trash-list, trash-restore, trash-empty, and trash-rm.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
