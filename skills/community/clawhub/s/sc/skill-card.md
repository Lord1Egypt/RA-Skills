## Description:

Supernal Coding CLI helps agents and developers work with task management, requirements tracking, testing, git automation, compliance checks, documentation, and autonomous ralph workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianderrington](https://clawhub.ai/user/ianderrington)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to operate the sc CLI for project task tracking, health checks, requirements traceability, git workflow automation, compliance checks, documentation, and autonomous task execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install example uses an unpinned global npm package.

Mitigation: Pin the npm package to a reviewed version and avoid elevated privileges during installation.

Risk: Autonomous, git automation, cleanup, reindexing, cron, or heartbeat examples may mutate repositories.

Mitigation: Run these workflows only in repositories with backups, reviewable changes, and clear approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ianderrington/skills/sc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands for task state, project files, git workflows, health checks, compliance checks, and autonomous execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
