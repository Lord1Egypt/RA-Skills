## Description:

X (Twitter) analytics and data retrieval via x-analytics-cli for tweet search, tweet counts, user profile lookup, tweet details, and authenticated timeline retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and social media teams use this skill to retrieve X API v2 data with x-analytics-cli, including recent tweet searches, tweet volume counts, profiles, tweet lookups, and authenticated timelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party CLI package globally.

Mitigation: Use a pinned, reviewed package version and prefer a local or sandboxed install instead of a global install.

Risk: The CLI handles X OAuth credentials.

Mitigation: Use least-privilege X tokens, keep credential files owner-readable only, and rotate tokens if they may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bin-huang/skills/x-analytics-cli)
- [x-analytics-cli documentation](https://github.com/Bin-Huang/x-analytics-cli)
- [X API v2 overview](https://docs.x.com/x-api)
- [Tweet Lookup](https://docs.x.com/x-api/posts/lookup)
- [User Lookup](https://docs.x.com/x-api/users/lookup)
- [Recent Search](https://docs.x.com/x-api/posts/search)
- [Tweet Counts](https://docs.x.com/x-api/posts/counts)
- [Timelines](https://docs.x.com/x-api/posts/timelines)
- [X API v2 fields and expansions](https://docs.x.com/x-api/fields)
- [Search query syntax](https://docs.x.com/x-api/posts/search/integrate/build-a-query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may require configured X OAuth credentials and sufficient X API access tier.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
