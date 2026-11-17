## Description:

Maintain a Markdown task dashboard backed by agent-written append-only AI work logs, then sync a daily AI DONE TODAY section plus a weekly usage panel via heartbeat or on-demand refresh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayao99315](https://clawhub.ai/user/ayao99315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use PulseFlow to maintain a reusable local work dashboard where human tasks, AI work logs, weekly usage visibility, and monthly history stay aligned through initialization, heartbeat sync, repair, and rollover workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local dashboards, logs, and history can contain AI work summaries and task details.

Mitigation: Install PulseFlow only in workspaces where local retention of those details is acceptable, and define retention expectations before use.

Risk: AGENTS.md rule installation changes agent operating instructions for configured agents.

Mitigation: Review managed rule changes before enabling installation and configure only the intended agent files.

Risk: Optional summary crons can run on a schedule and deliver work summaries to configured targets.

Mitigation: Use the dry run first, set trusted internal delivery targets, and verify timezone, paths, agent names, and cron timing.

## Reference(s):

- [PulseFlow ClawHub Page](https://clawhub.ai/ayao99315/skills/pulseflow)
- [README](README.md)
- [Design](docs/design.md)
- [File Specification](docs/file-spec.md)
- [Lifecycle](docs/lifecycle.md)
- [Portability](docs/portability.md)
- [Agent Log Format](references/agent-log-format.md)
- [Configuration Template](references/config-template.json)
- [Heartbeat Checklist](references/heartbeat-checklist.md)
- [Recovery Playbook](references/recovery-playbook.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown dashboards and archives, JSON/JSONL state and logs, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local files and a JavaScript runtime; optional summary cron installation is configuration-driven.]

## Skill Version(s):

1.2.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
