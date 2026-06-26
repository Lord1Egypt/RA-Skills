## Description: <br>
Automated workspace health checks and entropy prevention for OpenClaw. Detects broken symlinks, empty dirs, large files, malformed names. Maintenance audit script with cron support. Keeps deployments clean and structured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donovanpankratz-del](https://clawhub.ai/user/donovanpankratz-del) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and workspace operators use this skill to initialize an OpenClaw workspace structure and run periodic filesystem health audits. It helps surface broken symlinks, empty directories, large files, malformed names, disk usage, recent changes, and git status before cleanup or backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit can expose workspace metadata such as local paths, directory sizes, git status counts, and recently changed files. <br>
Mitigation: Review audit output before sharing it and keep any scheduled audit logs in a private location. <br>
Risk: Scheduled audit logs may retain filesystem metadata longer than intended. <br>
Mitigation: Enable scheduled logging only when the log destination is private and retention is acceptable. <br>
Risk: The setup script creates a standard directory tree and placeholder files in the selected workspace. <br>
Mitigation: Run setup against the intended workspace path and review existing files before using it in a populated workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/donovanpankratz-del/workspace-organization) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Installation and setup guide](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and plain-text audit output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audit output may include local workspace paths, file sizes, recent file changes, and git status counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
