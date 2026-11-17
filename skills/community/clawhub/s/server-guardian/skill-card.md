## Description:

Server Guardian helps agents monitor OpenClaw server health, diagnose slowdowns or outages, and guide recovery actions for Gateway, process, memory, disk, log, and OOM conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efgyuhhgy](https://clawhub.ai/user/efgyuhhgy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check OpenClaw server health, investigate Gateway or bot availability problems, and decide when to run recovery actions. It is intended for operational troubleshooting where service restarts, log cleanup, memory cleanup, and configuration guidance may be relevant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recovery actions can restart services and change host runtime state.

Mitigation: Run the health check separately first and require operator approval before invoking recovery actions on production systems.

Risk: Full recovery may drop caches, delete old compressed logs, clean package caches, or terminate high-memory processes.

Mitigation: Review the planned action, confirm affected paths and processes, and avoid unrestricted root execution unless those side effects are acceptable.

Risk: Unattended scheduled full recovery can mask incidents or apply broad cleanup without review.

Mitigation: Use scheduled checks for alerting, and reserve full recovery for supervised maintenance or documented incident response.

## Reference(s):

- [Alert threshold reference](references/thresholds.md)
- [ClawHub skill page](https://clawhub.ai/efgyuhhgy/skills/server-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and operational status descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include health status categories, recovery recommendations, and commands for OpenClaw Gateway operations.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
