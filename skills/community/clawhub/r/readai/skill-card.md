## Description:

Fetch and manage Read AI meeting data, including summaries, transcripts, action items, search results, webhook payloads, and engagement metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandons7](https://clawhub.ai/user/brandons7)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to retrieve, search, export, and receive meeting intelligence from Read AI and Limitless sources. It supports meeting summaries, transcripts, action items, participant details, decisions, local digests, and webhook ingestion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting transcripts, participant details, webhook payloads, and lifelog records can contain highly sensitive personal or business information stored under ~/.readai.

Mitigation: Install only where local storage of this data is approved, use restrictive directory and file permissions, and regularly review or purge cached records.

Risk: A publicly exposed webhook receiver can accept untrusted meeting payloads without built-in signature or token validation.

Mitigation: Keep the receiver bound to localhost unless protected by HTTPS, authentication or signature validation, rate limits, and request-size limits.

Risk: Using the optional AI digest path can send conversation excerpts through the Claude CLI.

Mitigation: Use --ai only when that external processing path is acceptable for the meeting or lifelog data being summarized.

## Reference(s):

- [Read AI API Reference](references/api-reference.md)
- [Read AI API base URL](https://api.read.ai/v1)
- [Limitless API base URL](https://api.limitless.ai/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown, JSON, and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache meeting records, webhook payloads, transcripts, lifelogs, indexes, and generated digests under ~/.readai.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
