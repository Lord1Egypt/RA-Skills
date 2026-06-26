## Description: <br>
Generates token usage statistics and reference cost reports from local OpenClaw session history using Opus 4.7, GPT-5.5, or custom rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinoslug](https://clawhub.ai/user/sinoslug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for recent and monthly token usage, billing-token totals, and estimated CNY costs from local OpenClaw session logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local session history may contain sensitive conversation content, and this skill reads those files to compute usage statistics. <br>
Mitigation: Install only when local session-file access is acceptable; review the script before use and avoid running it on profiles with sensitive history that should not be scanned. <br>
Risk: Cost figures are reference estimates based on configured rates and a fixed USD to CNY conversion, so they may not match actual provider billing. <br>
Mitigation: Treat the report as informational and compare against provider invoices or account dashboards for financial decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sinoslug/token-stats-reporter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text token and cost report with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports last-message and current-month token totals; reads local OpenClaw session JSONL files and does not transmit data according to security evidence.] <br>

## Skill Version(s): <br>
1.5.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
