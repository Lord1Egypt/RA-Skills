## Description: <br>
Token Tracker Daily records API token usage, generates daily and weekly usage reports, analyzes trends, and supports optional scheduled reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to log input and output token counts locally, generate daily and weekly Markdown reports, and monitor token usage trends for budgeting and optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local token usage logs may expose usage metadata if the workspace or generated data file is shared. <br>
Mitigation: Protect or delete the local usage log when token-usage metadata is sensitive. <br>
Risk: The scripts write token usage data to a local path that may differ after installation. <br>
Mitigation: Confirm where the Python files are installed and where token_log.json will be written before relying on the reports. <br>
Risk: Optional cron jobs can create recurring report execution. <br>
Mitigation: Add scheduled jobs only when recurring reports are intended and document how to remove them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timyljob2011-sudo/token-tracker-daily) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with tables, trend summaries, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local token usage data; optional cron examples can schedule recurring reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
