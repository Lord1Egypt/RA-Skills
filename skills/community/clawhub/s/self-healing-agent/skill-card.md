## Description:

Self-recovery and auto-repair system for OpenClaw agents that monitors agent health, detects failures, diagnoses root causes, and applies repairs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check OpenClaw agent health, diagnose cron, memory, config, session, skill, and network failures, and run guided or automatic recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic healing can modify OpenClaw config, memory, session, and cron state.

Mitigation: Run check or heal --dry-run first, review proposed changes, and keep backups of ~/.openclaw/openclaw.json, memory, and sessions before enabling repairs.

Risk: Continuous monitor mode can repeatedly apply repairs without close supervision.

Mitigation: Start with a conservative interval and max-heals value, review the healing log after early cycles, and avoid monitor mode until file paths and repair behavior are understood.

Risk: Cron and session repair actions may restart jobs or archive session files in ways that affect active workflows.

Mitigation: Use targeted checks for cron and sessions before running heal, and confirm that active jobs or sessions can tolerate repair actions.

## Reference(s):

- [Self-Healing Agent ClawHub release](https://clawhub.ai/stevojarvisai-star/skills/self-healing-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text, JSON diagnostics, and Markdown health reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can log healing actions to memory/self-healing-log.json]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
