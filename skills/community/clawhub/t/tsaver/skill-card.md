## Description: <br>
Token Saver guides OpenClaw agents through a five-phase token audit and optimization workflow covering discovery, prioritization, optimization, validation, and monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youxiyin](https://clawhub.ai/user/youxiyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw cron tasks, model routing, context load, and tool profiles, then produce token-saving recommendations and audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to change prompts, cron jobs, model routing, tool profiles, configs, bootstrap files, or monitoring jobs. <br>
Mitigation: Require explicit approval before edits, and review proposed diffs, backups, rollback steps, and validation results before applying changes. <br>
Risk: Generated audit reports may expose private workflow, scheduling, configuration, or model-routing details. <br>
Mitigation: Review reports before sharing and remove sensitive operational details that are not needed by the audience. <br>


## Reference(s): <br>
- [OpenClaw Cron Jobs](https://docs.openclaw.ai/automation/cron.md) <br>
- [OpenClaw Standing Orders](https://docs.openclaw.ai/automation/standing-orders.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown reports, checklists, tables, configuration recommendations, and shell commands when validation requires them.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Full executions produce token-audit-report-YYYY-MM-DD.md with before/after comparisons, estimated weekly savings, deferred items, and recommended next steps.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
