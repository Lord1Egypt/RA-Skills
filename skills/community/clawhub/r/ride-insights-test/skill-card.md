## Description:

Build a local SQLite ride-history database from Gmail ride receipt emails using gog for fetch and OpenClaw Gateway /v1/responses for extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuleyko](https://clawhub.ai/user/tuleyko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to fetch ride receipt emails, extract structured ride records through a local or private Gateway-backed model, store them in SQLite, summarize ride history, and export an anonymized CSV report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ride receipt emails can include sensitive financial and location data, including full HTML receipt content in emails.json.

Mitigation: Review before installation, limit the date scope, store generated files in a private directory, and delete raw email exports when they are no longer needed.

Risk: Raw receipt content and a Gateway token are used during extraction.

Mitigation: Prefer a loopback Gateway URL, avoid remote plaintext HTTP Gateway targets, and use a short-lived token when available.

Risk: CSV exports may still reveal travel patterns through dates, cities, amounts, and providers.

Mitigation: Share only the anonymized CSV when needed, review it before distribution, and use care when opening it in spreadsheet software.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuleyko/skills/ride-insights-test)
- [Ride SQLite schema](artifact/references/schema_rides.sql)
- [Provider Gmail queries](artifact/references/provider_queries.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, JSON, SQLite database, CSV]

**Output Format:** [Markdown guidance with shell commands; generated artifacts include JSON, SQLite, and CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local files under data/gateway-llm and can attach the anonymized CSV through the host agent's media mechanism.]

## Skill Version(s):

0.1.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
