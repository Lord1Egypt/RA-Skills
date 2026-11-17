## Description:

Five-phase token audit and optimization framework for OpenClaw agents, covering discovery, prioritization, optimization, validation, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youxiyin](https://clawhub.ai/user/youxiyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit OpenClaw token usage, prioritize savings opportunities, and produce recommended prompt, model-routing, cron, and gateway configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local OpenClaw cron and gateway configuration while auditing token usage.

Mitigation: Run an initial read-only audit and require the agent to list exact paths inspected before making any changes.

Risk: The skill can propose or perform persistent prompt, routing, scheduled task, or gateway configuration changes, including changes labeled Safe.

Mitigation: Require exact diffs and explicit approval for every write, cron update, routing change, or gateway configuration change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youxiyin/skills/wave-token-saver)
- [OpenClaw Cron Jobs](https://docs.openclaw.ai/automation/cron.md)
- [OpenClaw Standing Orders](https://docs.openclaw.ai/automation/standing-orders.md)
- [Test prompts](artifact/test-prompts.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, recommendations, and occasional shell or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A full execution produces token-audit-report-YYYY-MM-DD.md and may recommend or perform prompt, model-routing, cron, and gateway configuration updates.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
