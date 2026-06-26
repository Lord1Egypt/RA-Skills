## Description: <br>
Local-only skill: fetch ride receipt emails from Gmail via gog, store them in local JSON, send raw receipt JSON/HTML to a loopback OpenClaw Gateway model for structured extraction, load the extracted rides into SQLite, generate ride-behavior insights, and export an anonymized DataHive-ready CSV from Uber, Bolt, Lyft, Yandex, Free Now, Curb, or Via receipts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windylam1986](https://clawhub.ai/user/windylam1986) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect ride receipt emails, convert them into local structured ride records, analyze ride spending and behavior, and export a shareable anonymized ride report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched ride receipt emails may include full HTML content and sensitive financial or location details stored in data/ride-insights/emails.json. <br>
Mitigation: Confirm the Gmail account and date scope before fetching, keep the data local, and review or delete data/ride-insights files when finished. <br>
Risk: Extraction sends raw per-email JSON and receipt HTML to the active Gateway-backed model. <br>
Mitigation: Use only a trusted local OpenClaw Gateway; the bundled extractor refuses non-local Gateway hosts. <br>
Risk: The anonymized CSV removes direct identifiers but can still reveal derived ride-location patterns. <br>
Mitigation: Treat exported CSV files as sensitive location data and review them before sharing. <br>


## Reference(s): <br>
- [Skill listing](https://clawhub.ai/windylam1986/windylamdatahive) <br>
- [ClawHub homepage](https://clawhub.com) <br>
- [DataHive AI](https://datahive.ai) <br>
- [DataHive missions blog](https://datahive.ai/blog/) <br>
- [Provider Gmail queries](references/provider_queries.json) <br>
- [Ride SQLite schema](references/schema_rides.sql) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, json, code, markdown, files] <br>
**Output Format:** [Markdown guidance with bash commands plus local JSON, SQLite, and CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default extraction is capped at 50 emails unless the user approves more; generated files are stored locally under data/ride-insights.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
