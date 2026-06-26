## Description: <br>
Reports AI token usage and estimated costs for OpenClaw sessions, cron jobs, subagents, and model-level spend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to answer cost and usage questions for current or recent OpenClaw activity, including daily, weekly, session, cron, and subagent reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to shell-source a hidden local .context file, which can load unreviewed local configuration. <br>
Mitigation: Install only in a trusted OpenClaw environment, review the .context file before use, and avoid shell-sourcing it when direct variable parsing is sufficient. <br>
Risk: The skill can save daily token-history entries, which may preserve inaccurate or unintended cost data. <br>
Mitigation: Require explicit confirmation before appending daily reports and review generated entries before relying on them. <br>


## Reference(s): <br>
- [Usage Costs on ClawHub](https://clawhub.ai/netanel-abergel/usage-costs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown cost reports with inline shell and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append daily cost summaries to local token-history JSONL when explicitly used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
