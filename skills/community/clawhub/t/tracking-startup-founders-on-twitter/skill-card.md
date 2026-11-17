## Description:

Tracks startup founders and their activity on Twitter using apidojo's Twitter scrapers, returning founder handles, companies, stages, follower counts, recent topics, and build-in-public signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

VCs, accelerators, partnership teams, and startup ecosystem researchers use this skill to discover, classify, and monitor startup founders on X/Twitter by sector, stage, relevance, and build-in-public signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify API tokens can be exposed when placed directly in example request URLs.

Mitigation: Use a narrowly scoped Apify token, prefer MCP or an authorization header when supported, and avoid sharing URLs or logs that contain credentials.

Risk: Collected Twitter/X profile and activity data may be unsuitable for some use cases or jurisdictions.

Mitigation: Keep scraping parameters narrow and confirm that the data collection and use are appropriate before running the skill.

Risk: Stored environment files can leak credentials if committed or shared.

Mitigation: Do not commit or share .env files, and review generated outputs and logs for secrets before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/tracking-startup-founders-on-twitter)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables and inline shell command/API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save Apify actor results as CSV or JSON when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
