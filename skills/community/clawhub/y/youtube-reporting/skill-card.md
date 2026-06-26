## Description: <br>
YouTube Reporting API integration with managed OAuth for scheduling and downloading bulk YouTube Analytics reports as CSV files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect a YouTube Reporting OAuth account through Maton, schedule or inspect bulk reporting jobs, and download generated YouTube Analytics CSV reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and OAuth connection that can access YouTube channel reporting data. <br>
Mitigation: Install only when Maton is trusted for this use case, keep MATON_API_KEY private, and avoid sharing connection session URLs in logs or transcripts. <br>
Risk: Multiple YouTube Reporting connections can cause requests to target the wrong account. <br>
Mitigation: Confirm the selected account and use the Maton-Connection header when more than one connection is available. <br>
Risk: Creating or deleting reporting jobs changes ongoing report generation. <br>
Mitigation: Approve job and connection changes only after confirming the report type, target account, and expected ongoing effect. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/youtube-reporting) <br>
- [Maton Homepage](https://maton.ai) <br>
- [YouTube Reporting API Overview](https://developers.google.com/youtube/reporting) <br>
- [YouTube Reporting API Reference](https://developers.google.com/youtube/reporting/v1/reference/rest) <br>
- [YouTube Reporting Bulk Reports](https://developers.google.com/youtube/reporting/v1/reports) <br>
- [YouTube Reporting Report Types](https://developers.google.com/youtube/reporting/v1/report_types) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text] <br>
**Output Format:** [Markdown with inline Python, JavaScript, shell commands, HTTP examples, and JSON or CSV API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized YouTube Reporting OAuth connection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; skill frontmatter version is 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
