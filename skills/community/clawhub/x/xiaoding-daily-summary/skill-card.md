## Description: <br>
Generates a dated Markdown daily summary that includes OpenClaw token usage, task progress, and next-day planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users who track daily agent activity use this skill to generate a Markdown report summarizing token usage, completed work, task status, and the next day's plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily summaries may record sensitive local task details or usage information. <br>
Mitigation: Review generated summaries before sharing and keep the OpenClaw memory folder access-restricted. <br>
Risk: The skill depends on reading local OpenClaw usage via openclaw status --json. <br>
Mitigation: Install only in environments where the agent is allowed to read local OpenClaw usage status. <br>
Risk: Scheduled automation could run outside an interactive review flow. <br>
Mitigation: Inspect any separate cron script before enabling scheduled execution. <br>


## Reference(s): <br>
- [Daily Summary on ClawHub](https://clawhub.ai/asterisk622/xiaoding-daily-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown daily summary file with a brief text response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a dated summary to the OpenClaw memory folder when the local OpenClaw status command is available.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact SKILL.md and package.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
