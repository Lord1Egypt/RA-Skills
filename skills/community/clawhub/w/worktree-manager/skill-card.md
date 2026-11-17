## Description:

Manage Docker-based dev instances and git worktrees, including app container lifecycle, database seeding, and proxy route activation after mysql-manager and proxy-manager are running.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pereirajair](https://clawhub.ai/user/pereirajair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to manage local Docker development instances tied to git worktrees, seed per-instance MySQL databases, and activate local frontend and backend proxy routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive cleanup can remove containers, a database, a git worktree, and an environment file.

Mitigation: Run list first, confirm the exact target instance before removal, and use the skill only in disposable local development repositories unless destructive paths are hardened to fail closed.

Risk: Shared MySQL access and default credentials can affect real or shared data.

Mitigation: Use a non-default least-privilege MySQL credential and avoid connecting the skill to valuable local work, production data, or shared databases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pereirajair/skills/worktree-manager)
- [Publisher profile](https://clawhub.ai/user/pereirajair)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs local development commands, environment setup steps, instance URLs, and operational cautions for Docker, git worktrees, MySQL, and nginx-proxy.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
