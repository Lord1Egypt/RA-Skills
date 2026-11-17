## Description:

Hot China helps agents fetch live Chinese trend, music, entertainment, app chart, and People's Daily newspaper data as JSON using local Node.js crawler scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gfhe](https://clawhub.ai/user/gfhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when an agent needs current Chinese hot-search rankings, music charts, entertainment rankings, App Store charts, or People's Daily newspaper page metadata. The skill selects the relevant crawler command and returns live public data in a consistent JSON structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger examples may cause the agent to run a crawler for vague news or recommendation requests.

Mitigation: Clarify the requested platform, category, or date before execution when the user's intent is ambiguous.

Risk: Live public platform data may be incomplete, unavailable, or change between runs.

Mitigation: Report the source platform and retrieval time when available, and clearly surface empty or failed crawler results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gfhe/skills/web-hot-cn)
- [API endpoints and command parameters](references/api-endpoints.md)
- [Crawler data formats](references/data-formats.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with Node.js shell commands and JSON crawler output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and live network access; no API key, credentials, persistence, or local data access are reported in the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
