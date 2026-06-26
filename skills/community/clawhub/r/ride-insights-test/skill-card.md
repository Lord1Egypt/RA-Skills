## Description: <br>
Build a local SQLite ride-history database from Gmail ride receipt emails using gog for fetch and OpenClaw Gateway /v1/responses for extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuleyko](https://clawhub.ai/user/tuleyko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch ride receipt emails from Gmail, extract structured ride records with a Gateway-backed model, store them in SQLite, summarize ride history, and export anonymized CSV reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ride receipts can contain sensitive financial and location data, and emails.json may store raw receipt email content locally. <br>
Mitigation: Use a narrow date range, protect or delete generated data files after use, and share only the anonymized CSV report when a shareable output is needed. <br>
Risk: Raw receipt email JSON or HTML is sent to the configured Gateway-backed model during extraction. <br>
Mitigation: Prefer a loopback or private Gateway and enable the non-local Gateway override only when the destination is explicitly trusted. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/tuleyko/ride-insights-test) <br>
- [Publisher profile](https://clawhub.ai/user/tuleyko) <br>
- [Provider Gmail queries](artifact/references/provider_queries.json) <br>
- [SQLite ride schema](artifact/references/schema_rides.sql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and generated local JSON, SQLite, and CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local ride data artifacts under data/gateway-llm, including emails.json, rides.json, rides.sqlite, summaries, and an anonymized CSV report when requested.] <br>

## Skill Version(s): <br>
0.1.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
