## Description:

Complete maintenance system for OpenClaw with unified architecture, filesystem governance, and cross-platform design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jazzqi](https://clawhub.ai/user/jazzqi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan and run OpenClaw maintenance workflows, including monitoring, cleanup, log management, health checks, backup, and rollback guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes one-click setup and scheduled maintenance actions that may affect cron jobs, cleanup paths, backups, service restarts, and webhooks.

Mitigation: Inspect the exact scripts from a pinned commit or signed release, confirm configured paths and scheduled jobs, and run dry-run, test, or status commands before enabling automation.

Risk: Automated recovery and service-control commands can disrupt a running OpenClaw environment if used without review.

Mitigation: Test in a non-production environment first, verify backup and rollback behavior, and require operator review before force or restore commands are used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jazzqi/skills/system-maintenance-test)
- [Project homepage](https://github.com/jazzqi/openclaw-system-maintenance)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes maintenance schedules, command references, setup guidance, and operational checks.]

## Skill Version(s):

1.3.2 (source: ClawHub release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
