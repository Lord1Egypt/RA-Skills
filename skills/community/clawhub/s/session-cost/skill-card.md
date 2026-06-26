## Description: <br>
Analyze OpenClaw session logs to report token usage, costs, and performance metrics grouped by agent and model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khaney64](https://clawhub.ai/user/khaney64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to summarize local session logs, estimate API spending, inspect token usage, and compare costs by agent, provider, model, or session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local OpenClaw session logs may include session IDs, usage history, and spending patterns. <br>
Mitigation: Use --agent, --offset, --provider, or a narrow --path to limit the report scope, and avoid sharing JSON, details, or Discord output when the contents are sensitive. <br>
Risk: The utility reads local session log files from the default OpenClaw agents directory or a user-supplied path. <br>
Mitigation: Run it only when local log access is appropriate, and review the selected path before producing or sharing reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/khaney64/session-cost) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text summaries, compact tables, JSON objects, and Discord-friendly Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports filters for agent, provider, time offset, custom log path, and per-session details.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
