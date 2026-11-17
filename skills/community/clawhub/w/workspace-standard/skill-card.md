## Description:

Set up and maintain a structured OpenClaw workspace with project boundaries, role-based file taxonomy, memory budgets, and maintenance tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcus-daemon](https://clawhub.ai/user/marcus-daemon)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to bootstrap, organize, audit, and maintain markdown-based OpenClaw workspaces so files have clear project boundaries, roles, freshness signals, and memory budgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The init workflow creates persistent workspace directories and template files.

Mitigation: Run it in a git-tracked workspace, review the target path first, and inspect git changes before committing.

Risk: The README includes a curl-based script download path.

Mitigation: Prefer the bundled scripts from the installed skill, or inspect downloaded scripts before executing them.

Risk: Using --force may overwrite existing generated files.

Mitigation: Avoid --force unless the destination has been reviewed and existing files are backed up or version controlled.

Risk: Unsanitized project names could create confusing paths.

Mitigation: Use simple project names without slashes, parent-directory segments, or shell metacharacters.

## Reference(s):

- [Workspace Standard ClawHub Page](https://clawhub.ai/marcus-daemon/skills/workspace-standard)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Roles Guide](references/roles-guide.md)
- [Maintenance Checklist](references/maintenance-checklist.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and optional configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or audit workspace files when the bundled scripts are run by the agent or user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
