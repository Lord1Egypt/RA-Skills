## Description: <br>
更新守护者 helps agents manage platform and skill package updates with dry-run checks, snapshots, conflict detection, scheduled maintenance, health checks, and rollback guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan safer automated updates for agent platforms and installed skill packages, including preflight checks, backups, scheduled update windows, and rollback steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run broad platform and skill update, rollback, backup, and scheduling actions. <br>
Mitigation: Review before production or shared-system use, start with dry-run checks, and require manual confirmation before apply, rollback, or schedule changes. <br>
Risk: Loose activation and confirmation boundaries could cause updates to run at unsafe times or with unintended scope. <br>
Mitigation: Set explicit timezone and blackout windows, limit execution to systems where update-manager commands are allowed, and confirm the target skills or platform packages before changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/update-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational update plans, command suggestions, schedules, backup and rollback guidance, and health-check steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
