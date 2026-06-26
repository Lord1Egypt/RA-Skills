## Description: <br>
Set up and maintain a structured OpenClaw workspace with project boundaries, role-based file taxonomy, and memory budgets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcus-daemon](https://clawhub.ai/user/marcus-daemon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to bootstrap, organize, audit, and maintain OpenClaw workspaces with consistent project boundaries, role-based markdown files, memory budgets, and maintenance routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace maintenance guidance can lead to broad git commits, pushes, or cleanup commands if followed without review. <br>
Mitigation: Inspect git status and git diff first, avoid automatic git push, and preview cleanup with git clean -fdn before any destructive cleanup. <br>
Risk: Generated memory and entity files may contain sensitive workspace details. <br>
Mitigation: Review generated files before committing or sharing them and keep secrets out of memory, entity, and project reference files. <br>
Risk: The skill may reorganize workspace knowledge in ways that affect agent behavior and file lookup habits. <br>
Mitigation: Run the audit first, review proposed migrations before moving files, and make changes in reversible git commits. <br>


## Reference(s): <br>
- [Workspace Standard ClawHub page](https://clawhub.ai/marcus-daemon/workspace-standard) <br>
- [The Seven Roles - Detailed Guide](references/roles-guide.md) <br>
- [Workspace Maintenance Checklist](references/maintenance-checklist.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes shell scripts that create workspace files and audit existing workspace structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
