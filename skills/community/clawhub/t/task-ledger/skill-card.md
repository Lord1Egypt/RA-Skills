## Description: <br>
Task Ledger provides a durable workflow layer for OpenClaw long-running work by tracking task state, execution bindings, dependencies, recovery notes, logs, and auditable outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gejiliang](https://clawhub.ai/user/gejiliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Task Ledger to make long-running, multi-stage, parallel, scheduled, or side-effectful OpenClaw work recoverable, resumable, dependency-aware, and auditable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can resume or continue side-effectful workflows such as deploy, restart, maintenance, or sync tasks from vague context. <br>
Mitigation: Use explicit task IDs when resuming and verify real system state before continuing any deploy, restart, maintenance, or sync workflow. <br>
Risk: Helper scripts persist task files, logs, reports, execution bindings, and copied toolkit files in the workspace. <br>
Mitigation: Install only in workspaces where persistent operational files are acceptable and review generated files before sharing or committing them. <br>
Risk: Exported reports can contain process, session, subtask, or cron identifiers. <br>
Mitigation: Review and redact exported reports before sharing them outside the intended workspace or team. <br>


## Reference(s): <br>
- [Task Ledger on ClawHub](https://clawhub.ai/gejiliang/task-ledger) <br>
- [Publisher profile](https://clawhub.ai/user/gejiliang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON task files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent workspace files under tasks/, logs/, outputs/, scripts/, and task-templates/ when used.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
