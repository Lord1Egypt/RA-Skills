## Description:

Five-phase token audit and optimization framework for OpenClaw agents covering discovery, prioritization, optimization, validation, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youxiyin](https://clawhub.ai/user/youxiyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit OpenClaw token consumption, prioritize high-impact savings, optimize prompts, model routing, context loading, and tool profiles, then validate and monitor the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change persistent OpenClaw configuration, prompts, model routing, tool settings, and memory or history files.

Mitigation: Run it in read-only audit mode first, require exact diffs and backups before persistent changes, and keep a clear rollback plan.

Risk: Quick Wins and Express Audit paths may encourage direct changes before a full validation pass.

Mitigation: Use those paths only for explicitly approved files and run the validation steps before keeping configuration or prompt changes.

## Reference(s):

- [Token Saver ClawHub Page](https://clawhub.ai/youxiyin/skills/tsaver)
- [OpenClaw Cron Jobs](https://docs.openclaw.ai/automation/cron.md)
- [OpenClaw Standing Orders](https://docs.openclaw.ai/automation/standing-orders.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with tables, recommendations, inline shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full executions produce token-audit-report-YYYY-MM-DD.md with before/after comparisons, estimated savings, deferred items, and next steps.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
