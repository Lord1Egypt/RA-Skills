## Description:

分层任务分解与执行工作流。

This skill is ready for commercial/non-commercial use.

## Publisher:

[whoisme007](https://clawhub.ai/user/whoisme007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to break complex tasks into hierarchical phases, steps, and substeps, then generate project structure, execution records, reports, and recovery guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because workflow execution and backup code can handle local files and remote backups without enough scoping or user control.

Mitigation: Review before installing, use a non-sensitive test workspace first, and keep backup, Git backup, email, and background progress reporting disabled unless explicitly needed.

Risk: Imported or untrusted project step files could affect workflow behavior during execution.

Mitigation: Do not run imported or untrusted project step files; review generated steps and project files before enabling execution.

Risk: Remote Git backup configuration may move workspace data outside the local environment.

Mitigation: Avoid configuring a remote Git repository until path containment, secret exclusions, destination allowlisting, and explicit confirmation prompts are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whoisme007/skills/xiaolongxia-workflow)
- [workflow_overview.md](references/workflow_overview.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON files, shell commands, and Python code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create project files, logs, reports, backups, and progress artifacts when its workflow scripts are used.]

## Skill Version(s):

0.5.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
