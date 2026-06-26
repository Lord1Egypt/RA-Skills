## Description: <br>
Generate team quality daily report automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bondli](https://clawhub.ai/user/bondli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team quality owners use this skill to fetch configured dashboard metrics, compare them with the previous day's data, and produce daily quality reports for team syncs, project monitoring, and management updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reuses a live browser login and captures dashboard API request payloads. <br>
Mitigation: Run it only with authorized access, preferably through a dedicated low-privilege browser profile or service account. <br>
Risk: Generated JSON and Markdown reports may contain sensitive team or business metrics. <br>
Mitigation: Store the output in a protected location and periodically delete files that are no longer needed. <br>
Risk: Scheduled execution can repeatedly query internal systems without interactive review. <br>
Mitigation: Inspect config.json and run the skill manually before enabling cron or other automation. <br>


## Reference(s): <br>
- [README.md](artifact/README.md) <br>
- [Configuration example](artifact/config.example.json) <br>
- [ClawHub release page](https://clawhub.ai/bondli/team-quality-daily-report) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Configuration] <br>
**Output Format:** [Markdown daily report and JSON metric snapshot saved as dated files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured dashboard URL, API endpoint, and metric column mappings; compares with the prior day's saved JSON when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
