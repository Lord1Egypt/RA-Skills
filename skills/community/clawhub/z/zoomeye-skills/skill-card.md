## Description:

Integrates the ZoomEye cyberspace search API for asset search, host discovery, web application detection, resource statistics, and threat-intelligence analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and threat-intelligence analysts use this skill to query ZoomEye for internet-exposed hosts, web applications, service fingerprints, and aggregate resource statistics during authorized asset discovery and security assessment work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches and target identifiers may be sent to ZoomEye as third-party reconnaissance activity.

Mitigation: Use the skill only for authorized asset discovery or threat-intelligence work, and avoid querying third-party targets without permission.

Risk: ZoomEye API credentials are required for the skill to function.

Mitigation: Store ZOOMEYE_API_KEY in the agent environment and do not include secrets or private internal details in search parameters.

Risk: API quota and rate limits can affect result completeness or availability.

Mitigation: Check user quota before large searches and use precise queries or pagination to control request volume.

## Reference(s):

- [ZoomEye Query Syntax Reference](references/query_syntax.md)
- [ZoomEye API Endpoint](https://api.zoomeye.org)
- [ZoomEye API Key Registration](https://www.zoomeye.org/pricing?aff=INVITE-4KZ6-640E)
- [ClawHub Skill Page](https://clawhub.ai/moxin1044/skills/zoomeye-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZOOMEYE_API_KEY and sends search queries to ZoomEye.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
