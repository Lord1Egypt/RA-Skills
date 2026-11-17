## Description:

Search and analyze global news using SonarBay News Intelligence. Provides real-time access to 7 days of worldwide news coverage via CLI or REST API. Use when the user needs news search, trending entities, mention counts over time, or any news-related data analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pavanxs](https://clawhub.ai/user/pavanxs)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to search recent global news, inspect trending entities, and analyze mention counts over time through the SonarBay CLI or REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installer and self-update instructions can execute mutable code without published verification in the artifact.

Mitigation: Prefer the documented REST API when possible, or require versioned installers with published checksums or signatures before running local code.

## Reference(s):

- [SonarBay](https://sonarbay.com)
- [ClawHub skill page](https://clawhub.ai/pavanxs/skills/sonarbay-news)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands, REST API examples, and optional JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI and REST API access can return live news search results, trending entity data, article metadata, status checks, and time-series count buckets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
