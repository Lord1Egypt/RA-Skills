## Description:

Timestamp conversion tool. Convert between Unix timestamp, datetime, and various date formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeter226](https://clawhub.ai/user/freeter226)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert Unix timestamps and datetime strings, format dates, get current time values, and calculate differences for log analysis, API development, data processing, and debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: README content and the human-readable diff field are Chinese-localized, which may surprise users expecting English-only output.

Mitigation: Rely on the structured JSON keys and numeric fields for automation, and document the localized human-readable field for users who need English-only workflows.

Risk: Local-time conversions can vary by runtime environment, and non-utc timezone values are treated as local time by the artifact script.

Mitigation: Use the utc option for reproducible conversions and validate timezone assumptions before using converted times in logs, APIs, or data pipelines.

## Reference(s):

- [Timestamp Toolkit ClawHub skill page](https://clawhub.ai/freeter226/skills/timestamp-toolkit)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON objects printed by a Python command, with Markdown command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3. Results include success/error status, converted timestamp or datetime fields, and a localized human-readable diff field.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
