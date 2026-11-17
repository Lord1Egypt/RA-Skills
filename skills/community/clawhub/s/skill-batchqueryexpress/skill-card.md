## Description:

Batch queries parcel-tracking information for multiple express numbers and returns logistics status, tracking events, and exportable reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xdccycom](https://clawhub.ai/user/xdccycom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query logistics status for one or more express tracking numbers, including SF shipments that require a phone suffix. It helps agents summarize parcel status, inspect tracking history, and export results for downstream handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking numbers and required phone suffixes are sent to the xdccy service for lookup.

Mitigation: Use the skill only when that data sharing is acceptable, minimize submitted shipment data, and avoid querying shipments without appropriate permission.

Risk: PlatformID, MemberID, and APIKey values can be exposed if pasted directly into shell commands or logs.

Mitigation: Provide credentials through protected environment variables or a secret manager, and avoid storing real API keys in command history, transcripts, or shared files.

Risk: Exported CSV, TXT, JSON, or XLSX files may contain detailed logistics events and contact-related delivery information.

Mitigation: Save exports only to approved locations, restrict sharing, and delete result files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xdccycom/skills/skill-batchqueryexpress)
- [小递查查 credential and API service site](https://xdccy.com)
- [Input format reference](references/input-format.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, files]

**Output Format:** [Console text, JSON, CSV, TXT, or XLSX files depending on query count and output path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include detailed logistics events, timestamps, courier details, phone suffixes, and exported result files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
