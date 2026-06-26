## Description: <br>
Rauto Usage executes rauto device commands, templates, transaction blocks, transaction workflows, multi-device orchestration, replay, backup/restore, and connection/profile/template/history operations directly for users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[demohiiiii](https://clawhub.ai/user/demohiiiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network operators and automation engineers use this skill to run rauto operations against managed devices, inspect saved state, prepare rollback-aware changes, and summarize execution results. It is intended for agents operating on devices and local rauto state that the user controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authority to run rauto operations that can affect real devices. <br>
Mitigation: Install it only for devices you control, use dry-runs and canary scopes before live changes, and confirm restore, delete, and orchestration targets explicitly. <br>
Risk: Credentials, recordings, histories, saved connections, and backups may expose sensitive local state. <br>
Mitigation: Prefer named connections or secure prompts over command-line passwords, avoid printing real secrets in exact command summaries, and protect or periodically clean ~/.rauto state. <br>


## Reference(s): <br>
- [Rauto Agent Execution Playbook](references/agent-execution.md) <br>
- [Rauto CLI Reference](references/cli.md) <br>
- [Rauto Execution-Style Prompt Examples](references/examples.md) <br>
- [Multi-Device Orchestration JSON Templates](references/orchestration-json-template.md) <br>
- [Multi-Device Orchestration Risk Check](references/orchestration-risk-check.md) <br>
- [Rauto Paths](references/paths.md) <br>
- [Rauto Usage Scenarios](references/scenarios.md) <br>
- [Rauto Troubleshooting](references/troubleshooting.md) <br>
- [Rauto Web UI Reference](references/web.md) <br>
- [Tx Workflow JSON Templates](references/workflow-json-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Executed-command summaries include operation, exact command, result, and risk notes when applicable.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
