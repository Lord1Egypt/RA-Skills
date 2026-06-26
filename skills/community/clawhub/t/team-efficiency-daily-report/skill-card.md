## Description: <br>
Generate team efficiency daily report automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bondli](https://clawhub.ai/user/bondli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Team leads, delivery managers, and engineering teams use this skill to collect configured dashboard metrics and generate daily Markdown reports for delivery tracking, team efficiency syncs, and management reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses authenticated dashboard data and stores generated data and reports locally. <br>
Mitigation: Install and run it only when authorized to access and retain the configured dashboard data, and protect the local output directory. <br>
Risk: Misconfigured dashboard or API URLs could collect data from the wrong source. <br>
Mitigation: Review config.json URLs, API endpoints, and column mappings before running the skill. <br>
Risk: A scheduled cron run can repeatedly collect dashboard data without interactive review. <br>
Mitigation: Add the cron job only when unattended recurring collection is intended, and use a least-privilege browser account when possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bondli/team-efficiency-daily-report) <br>
- [Publisher profile](https://clawhub.ai/user/bondli) <br>
- [README](README.md) <br>
- [Configuration example](config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report and JSON data files, with setup guidance and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes date-stamped daily report and data files under the local team-efficiency-daily-report data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact/package.json declares 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
