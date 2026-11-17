## Description:

Roadbook Csv turns itinerary location data in CSV format into a Cyeam roadbook sharing link with map visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mnhkahn](https://clawhub.ai/user/mnhkahn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to format multi-day itinerary stops as CSV, submit them to Cyeam, and return a roadbook URL and QR code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Itinerary names, addresses, dates, and notes are sent to Cyeam-operated services and stored remotely.

Mitigation: Ask for confirmation before posting CSV, avoid sensitive personal details, and tell users that generated roadbook data may be retained temporarily.

Risk: Shell curl examples can be unsafe if user-provided CSV is interpolated directly into a command.

Mitigation: Pass CSV via stdin or a structured HTTP client, and never print or log CYEAM_API_KEY.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mnhkahn/skills/roadbook-csv-1-0-0)
- [Cyeam roadbook CSV API](https://cyeam-open-main-d02895c.d2.zuplo.dev/api/roadbook/csv)
- [Cyeam roadbook viewer](https://www.cyeam.com/tool/roadbook?id={id})
- [Cyeam open platform](https://cyeam-open-main-d02895c.zuplo.site/api/~endpoints)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with CSV snippets, curl commands, generated sharing URLs, and QR-code data returned by the API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CYEAM_API_KEY and curl; posts itinerary/location CSV to Cyeam-operated endpoints.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
