## Description: <br>
Backup readiness and disaster recovery for an OpenClaw agent, including local backup checks, declared offsite-copy status, user-gated backup scheduling, and guidance for rollback and disaster recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavinlinasd](https://clawhub.ai/user/gavinlinasd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to assess whether agent memory, identity, configuration, skills, workspace files, and cron jobs are covered by recent local backups and a declared offsite copy. It can also help manage user-approved backup schedules and provide recovery guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring backup schedules can change ongoing agent behavior if created or modified accidentally. <br>
Mitigation: Require explicit user confirmation before creating, updating, or deleting any backup cron schedule. <br>
Risk: Backup readiness checks can expose sensitive data if file contents or credential paths are inspected. <br>
Mitigation: Limit checks to file names, sizes, and dates; skip credential directories and redact any secret-like value if accidentally observed. <br>
Risk: A local backup alone does not protect against device loss, disk failure, or a wiped home directory. <br>
Mitigation: Report offsite status separately and require a user-maintained offsite marker before treating an offsite copy as confirmed. <br>


## Reference(s): <br>
- [OpenClaw Agent State](https://docs.openclaw.dev/concepts/agent-state) <br>
- [Self Preserve on ClawHub](https://clawhub.ai/gavinlinasd/self-preserve) <br>
- [Self Preserve Repository](https://github.com/gavinlinasd/self-preserve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include backup status tables, at-risk findings, recommended actions, and user-confirmed cron scheduling steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
