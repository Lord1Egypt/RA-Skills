## Description: <br>
PulseFlow maintains a Markdown task dashboard with append-only AI work logs, then syncs daily AI DONE TODAY and weekly usage panels through heartbeat or on-demand refresh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayao99315](https://clawhub.ai/user/ayao99315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use PulseFlow to keep human task planning, AI execution logs, weekly usage visibility, and monthly history aligned in a reusable local workspace workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured file paths may target unintended dashboards, history folders, reports, or AGENTS.md files. <br>
Mitigation: Review todo/system/config.json before running scripts, especially dashboardPath, historyDir, reportsDir, syncStatePath, and agentsFilePath. <br>
Risk: Optional summary cron installation can schedule agents to read dashboard and log files and write summary archives. <br>
Mitigation: Run scripts/install_summary_crons.js with --dry-run first and enable summaryCrons only in workspaces where scheduled summaries are intended. <br>
Risk: Managed AGENTS.md rule installation changes agent operating instructions so completed work is appended to AI logs. <br>
Mitigation: Enable AGENTS.md rule installation only for intended agents and confirm the managed rule block after installation. <br>


## Reference(s): <br>
- [PulseFlow release page](https://clawhub.ai/ayao99315/pulseflow) <br>
- [Publisher profile](https://clawhub.ai/user/ayao99315) <br>
- [Design](docs/design.md) <br>
- [File Specification](docs/file-spec.md) <br>
- [Lifecycle](docs/lifecycle.md) <br>
- [Portability Notes](docs/portability.md) <br>
- [Agent Log Format](references/agent-log-format.md) <br>
- [Config Template](references/config-template.json) <br>
- [Recovery Playbook](references/recovery-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local dashboard, history, sync-state, AI log, AGENTS.md, and optional cron configuration files when the documented scripts are run.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
