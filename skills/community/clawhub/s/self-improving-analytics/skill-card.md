## Description: <br>
Captures data quality issues, metric drift, pipeline failures, misleading visualizations, metric definition mismatches, and data freshness problems to enable continuous analytics improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analytics engineers, and data teams use this skill to capture recurring analytics issues, data quality lessons, metric definition conflicts, and improvement requests so they can be reviewed and promoted into durable analytics standards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent analytics learning logs and reminders can influence future agent behavior beyond the immediate task. <br>
Mitigation: Prefer project-local setup, review generated or modified guidance files before trusting them, and keep logged entries concise and relevant. <br>
Risk: Optional hooks can inspect broad command output and may surface analytics reminders in unrelated contexts if enabled too widely. <br>
Mitigation: Use analytics-specific hook filters where possible, avoid global user-level hooks, and leave Bash output detection disabled unless needed. <br>
Risk: Analytics logs may accidentally capture connection strings, credentials, API keys, PII, or raw query results. <br>
Mitigation: Redact sensitive values, summarize failures instead of storing full outputs, and follow the skill guidance not to log credentials or PII. <br>


## Reference(s): <br>
- [Self-Improving Analytics on ClawHub](https://clawhub.ai/jose-compu/self-improving-analytics) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and reusable log-entry templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local .learnings markdown files when the agent follows the workflow; optional hooks can inject reminders.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
