## Description:

Queries Huoxiaoding customer service records by extracting a customer name and optional date range, searching for matching customers, retrieving records, and summarizing the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adtomato](https://clawhub.ai/user/adtomato)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or authorized support and sales operators use this skill to look up a named customer's service records for a selected date range and receive a concise summary of service count, participants, service types, and time span.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query sensitive customer service records.

Mitigation: Use only when the user and environment are authorized to access those records.

Risk: The API endpoint is caller-configurable and unauthenticated in the artifact.

Mitigation: Restrict network egress to trusted hosts, prefer HTTPS and host allowlisting, and add authentication before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adtomato/skills/query-customer-service-record)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown response with shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a caller-supplied base_url, customer name, and optional start/end dates; defaults to the current day when no date range is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
