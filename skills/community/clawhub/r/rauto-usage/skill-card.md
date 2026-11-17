## Description:

Runs and plans rauto operations for network devices, including command execution, templates, transactional workflows, orchestration, replay, backup/restore, and connection/profile/template/history management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[demohiiiii](https://clawhub.ai/user/demohiiiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network operators use this skill to have an agent execute or prepare rauto CLI and web operations for device queries, configuration changes, transactional workflows, multi-device orchestration, replay, backup/restore, and runtime asset management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle network-device credentials and saved connection data.

Mitigation: Prefer protected saved connections or an external secret manager, avoid inline passwords and --save-password unless storage behavior is understood, and sanitize command output before sharing.

Risk: The skill can execute destructive or configuration-changing rauto operations against real devices.

Mitigation: Require dry-run and explicit confirmation before deletes, replace restores, orchestration, or configuration changes, and include a rollback path before live execution.

Risk: Rauto records, backups, and history may contain sensitive operational data.

Mitigation: Protect ~/.rauto records, backups, and history with appropriate filesystem permissions and retention controls.

Risk: Multi-device orchestration can have weak target scoping or incomplete rollback boundaries.

Mitigation: Review target scope, fail_fast behavior, concurrency, and rollback boundary before execution, and use canary or staged rollout when appropriate.

## Reference(s):

- [Rauto Agent Execution Playbook](references/agent-execution.md)
- [Rauto CLI Reference](references/cli.md)
- [Multi-Device Orchestration JSON Templates](references/orchestration-json-template.md)
- [Multi-Device Orchestration Risk Check](references/orchestration-risk-check.md)
- [Tx Workflow JSON Templates](references/workflow-json-template.md)
- [Rauto Usage Scenarios](references/scenarios.md)
- [Rauto Troubleshooting](references/troubleshooting.md)
- [Rauto Paths](references/paths.md)
- [Rauto Web UI Reference](references/web.md)
- [Rauto Execution-Style Prompt Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include rauto CLI commands, rollback-aware plans, dry-run and confirmation notes, and summarized execution results.]

## Skill Version(s):

0.2.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
