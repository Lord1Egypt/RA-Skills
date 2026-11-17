## Description:

Durable workflow layer for OpenClaw long-running work that turns multi-stage, recoverable, parallel, background, scheduled, or side-effecting tasks into auditable and resumable task objects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gejiliang](https://clawhub.ai/user/gejiliang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Task Ledger to manage long-running OpenClaw work with durable task state, execution bindings, dependency checks, recovery flow, and short human-facing status backed by file-based reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some helper scripts can read or write outside intended task folders when given unsafe task data.

Mitigation: Use only in trusted workspaces, avoid untrusted task IDs or task JSON, and confirm task-ID validation plus output path containment before sensitive deployments, document sync, cron, or long-running automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gejiliang/skills/task-ledger)
- [README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)
- [Task Templates Guide](artifact/toolkit/task-templates/README.md)
- [Tasks Runtime Directory Guide](artifact/toolkit/tasks/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON, Markdown]

**Output Format:** [Markdown guidance with shell commands, JSON task files, helper scripts, logs, and exported task reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and bash; creates or updates task checkpoint files, logs, output directories, execution bindings, readiness data, and task graph/report exports.]

## Skill Version(s):

0.3.2 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
