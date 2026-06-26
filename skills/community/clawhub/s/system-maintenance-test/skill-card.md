## Description: <br>
Complete maintenance system for OpenClaw with unified architecture, filesystem governance, and cross-platform design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jazzqi](https://clawhub.ai/user/jazzqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan OpenClaw maintenance workflows, including monitoring, cleanup, log management, health checks, backup, rollback, and service recovery tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run maintenance scripts that can create recurring jobs, change files and logs, restore backups, and restart services. <br>
Mitigation: Inspect the repository and installer scripts at the exact version you intend to run, confirm the planned cron, file, log, service, backup, and .learnings changes, and verify rollback steps before setup or emergency recovery. <br>
Risk: Automated cleanup or recovery could affect system state if used without environment-specific review. <br>
Mitigation: Use test, dry-run, status, or report-only modes where available, then monitor the first scheduled runs and disable the automation if behavior is unexpected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jazzqi/system-maintenance-test) <br>
- [Project homepage](https://github.com/jazzqi/openclaw-system-maintenance) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review proposed commands and configuration changes before running them in a target environment.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
