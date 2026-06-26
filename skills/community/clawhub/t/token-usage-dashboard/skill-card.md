## Description: <br>
Use CodexBar CLI local cost usage to summarize per-model usage for Codex or Claude, including the current model or a full model breakdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bkes994408-cmd](https://clawhub.ai/user/bkes994408-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to summarize local CodexBar usage and cost data by provider, model, and time range. It can produce a local HTML dashboard, JSON summaries, custom reports, scheduled exports, and tenant-scoped views for LLM usage monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write dashboard summaries, reports, report history, and tenant-specific outputs that may contain usage, cost, prompt-derived, or identity-linked data. <br>
Mitigation: Write outputs only to private local directories, review generated JSON/CSV/HTML before sharing, and avoid using raw prompt or user-identifying payloads unless local export is acceptable. <br>
Risk: Tenant and user-management flags can persistently change or delete access configuration. <br>
Mitigation: Treat tenant-management commands as administrative operations, keep backups of tenant configuration files, and review role, group, and dashboard-view changes before running them. <br>
Risk: The release includes broader dashboard, reporting, and policy-evaluation behavior than a simple per-model usage summary. <br>
Mitigation: Install it only when the full local dashboard and reporting workflow is desired, and test commands with pre-exported sample JSON before pointing the skill at operational data. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/bkes994408-cmd/token-usage-dashboard) <br>
- [Publisher Profile](https://clawhub.ai/user/bkes994408-cmd) <br>
- [CodexBar CLI Quick Reference](references/codexbar-cli.md) <br>
- [Tenant Config Example](docs/TENANT_CONFIG_EXAMPLE.json) <br>
- [Alert Config Example](docs/ALERT_CONFIG_EXAMPLE.json) <br>
- [Cost Control Config Example](docs/COST_CONTROL_CONFIG_EXAMPLE.json) <br>
- [Report Scheduler Example](docs/REPORT_SCHEDULER_EXAMPLE.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus generated HTML, JSON, and CSV files when the bundled scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dashboard and report output paths are configurable; live mode requires the local codexbar CLI on macOS, while pre-exported JSON can be provided as input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
