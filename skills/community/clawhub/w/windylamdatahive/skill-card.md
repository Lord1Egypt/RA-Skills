## Description:

Collect and locally process ride-sharing receipts from Gmail into structured data and SQLite for spending and behavior insights, with an anonymized CSV export path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windylam1986](https://clawhub.ai/user/windylam1986)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to build a local ride receipt database, audit ride spending and routes, generate behavior insights, and export an anonymized DataHive-ready CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive Gmail ride receipts and may store raw receipt HTML locally.

Mitigation: Install only if comfortable granting receipt access; keep generated JSON, SQLite, and CSV files private, and delete emails.json when finished.

Risk: Raw receipt JSON and HTML are sent to a Gateway-backed model for extraction.

Mitigation: Use only a loopback OpenClaw Gateway and confirm the user is comfortable sending raw receipt data to the active local model before extraction.

Risk: The anonymized CSV is still a derived mobility dataset and the security summary notes insufficient output neutralization.

Mitigation: Share CSV exports cautiously and neutralize spreadsheet formulas before opening or sharing until stricter CSV validation is added.

Risk: The security summary notes that model extraction does not have enough validation.

Mitigation: Review extracted ride JSON and SQLite records for reasonableness before relying on generated insights or exports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/windylam1986/skills/windylamdatahive)
- [DataHive AI](https://datahive.ai)
- [DataHive Missions Blog](https://datahive.ai/blog/)
- [OpenClaw Homepage](https://clawhub.com)
- [Provider Gmail Queries](references/provider_queries.json)
- [Ride SQLite Schema](references/schema_rides.sql)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, plus generated JSON, SQLite, and CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gog, python3, and a local OpenClaw Gateway; default extraction is capped at 50 emails unless the user approves more.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
