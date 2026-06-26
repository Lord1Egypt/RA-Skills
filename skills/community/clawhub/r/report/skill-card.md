## Description: <br>
Configure custom recurring reports. User defines data sources, skill handles scheduling and formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People and teams use this skill to define recurring reports from user-selected data sources, schedule them, and deliver them through chat, local files, Telegram, email, or webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled reports may continue delivering content after needs or recipients change. <br>
Mitigation: Periodically review ~/report plus active schedules, and pause or archive reports that are no longer needed. <br>
Risk: External delivery through Telegram, email, or webhooks can send report content off-device. <br>
Mitigation: Use local file delivery for sensitive reports, and verify chat IDs, recipients, and webhook URLs before enabling external delivery. <br>
Risk: Reports that use external APIs depend on user-provided credentials. <br>
Mitigation: Use least-privilege API keys and store only environment variable references in report configuration. <br>


## Reference(s): <br>
- [Report Configuration Schema](schema.md) <br>
- [Output Formats](formats.md) <br>
- [Delivery Channels & Scheduling](delivery.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance, report configuration, and generated chat, PDF, HTML, or JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores report configurations and generated reports under ~/report; external delivery depends on user-configured destinations and credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
